import os, json, shutil
from typing import List, Dict, Any
from slugify import slugify
from git import Repo
from .utils import temp_workdir, cleanup, docker_run, safe_json_loads
from .models import Finding, ScanResult


TRIVY_IMAGE = os.environ.get("TRIVY_IMAGE", "aquasec/trivy:latest")
SEMGREP_IMAGE = os.environ.get("SEMGREP_IMAGE", "returntocorp/semgrep:latest")
GITLEAKS_IMAGE = os.environ.get("GITLEAKS_IMAGE", "zricethezav/gitleaks:latest")


def clone_repo(repo_url: str, branch: str = "main", token: str | None = None) -> str:
    workdir = temp_workdir("repo")
    if token and repo_url and repo_url.startswith("https://"):
        parts = repo_url.split("https://", 1)[1]
        url = f"https://oauth2:{token}@{parts}"
    else:
        url = repo_url
    Repo.clone_from(url, workdir, branch=branch, depth=1)
    return workdir


def run_trivy(path: str) -> List[Finding]:
    args = ["fs", "--format", "json", "/src"]
    code, out, err = docker_run(TRIVY_IMAGE, args, mounts=[(path, "/src")])
    data = safe_json_loads(out) or {}
    findings: List[Finding] = []
    results = data.get("Results") or []
    for r in results:
        vulns = r.get("Vulnerabilities") or []
        for v in vulns:
            findings.append(Finding(
                tool="trivy",
                severity=(v.get("Severity") or "UNKNOWN").lower(),
                rule_id=v.get("VulnerabilityID"),
                title=v.get("Title") or v.get("PkgName") or "Vulnerability",
                description=v.get("Description"),
                file=r.get("Target"),
                metadata={
                    "pkg": v.get("PkgName"),
                    "installed_version": v.get("InstalledVersion"),
                    "fixed_version": v.get("FixedVersion"),
                    "cvss": v.get("CVSS"),
                    "references": v.get("References"),
                }
            ))
    return findings


def run_semgrep(path: str) -> List[Finding]:
    args = ["semgrep", "--config", "p/ci", "--json", "--quiet"]
    code, out, err = docker_run(SEMGREP_IMAGE, args, mounts=[(path, "/src")], workdir="/src")
    data = safe_json_loads(out) or {}
    findings: List[Finding] = []
    for r in data.get("results", []):
        findings.append(Finding(
            tool="semgrep",
            severity=(r.get("extra", {}).get("severity") or "INFO").lower(),
            rule_id=r.get("check_id"),
            title=r.get("extra", {}).get("message") or r.get("check_id"),
            description=r.get("extra", {}).get("metadata", {}).get("references"),
            file=r.get("path"),
            line=r.get("start", {}).get("line"),
            metadata=r.get("extra", {}),
        ))
    return findings


def run_gitleaks(path: str) -> List[Finding]:
    # Write report to file to capture JSON if stdout formatting changes
    report_path = os.path.join(path, "gitleaks_report.json")
    args = ["detect", "-s", "/src", "-f", "json", "-r", "/src/gitleaks_report.json"]
    code, out, err = docker_run(GITLEAKS_IMAGE, args, mounts=[(path, "/src")])
    findings: List[Finding] = []
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = safe_json_loads(out) or []
    for item in data or []:
        findings.append(Finding(
            tool="gitleaks",
            severity="high",
            rule_id=str(item.get("RuleID") or item.get("Rule")),
            title="Hardcoded secret",
            description=item.get("Description"),
            file=(item.get("File") or item.get("Location", {}).get("File")),
            line=(item.get("StartLine") or item.get("Line")),
            metadata={k: v for k, v in item.items() if k not in ["Description", "File", "Line", "StartLine"]}
        ))
    # cleanup report file
    try:
        os.remove(report_path)
    except Exception:
        pass
    return findings


def aggregate(findings_lists: List[List[Finding]]) -> List[Finding]:
    merged: List[Finding] = []
    for fl in findings_lists:
        merged.extend(fl)
    return merged


def scan_repository(repo_url: str | None, branch: str | None, local_path: str | None, private_token: str | None) -> ScanResult:
    repo_id = repo_url or local_path or "unknown"
    tmp_path = None
    try:
        if local_path:
            path = local_path
        else:
            tmp_path = clone_repo(repo_url, branch or "main", private_token)
            path = tmp_path

        trivy = run_trivy(path)
        semgrep = run_semgrep(path)
        gitleaks = run_gitleaks(path)
        findings = aggregate([trivy, semgrep, gitleaks])

        stats = {
            "total": len(findings),
            "by_tool": {
                "trivy": len(trivy),
                "semgrep": len(semgrep),
                "gitleaks": len(gitleaks),
            },
            "by_severity": {
                "critical": sum(1 for f in findings if f.severity == "critical"),
                "high": sum(1 for f in findings if f.severity == "high"),
                "medium": sum(1 for f in findings if f.severity == "medium"),
                "low": sum(1 for f in findings if f.severity == "low"),
                "info": sum(1 for f in findings if f.severity == "info"),
                "unknown": sum(1 for f in findings if f.severity not in {"critical", "high", "medium", "low", "info"}),
            }
        }

        return ScanResult(repo=repo_id, branch=branch, findings=findings, stats=stats)
    finally:
        if tmp_path:
            cleanup(tmp_path)

import os, shutil, tempfile, subprocess, json, uuid
from typing import Tuple


def run(cmd: list, cwd: str | None = None, timeout: int = 1800) -> Tuple[int, str, str]:
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(timeout=timeout)
    return p.returncode, out, err


def temp_workdir(prefix: str = "sentrius") -> str:
    base = os.environ.get("SENTRIUS_TMP", "/tmp/sentrius")
    os.makedirs(base, exist_ok=True)
    d = tempfile.mkdtemp(prefix=f"{prefix}-", dir=base)
    return d


def cleanup(path: str):
    if path and os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def safe_json_loads(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None


def docker_run(image: str, args: list, mounts: list[tuple[str, str]] | None = None, workdir: str | None = None, env: dict | None = None, network: str | None = None) -> Tuple[int, str, str]:
    cmd = ["docker", "run", "--rm"]
    if mounts:
        for host, cont in mounts:
            cmd += ["-v", f"{host}:{cont}"]
    if workdir:
        cmd += ["-w", workdir]
    if env:
        for k, v in env.items():
            cmd += ["-e", f"{k}={v}"]
    if network:
        cmd += ["--network", network]
    cmd += [image] + args
    return run(cmd)

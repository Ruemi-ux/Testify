import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from typing import List
from .models import ScanRequest, ScanResult, NotifyRequest, ExportRequest, Finding
from .scanner import scan_repository
from notify.alert import broadcast
from splunk.export import export_findings


class Settings(BaseSettings):
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(title="Sentrius API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scan", response_model=ScanResult)
def scan(req: ScanRequest):
    if not req.repo_url and not req.local_path:
        raise HTTPException(400, "Please provide repo_url or local_path")
    try:
        result = scan_repository(req.repo_url, req.branch, req.local_path, req.private_token)
        # Notify on high/critical
        high = [f for f in result.findings if f.severity in ("high", "critical")]
        if high:
            msg = f"{len(high)} high/critical findings in {result.repo} ({result.branch})"
            try:
                broadcast(msg, "critical")
            except Exception:
                pass
        return result
    except Exception as e:
        raise HTTPException(500, f"Scan failed: {e}")


@app.post("/export_splunk")
def export(req: ExportRequest):
    try:
        res = export_findings(req.findings, sourcetype=req.sourcetype, source=req.source or "sentrius-backend")
        return res
    except Exception as e:
        raise HTTPException(500, f"Export failed: {e}")


@app.post("/notify")
def notify(req: NotifyRequest):
    try:
        res = broadcast(req.message, req.level)
        return res
    except Exception as e:
        raise HTTPException(500, f"Notify failed: {e}")

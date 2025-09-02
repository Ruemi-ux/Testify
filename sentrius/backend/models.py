from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ScanRequest(BaseModel):
    repo_url: Optional[str] = None
    branch: Optional[str] = "main"
    local_path: Optional[str] = None
    private_token: Optional[str] = None


class Finding(BaseModel):
    tool: str
    severity: str
    rule_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    file: Optional[str] = None
    line: Optional[int] = None
    metadata: Dict[str, Any] = {}


class ScanResult(BaseModel):
    repo: str
    branch: Optional[str] = None
    findings: List[Finding] = []
    stats: Dict[str, Any] = {}


class NotifyRequest(BaseModel):
    message: str
    level: str = Field(default="info", pattern="^(info|warn|critical)$")


class ExportRequest(BaseModel):
    findings: List[Finding]
    sourcetype: str = "sentrius:findings"
    source: Optional[str] = "sentrius-backend"

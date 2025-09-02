# Sentrius — DevSecOps Security Scanner (MVP)

Sentrius ist ein leichtgewichtiges, modular erweiterbares DevSecOps-MVP, das Repositories mit **Trivy**, **Semgrep** und **Gitleaks** scannt.
Ergebnisse werden im **React Dashboard** angezeigt und können via **Slack/Discord** gemeldet sowie an **Splunk (HEC)** exportiert werden.

## Features (MVP)
- 🔎 Scans: Trivy (Vulnerabilities), Semgrep (SAST), Gitleaks (Secrets)
- 🚀 API: FastAPI `/scan`, `/export_splunk`, `/notify`
- 📊 UI: Minimal-React-Dashboard mit Scan-Button & Liste
- 🤒 CI/CD: GitHub Actions Workflow `.github/workflows/sentrius-scan.yml`
- 📱 Export: Splunk HEC, Slack/Discord Webhooks
- 🔐 Keine Persistenz der Findings

## Quickstart (Dev)
```bash
cp .env.example .env
docker compose up --build
```
Frontend: http://localhost:3000  
Backend: http://localhost:8000/docs

## Endpunkte
- `POST /scan` Body:
```json
{ "repo_url": "https://github.com/org/repo.git", "branch": "main" }
```
Optional: `local_path` statt `repo_url`, `private_token` für private Repos.

- `POST /export_splunk` Body: `{ "findings": [...] }`
- `POST /notify` Body: `{ "message": "text", "level": "info|warn|critical" }`

## Sicherheit
- Keine Speicherung sensibler Daten
- `.env` für Secrets & Konfiguration
- Scanner in isolierten Containern

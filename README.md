# Sentrius – DevSecOps Security Scanner

Sentrius is a lightweight, modular security‑scanner MVP (minimum viable product) designed to help development teams identify security weaknesses early.  It automatically scans source code repositories using several best‑in‑class open‑source tools and aggregates the findings into a single report.  The platform integrates with CI/CD pipelines, provides real‑time notifications, and offers a simple dashboard to review results and export them to other systems such as Splunk.

Sentrius is not a replacement for a full security programme.  It is intended as a foundation for learning about DevSecOps practices and can be extended to fit specific workflows.

## ✨ Features

* **Multi‑tool scanning** – Sentrius orchestrates three complementary scanners:
  * **Trivy** – An all‑in‑one open‑source security scanner that finds vulnerabilities and infrastructure‑as‑code misconfigurations across code repositories, binary artefacts, container images and Kubernetes clusters【230576495311774†L24-L28】.
  * **Semgrep** – A fast static application security testing (SAST) tool that searches code for patterns corresponding to bugs, insecure APIs and coding standards violations.
  * **Gitleaks** – A secret scanner that detects hard‑coded credentials, API keys and other sensitive values in Git repositories.
* **REST API** – A FastAPI backend provides the following endpoints:
  * `POST /scan` – trigger a scan of a Git repository or local folder.
  * `POST /export_splunk` – export findings to Splunk via the HTTP Event Collector (HEC).
  * `POST /notify` – send alert messages to Slack and Discord webhooks.
* **Web Dashboard** – A minimal React dashboard with a “Scan” button, results table and statistics cards.  It displays the findings produced by all three tools and allows exporting them to Splunk.
* **CI/CD Integration** – A GitHub Actions workflow (`.github/workflows/sentrius‑scan.yml`) runs Trivy, Semgrep and Gitleaks on every push or pull request.  The generated reports can be uploaded as artefacts or optionally exported to Splunk.
* **Notifications** – Send high‑severity findings to Slack and Discord channels via webhooks.
* **Secure by default** – Scans run in disposable containers.  Sensitive findings are not persisted on the server, and all secrets (webhook URLs, Splunk tokens, GitHub tokens) are provided via environment variables.

## 🧱 Architecture

Sentrius is composed of a FastAPI backend that exposes a REST API and coordinates the scanning process.  When `/scan` is called, the backend clones the target Git repository into a temporary directory (or uses a local directory), then runs each scanner inside its own Docker container.  The raw outputs are normalised into a common schema and aggregated.  A simple React front‑end calls the API and displays the results.  Optional integrations send notifications and export data.

```
┌───────────────┐      ┌─────────────────────┐
│    Frontend   │──►──│ FastAPI backend      │
│ (React/Vite)  │      │  /scan, /export      │
└───────┬───────┘      └───────┬──────────────┘
        │                      │
        │                      ▼
        │          ┌───────────┴───────────┐
        ▼          │  Trivy  │  Semgrep    │  Gitleaks
    User clicks    │ Scanner │  Scanner    │  Scanner
    “Scan”         └──────────┬────────────┘
                             ▼
                      Findings aggregator
                             ▼
     ┌───────────────────────┼────────────────────────┐
     │                       │                        │
   Splunk               Slack/Discord             GitHub Action
   Export                Alerts                    Workflow
```

## 🚀 Getting Started

### Requirements

- Docker and Docker Compose installed.
- Internet access to pull the scanner images (Trivy, Semgrep, Gitleaks).
- Optional: Splunk HEC URL & token, Slack/Discord webhook URLs.

### Quick Start

1. Clone this repository and switch into the project directory.
2. Copy `.env.example` to `.env` and set your tokens (or leave empty to skip optional integrations).
3. Build and run the stack with Docker Compose:

   ```bash
   cp .env.example .env
   docker compose up --build
   ```
4. Open the dashboard at [http://localhost:3000](http://localhost:3000) and the API docs at [http://localhost:8000/docs](http://localhost:8000/docs).
5. Click “Scan”, enter the Git repository URL and branch name, then wait for results.

### API Usage

To scan a repository via API, send a POST request to `/scan` with a JSON body:

```json
{
  "repo_url": "https://github.com/example/project.git",
  "branch": "main"
}
```

For private repositories, include `private_token` or supply a local path via `local_path`.

### CI/CD

Sentrius includes a GitHub Actions workflow that scans the repository on every push or pull request using the same scanners.  Reports are saved as artefacts.  To enable Splunk export from CI, set the `CI_EXPORT_TO_SPLUNK` environment variable and provide the HEC URL and token via repository secrets.

## 🔐 Security & Privacy

Sentrius is designed to reduce the risk of exposing sensitive information:

* **No persistent storage** – Scan results live only in memory and are returned in the API response.  The backend does not store findings on disk or in a database.
* **Isolated execution** – Each scanner runs in its own container.  The backend interacts with the Docker daemon only to start and destroy containers.
* **Secrets in environment variables** – Webhook URLs and Splunk tokens are passed via `.env` and are not hard‑coded in the codebase.

## 📦 Roadmap

The current MVP implements basic scanning, API endpoints and a simple UI.  Planned improvements include:

1. A modern React dashboard with dark mode and configurable scanner settings.
2. Authentication and user roles for multi‑tenant deployments.
3. Fine‑grained control over rule sets and severity thresholds.
4. Additional output formats and integrations beyond Splunk/Slack/Discord.

## 📝 Example Use Case

> A developer pushes new code to a GitHub repository.  A GitHub Actions workflow triggers Sentrius to run Trivy, Semgrep and Gitleaks on the latest commit.  The FastAPI backend aggregates the findings and highlights critical and high‑severity issues.  The security team sees the results in the dashboard, receives alerts via Slack and Discord, and exports the findings to Splunk for correlation with other logs.

## ℹ️ Disclaimer

Sentrius is provided as an example and learning tool.  It is not a replacement for dedicated security teams or commercial scanning solutions.  Always review findings carefully and keep your scanning tools up to date.

---

## Sentrius – DevSecOps Security Scanner (Deutsch)

Sentrius ist ein leichtgewichtiges, modular erweiterbares MVP (Minimum Viable Product) für DevSecOps‑Sicherheitsscans.  Es durchsucht automatisch Quellcode‑Repositories mit mehreren Open‑Source‑Werkzeugen nach Schwachstellen, Secrets, Fehlkonfigurationen und Compliance‑Verstößen.  Die Plattform integriert sich in CI/CD‑Pipelines, versendet Echtzeit‑Benachrichtigungen und bietet ein einfaches Dashboard zur Auswertung der Ergebnisse und zum Export nach Splunk.

Sentrius ersetzt **nicht** ein vollständiges Sicherheitsprogramm.  Es dient als Lernprojekt und Grundlage für eigene Erweiterungen.

### ✨ Funktionen

* **Mehrfach‑Scans** – Sentrius koordiniert drei ergänzende Scanner:
  * **Trivy** – Ein All‑in‑One‑Sicherheitsscanner, der Schwachstellen (CVE) und Infrastructure‑as‑Code‑Fehlkonfigurationen in Code‑Repositories, Binärartefakten, Container‑Images und Kubernetes‑Clustern erkennt【230576495311774†L24-L28】.
  * **Semgrep** – Ein schneller statischer Code‑Scanner (SAST), der Quellcode nach Mustern durchsucht, die auf Sicherheitslücken, unsichere APIs oder Verstöße gegen Coding‑Standards hinweisen.
  * **Gitleaks** – Ein Secret‑Scanner, der hartkodierte Passwörter, API‑Schlüssel und andere sensible Daten in Git‑Repositories findet.
* **REST‑API** – Das FastAPI‑Backend stellt folgende Endpunkte bereit:
  * `POST /scan` – Startet einen Scan eines Git‑Repos oder lokalen Ordners.
  * `POST /export_splunk` – Exportiert Ergebnisse an Splunk (HEC).
  * `POST /notify` – Sendet Benachrichtigungen an Slack‑ und Discord‑Webhooks.
* **Web‑Dashboard** – Ein minimales React‑Dashboard mit „Scan“-Button, Ergebnistabelle und Statistik‑Karten.  Es zeigt die Ergebnisse aller drei Werkzeuge an und erlaubt den Export nach Splunk.
* **CI/CD‑Integration** – Ein GitHub‑Actions‑Workflow (`.github/workflows/sentrius‑scan.yml`) führt Trivy, Semgrep und Gitleaks bei jedem Push oder Pull‑Request aus.  Die erzeugten Reports können als Artefakte gespeichert oder optional an Splunk exportiert werden.
* **Benachrichtigungen** – Sendet Funde mit hoher oder kritischer Schwere an Slack‑ und Discord‑Kanäle.
* **Sichere Ausführung** – Scans laufen in isolierten Containern.  Ergebnisse werden nicht dauerhaft gespeichert; alle Secrets (Webhook‑URLs, Splunk‑Token, GitHub‑Token) werden über Umgebungsvariablen gesetzt.

### 🧱 Architektur

Das Backend cloniert das Ziel‑Repository in ein temporäres Verzeichnis (oder nutzt einen lokalen Pfad), startet die drei Scanner jeweils in einem separaten Docker‑Container und normalisiert die Ergebnisse in ein gemeinsames Format.  Das React‑Frontend kommuniziert mit der API und stellt die Resultate dar.  Optional können Benachrichtigungen versendet und die Findings exportiert werden.

### 🚀 Schnellstart

1. Repository klonen und ins Projektverzeichnis wechseln.
2. `.env.example` nach `.env` kopieren und Tokens eintragen (oder leer lassen, um optionale Integrationen zu überspringen).
3. Mit Docker Compose starten:

   ```bash
   cp .env.example .env
   docker compose up --build
   ```
4. Dashboard unter [http://localhost:3000](http://localhost:3000) und API‑Dokumentation unter [http://localhost:8000/docs](http://localhost:8000/docs) öffnen.
5. Auf „Scan“ klicken, das Git‑Repository und den Branch angeben und auf die Ergebnisse warten.

### API‑Nutzung

Um einen Scan per API auszulösen, eine POST‑Anfrage an `/scan` senden:

```json
{
  "repo_url": "https://github.com/beispiel/projekt.git",
  "branch": "main"
}
```

Für private Repositories `private_token` angeben oder einen lokalen Pfad über `local_path` senden.

### CI/CD

Der mitgelieferte GitHub‑Actions‑Workflow scannt das Repository bei jedem Push oder Pull‑Request und speichert die Reports als Artefakte.  Um den Export nach Splunk zu aktivieren, `CI_EXPORT_TO_SPLUNK` setzen und die HEC‑URL sowie den Token als Repository‑Secrets hinterlegen.

### 🔐 Sicherheit & Datenschutz

* **Keine Persistenz** – Scan‑Ergebnisse werden nur im API‑Response übermittelt und nicht gespeichert.
* **Isolierte Ausführung** – Jeder Scanner läuft in seinem eigenen Container, wodurch eine Trennung vom Backend gewährleistet ist.
* **Geheime Schlüssel in `.env`** – Webhook‑URLs, Splunk‑Token und Tokens für private Repos werden ausschließlich als Umgebungsvariablen gespeichert.

### 📦 Roadmap

* Modernes React‑Dashboard mit Dark‑Mode und konfigurierbaren Scanner‑Einstellungen
* Authentifizierung und Benutzerrollen für Mehrbenutzer‑Setups
* Erweiterte Filter‑ und Schweregradeinstellungen
* Weitere Export‑Formate und Integrationen neben Splunk/Slack/Discord

### 📝 Beispiel‑Use‑Case

> Ein Entwickler pusht neuen Code in ein GitHub‑Repository.  Ein GitHub‑Actions‑Workflow startet Trivy, Semgrep und Gitleaks auf dem aktuellen Commit.  Das FastAPI‑Backend aggregiert die Ergebnisse und hebt kritische und hohe Schweregrade hervor.  Das Security‑Team sieht die Resultate im Dashboard, erhält Benachrichtigungen via Slack und Discord und exportiert die Findings nach Splunk.

### ℹ️ Haftungsausschluss

Sentrius ist ein Beispiel‑ und Lernprojekt.  Es ersetzt keine professionelle Sicherheitslösung.  Prüfen Sie alle Ergebnisse sorgfältig und halten Sie Ihre Sicherheitstools stets aktuell.
import os, json, requests

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")


def send_slack(message: str, level: str = "info"):
    if not SLACK_WEBHOOK_URL:
        return {"status": "skipped", "reason": "no webhook configured"}
    payload = {"text": f"[Sentrius][{level.upper()}] {message}"}
    r = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=15)
    return {"status": "ok", "code": r.status_code}


def send_discord(message: str, level: str = "info"):
    if not DISCORD_WEBHOOK_URL:
        return {"status": "skipped", "reason": "no webhook configured"}
    payload = {"content": f"[Sentrius][{level.upper()}] {message}"}
    r = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=15)
    return {"status": "ok", "code": r.status_code}


def broadcast(message: str, level: str = "info"):
    res = {
        "slack": send_slack(message, level),
        "discord": send_discord(message, level),
    }
    return res

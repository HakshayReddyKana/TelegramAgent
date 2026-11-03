"""
Run this script ONCE after deploying to Vercel to register your webhook URL with Telegram.

Usage:
    python setup_webhook.py

Make sure to set BOT_TOKEN before running.
"""

import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN") or input("Enter your BOT_TOKEN: ").strip()
BOT_URL = os.environ.get("BOT_URL", "https://agent.hakshay.engineer").rstrip("/")

WEBHOOK_URL = f"{BOT_URL}/api/webhook"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def set_webhook():
    print(f"\n📡 Setting webhook to: {WEBHOOK_URL}")
    resp = requests.post(
        f"{TELEGRAM_API}/setWebhook",
        json={"url": WEBHOOK_URL},
        timeout=10,
    )
    data = resp.json()
    if data.get("ok"):
        print("✅ Webhook set successfully!")
    else:
        print(f"❌ Failed to set webhook: {data}")


def get_webhook_info():
    resp = requests.get(f"{TELEGRAM_API}/getWebhookInfo", timeout=10)
    info = resp.json().get("result", {})
    print("\n📋 Current Webhook Info:")
    print(f"  URL:            {info.get('url', 'Not set')}")
    print(f"  Pending updates: {info.get('pending_update_count', 0)}")
    print(f"  Last error:     {info.get('last_error_message', 'None')}")


def set_commands():
    """Register bot commands so they appear in the Telegram menu."""
    commands = [
        {"command": "start", "description": "Welcome message"},
        {"command": "help", "description": "List all commands"},
        {"command": "about", "description": "About this bot"},
        {"command": "ping", "description": "Check bot status"},
    ]
    resp = requests.post(
        f"{TELEGRAM_API}/setMyCommands",
        json={"commands": commands},
        timeout=10,
    )
    data = resp.json()
    if data.get("ok"):
        print("✅ Bot commands registered!")
    else:
        print(f"❌ Failed to set commands: {data}")


if __name__ == "__main__":
    set_webhook()
    set_commands()
    get_webhook_info()

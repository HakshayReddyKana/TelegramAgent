import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ──────────────────────────────────────────────
#  Telegram helper functions
# ──────────────────────────────────────────────

def send_message(chat_id: int, text: str, parse_mode: str = "Markdown") -> dict:
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    resp = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=10)
    return resp.json()


def send_typing(chat_id: int) -> None:
    requests.post(
        f"{TELEGRAM_API}/sendChatAction",
        json={"chat_id": chat_id, "action": "typing"},
        timeout=5,
    )


# ──────────────────────────────────────────────
#  Command handlers
# ──────────────────────────────────────────────

def handle_start(chat_id: int, first_name: str) -> None:
    text = (
        f"👋 Hey *{first_name}*! Welcome!\n\n"
        "I'm your personal Telegram bot.\n\n"
        "Use the commands below to get started:\n"
        "• /start — Show this welcome message\n"
        "• /help  — List all available commands\n"
        "• /about — Learn more about this bot\n"
        "• /ping  — Check if I'm alive\n"
    )
    send_message(chat_id, text)


def handle_help(chat_id: int) -> None:
    text = (
        "🛠 *Available Commands*\n\n"
        "/start — Welcome message\n"
        "/help  — This help menu\n"
        "/about — About this bot\n"
        "/ping  — Check bot status\n"
        "\n_More commands coming soon!_"
    )
    send_message(chat_id, text)


def handle_about(chat_id: int) -> None:
    text = (
        "🤖 *About This Bot*\n\n"
        "Built with *Python* + *Flask*, deployed on *Vercel*.\n\n"
        "Source code is open and fully customizable.\n"
        "Add your own commands in `api/webhook.py`!"
    )
    send_message(chat_id, text)


def handle_ping(chat_id: int) -> None:
    send_message(chat_id, "🏓 *Pong!* I'm alive and kicking.")


def handle_unknown(chat_id: int, text: str) -> None:
    send_message(
        chat_id,
        f"🤔 I don't understand `{text}`.\nTry /help to see what I can do.",
    )


def handle_message(chat_id: int, text: str) -> None:
    """Echo back plain messages (non-command)."""
    send_message(chat_id, f"You said:\n> {text}\n\nUse /help to see my commands.")


# ──────────────────────────────────────────────
#  Main router
# ──────────────────────────────────────────────

def process_update(update: dict) -> None:
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat_id: int = message["chat"]["id"]
    first_name: str = message.get("from", {}).get("first_name", "there")
    text: str = message.get("text", "")

    send_typing(chat_id)

    if text.startswith("/"):
        # Strip bot username suffix (e.g. /start@MyBot -> /start)
        command = text.split("@")[0].split(" ")[0].lower()

        if command == "/start":
            handle_start(chat_id, first_name)
        elif command == "/help":
            handle_help(chat_id)
        elif command == "/about":
            handle_about(chat_id)
        elif command == "/ping":
            handle_ping(chat_id)
        else:
            handle_unknown(chat_id, command)
    else:
        handle_message(chat_id, text)


# ──────────────────────────────────────────────
#  Vercel / Flask routes
# ──────────────────────────────────────────────

@app.route("/api/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json(force=True)
        if update:
            process_update(update)
    except Exception as e:
        # Never crash — always return 200 so Telegram doesn't retry
        print(f"Error processing update: {e}")

    return jsonify({"ok": True}), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Bot is running 🚀", "version": "1.0.0"}), 200


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


# ──────────────────────────────────────────────
#  Local dev entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Running locally on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)

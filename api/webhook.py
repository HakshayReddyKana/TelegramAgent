import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ──────────────────────────────────────────────
#  Telegram helper functions
# ──────────────────────────────────────────────

async def send_message(chat_id: int, text: str, parse_mode: str = "Markdown") -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=10,
        )
    return resp.json()


async def send_typing(chat_id: int) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_API}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
            timeout=5,
        )


# ──────────────────────────────────────────────
#  Command handlers
# ──────────────────────────────────────────────

async def handle_start(chat_id: int, first_name: str) -> None:
    text = (
        f"👋 Hey *{first_name}*! Welcome!\n\n"
        "I'm your personal Telegram bot.\n\n"
        "Use the commands below to get started:\n"
        "• /start — Show this welcome message\n"
        "• /help  — List all available commands\n"
        "• /about — Learn more about this bot\n"
        "• /ping  — Check if I'm alive\n"
    )
    await send_message(chat_id, text)


async def handle_help(chat_id: int) -> None:
    text = (
        "🛠 *Available Commands*\n\n"
        "/start — Welcome message\n"
        "/help  — This help menu\n"
        "/about — About this bot\n"
        "/ping  — Check bot status\n"
        "\n_More commands coming soon!_"
    )
    await send_message(chat_id, text)


async def handle_about(chat_id: int) -> None:
    text = (
        "🤖 *About This Bot*\n\n"
        "Built with *Python* + *FastAPI*, deployed on *Vercel*.\n\n"
        "Source code is open and fully customizable.\n"
        "Add your own commands in `api/webhook.py`!"
    )
    await send_message(chat_id, text)


async def handle_ping(chat_id: int) -> None:
    await send_message(chat_id, "🏓 *Pong!* I'm alive and kicking.")


async def handle_unknown(chat_id: int, command: str) -> None:
    await send_message(
        chat_id,
        f"🤔 I don't understand `{command}`.\nTry /help to see what I can do.",
    )


async def handle_message(chat_id: int, text: str) -> None:
    """Echo back plain messages (non-command)."""
    await send_message(chat_id, f"You said:\n> {text}\n\nUse /help to see my commands.")


# ──────────────────────────────────────────────
#  Main router
# ──────────────────────────────────────────────

async def process_update(update: dict) -> None:
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat_id: int = message["chat"]["id"]
    first_name: str = message.get("from", {}).get("first_name", "there")
    text: str = message.get("text", "")

    await send_typing(chat_id)

    if text.startswith("/"):
        # Strip bot username suffix (e.g. /start@MyBot -> /start)
        command = text.split("@")[0].split(" ")[0].lower()

        if command == "/start":
            await handle_start(chat_id, first_name)
        elif command == "/help":
            await handle_help(chat_id)
        elif command == "/about":
            await handle_about(chat_id)
        elif command == "/ping":
            await handle_ping(chat_id)
        else:
            await handle_unknown(chat_id, command)
    else:
        await handle_message(chat_id, text)


# ──────────────────────────────────────────────
#  FastAPI routes
# ──────────────────────────────────────────────

@app.post("/api/webhook")
async def webhook(request: Request):
    try:
        update = await request.json()
        if update:
            await process_update(update)
    except Exception as e:
        # Never crash — always return 200 so Telegram doesn't retry
        print(f"Error processing update: {e}")

    return JSONResponse({"ok": True})


@app.get("/")
async def index():
    return JSONResponse({"status": "Bot is running 🚀", "version": "1.0.0"})


@app.get("/api/health")
async def health():
    return JSONResponse({"status": "healthy"})

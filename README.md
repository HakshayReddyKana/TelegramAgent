# 🤖 Telegram Bot — Python + Vercel

A Telegram bot built with **Python (Flask)** and deployed as a **Vercel serverless function**.

---

## 📁 Project Structure

```
TelegramAgent/
├── api/
│   └── webhook.py      ← Main bot logic (Flask app)
├── requirements.txt    ← Python dependencies
├── vercel.json         ← Vercel routing config
├── setup_webhook.py    ← One-time webhook registration script
├── .env.example        ← Env variable template
└── .gitignore
```

---

## 🚀 Deployment Steps

### 1. Get a Bot Token
1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the prompts
3. Copy your **Bot Token**

### 2. Deploy to Vercel
1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → **New Project** → Import your repo
3. Add an **Environment Variable**:
   - Key: `BOT_TOKEN`
   - Value: your token from BotFather
4. Click **Deploy**

### 3. Register the Webhook
After deployment, run this once:
```bash
set BOT_TOKEN=your_token_here
python setup_webhook.py
```

That's it! Your bot is live 🎉

---

## 🛠 Available Commands

| Command  | Description            |
|----------|------------------------|
| /start   | Welcome message        |
| /help    | List all commands      |
| /about   | About this bot         |
| /ping    | Check bot status       |

---

## ➕ Adding New Commands

Open [`api/webhook.py`](api/webhook.py) and:

1. Add a new handler function:
```python
def handle_mycommand(chat_id: int) -> None:
    send_message(chat_id, "Your response here!")
```

2. Add a case in `process_update()`:
```python
elif command == "/mycommand":
    handle_mycommand(chat_id)
```

---

## 💻 Running Locally

```bash
pip install -r requirements.txt

# Create .env from template
copy .env.example .env
# Edit .env and add your BOT_TOKEN

python api/webhook.py
```

> Note: For local testing, use [ngrok](https://ngrok.com/) to expose your local server and run `setup_webhook.py` with the ngrok URL.

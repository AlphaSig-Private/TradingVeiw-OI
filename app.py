from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Telegram bot credentials (set these in Render's environment settings)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "-1003114080821"  # Your Telegram group ID

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "🚨 TradingView Alert Triggered")

    # Optional: include chart snapshot if TradingView sends one
    chart_url = data.get("chart_image_url")
    if chart_url:
        send_photo(chart_url, message)
    else:
        send_message(message)

    return "OK", 200

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload)

def send_photo(photo_url, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": photo_url,
        "caption": caption
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

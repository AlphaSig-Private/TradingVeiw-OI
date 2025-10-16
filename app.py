import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    response = requests.post(url, json=payload)
    print("Text response:", response.text)

def send_photo(photo_url, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": photo_url,
        "caption": caption
    }
    response = requests.post(url, json=payload)
    print("Photo response:", response.text)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("Webhook triggered")
    data = request.get_json()
    print("Received data:", data)

    if not data:
        return "Invalid JSON", 400

    message = data.get("message", "🚨 Alert received")
    chart_url = data.get("chart_image_url")

    if chart_url:
        send_photo(chart_url, message)
    else:
        send_message(message)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 🔐 ЗАМЕНИ НА СВОЙ ТОКЕН
BOT_TOKEN = "7934534421:AAGSYTjC-4f8U8nhnh3FKsSeh0wtQaOmC6o"
CHAT_ID = "973779570"  # Твой Telegram ID

# Ссылка на твой Telegram-канал или чат
YOUR_TELEGRAM_LINK = "https://t.me/meutask"  # Измени на свой чат-линк

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send_message():
    user_msg = request.json.get("message")
    
    if not user_msg:
        return jsonify({"error": "Нет сообщения"}), 400

    # Ответ на "привет"
    if user_msg.lower() == "привет":
        text = "Привет! Нажми кнопку, чтобы перейти в мой Telegram-чат!"
        reply_markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "Ссылка",
                        "url": YOUR_TELEGRAM_LINK
                    }
                ]
            ]
        }
    else:
        text = user_msg  # Если это не "привет", просто повторяем сообщение
        reply_markup = None

    # Отправляем сообщение пользователю через Telegram Bot API
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "reply_markup": reply_markup
    }
    
    response = requests.post(telegram_url, json=payload)

    if response.ok:
        return jsonify({"status": "ok", "reply": text, "reply_markup": reply_markup})
    else:
        return jsonify({"error": "Ошибка при отправке в Telegram"}), 500

if __name__ == "__main__":
    app.run(debug=True)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

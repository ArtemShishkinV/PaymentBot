from flask import Flask, request
import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
import uuid
from yookassa import Configuration, Payment

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def create_payment(chat_id):
    Configuration.account_id = get_from_env("SHOP_ID")
    Configuration.secret_key = get_from_env("PAYMENT_TOKEN")

    return Payment.create({
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.google.com"
        },
        "capture": True,
        "description": "Заказ №1",
        "metadata": {"chat_id", chat_id}
    }, uuid.uuid4())


def get_from_env(key):
    return os.environ.get(key)


token = get_from_env('TELEGRAM_BOT_TOKEN')


def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route('/', methods=["POST"])
def process():
    chat_id = request.json["message"]["chat"]["id"]
    send_message(chat_id=chat_id, text=create_payment(chat_id).confirmation.confirmation_url)
    return {"ok": True}


if __name__ == '__main__':
    app.run()

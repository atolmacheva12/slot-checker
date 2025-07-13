import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://www.eestipiir.ee/yphis/viewQueueTimes.action"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")

def check_slots():
    try:
        headers = {
           "User-Agent": "Mozilla/5.0",
           "Accept": "application/json"
        }
        response = requests.get(URL, headers=headers, timeout=30)
        data = response.json()
    except Exception as e:
        print("Ошибка при получении JSON:", e)
        return

    found = False
    for checkpoint in data:
        name = checkpoint.get("name")
        queueTimes = checkpoint.get("queueTimes", [])
        for row in queueTimes:
            if row.get("title", "").lower() == "first available pre-reservation time":
                slot_d = row.get("D")
                if slot_d and slot_d.lower() != "not available":
                    message = f"[{name}] Категория D: первый слот — {slot_d}"
                    print(message)
                    send_telegram_message(message)
                    found = True
    if not found:
        print("Нет доступных слотов для категории D")

if __name__ == "__main__":
    check_slots()

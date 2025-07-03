
import time
import requests
import telegram
import os

# === НАСТРОЙКИ ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.eestipiir.ee/yphis/borderQueueInfo.action"

def check_slots():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            return

        content = response.text.lower()
        if "koi" in content or "luha" in content:
            if "vaba" in content or "free" in content:
                message = "🟢 Есть свободный таймслот на Койдула или Лухамаа!"
                bot = telegram.Bot(token=TELEGRAM_TOKEN)
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
                print("Отправлено сообщение:", message)
            else:
                print("Нет свободных таймслотов.")
        else:
            print("Не удалось найти пункты пропуска в тексте.")
    except Exception as e:
        print("Ошибка:", e)

# === ЦИКЛ ПРОВЕРКИ КАЖДЫЕ 80 СЕКУНД ===
while True:
    check_slots()
    time.sleep(80)

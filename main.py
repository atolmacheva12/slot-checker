import requests
from bs4 import BeautifulSoup
import telegram
import os
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.eestipiir.ee/yphis/borderQueueInfo.action"

def check_slots():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Найти таблицу и нужную строку с "First available pre-reservation time"
        rows = soup.find_all("tr")
        target_row = None
        for row in rows:
            if "First available pre-reservation time" in row.text:
                target_row = row
                break

        if not target_row:
            print("Не удалось найти строку с First available pre-reservation time")
            return

        # В строке взять все ячейки (td)
        cells = target_row.find_all("td")

        # Заголовки столбцов в таблице (по ним определяем индекс нужных столбцов)
        header_row = soup.find("tr")  # предполагаем, что первая строка — заголовок
        headers = [th.text.strip() for th in header_row.find_all("th")]

        messages = []

        for place in ["Koidula A/B", "Luhamaa A/B"]:
            try:
                idx = headers.index(place)
            except ValueError:
                print(f"Не найден столбец '{place}'")
                continue

            value = cells[idx].text.strip()

            if value:
                messages.append(f"🟢 Есть свободный таймслот в {place}: {value}")

        if messages:
            bot = telegram.Bot(token=TELEGRAM_TOKEN)
            for msg in messages:
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
                print("Отправлено сообщение:", msg)
        else:
            print("Свободных таймслотов нет.")

    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    while True:
        check_slots()
        time.sleep(80)

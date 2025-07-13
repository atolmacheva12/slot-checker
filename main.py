print("СКРИПТ ЗАПУЩЕН")
import time
import requests
import telegram
import os
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.eestipiir.ee/yphis/borderQueueInfo.action"

def check_slots():
    try:
        response = requests.get(URL, timeout=30)
        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            return

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find('table', {'class': 'borderQueueTable'})
        if not table:
            print("Не найдена таблица с данными")
            return

        headers = [th.text.strip() for th in table.find_all('th')]
        ab_columns_indices = [i for i, h in enumerate(headers) if 'A/B' in h]

        if not ab_columns_indices:
            print("Не найдены столбцы с 'A/B'")
            return

        first_available_row = None
        for tr in table.find_all('tr'):
            tds = tr.find_all(['th', 'td'])
            if tds and 'First available pre-reservation time' in tds[0].text:
                first_available_row = tds
                break

        if not first_available_row:
            print("Не найдена строка 'First available pre-reservation time'")
            return

        messages = []
        for idx in ab_columns_indices:
            time_val = first_available_row[idx].text.strip()
            if time_val:
                place_name = headers[idx]
                messages.append(f"🟢 Есть свободный таймслот в {place_name}: {time_val}")

        if messages:
            bot = telegram.Bot(token=TELEGRAM_TOKEN)
            for msg in messages:
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
                print("Отправлено сообщение:", msg)
        else:
            print("Свободных таймслотов нет в колонках A/B")

    except Exception as e:
        print("Ошибка:", e)

while True:
    check_slots()
    time.sleep(80)

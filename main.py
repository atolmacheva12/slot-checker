import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = "https://www.eestipiir.ee/yphis/borderQueueInfo.action"

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
        response = requests.get(URL, timeout=30)
        if response.status_code != 200:
            print("Ошибка запроса:", response.status_code)
            return
    except Exception as e:
        print("Ошибка при запросе:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "borderQueueTable"})
    if not table:
        print("Не найдена таблица с данными")
        return

    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if not cells:
            continue
        if "first available pre-reservation time" in row.get_text().lower():
            if len(cells) >= 4:
                d_cell = cells[3].get_text(strip=True)
                if d_cell and d_cell.lower() != "not available":
                    print("Найдено значение в колонке D:", d_cell)
                    send_telegram_message(f"Свободное время для категории D: {d_cell}")
                else:
                    print("Ячейка D пуста или недоступна")
            else:
                print("Недостаточно колонок в строке")
            break

if __name__ == "__main__":
    check_slots()

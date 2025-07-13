import requests
from bs4 import BeautifulSoup

# === НАСТРОЙКИ ===
URL = "https://www.eestipiir.ee/yphis/borderQueueInfo.action"

# Токен и ID Telegram
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

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
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "borderQueueTable"})

    if not table:
        print("Не найдена таблица с данными")
        return

    # 1. Найти номер колонки D
    headers = table.find("thead").find_all("th")
    d_index = None
    for idx, th in enumerate(headers):
        if th.text.strip() == "D":
            d_index = idx
            break

    if d_index is None:
        print("Не найдена колонка D")
        return

    # 2. Найти строку 'First available pre-reservation time'
    for row in table.find("tbody").find_all("tr"):
        first_cell = row.find("th") or row.find("td")
        if not first_cell:
            continue
        row_title = first_cell.text.strip()
        if "First available pre-reservation time" in row_title:
            cells = row.find_all(["td", "th"])
            if d_index < len(cells):
                value = cells[d_index].text.strip()
                if value and value.lower() != "not available":
                    print(f"Найден слот: {value}")
                    send_telegram_message(f"Категория D – первый слот: {value}")
                else:
                    print("Слот не найден или недоступен")
                return

    print("Не найдена строка с 'First available pre-reservation time'")

# === ЗАПУСК ===
if _name_ == "_main_":
    check_slots()

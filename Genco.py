import requests
from bs4 import BeautifulSoup
import csv
from telegram.ext import Application, CommandHandler

TOKEN = "place your token here"
CHAT_ID = None #change it once you start the bot with command /getid

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://genshin-impact.fandom.com/"
}

def get_data():
    url = "https://genshin-impact.fandom.com/wiki/Promotional_Codes"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return [], []
    
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="wikitable")
    if not tables:
        print("Таблицы с классом 'wikitable' не найдены!")
        return [], []
    
    table = tables[0]
    codes = []
    rewards = []

    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        if len(columns) > 0:
            code_element = columns[0].find("a")
            reward_td = columns[1] if len(columns) > 1 else None
            expired_check = columns[0].find("i", string="Expired")

            if not expired_check and code_element:
                code = code_element.text.strip()
                reward = reward_td.text.strip() if reward_td else "Неизвестно"
                codes.append(code)
                rewards.append(reward)

    print(f"Найдено кодов: {len(codes)}")
    return codes, rewards

async def start(update, context):
    await update.message.reply_text("Привет! Я бот для промокодов Genshin Impact. Напиши /codes для кодов!")

async def send_codes(update, context):
    codes, rewards = get_data()
    if codes:
        message = "Актуальные промокоды:\n"
        for code, reward in zip(codes, rewards):
            message += f"Код: {code} | Награда: {reward}\n"
        
        # Записываем в CSV
        with open("Promocodes.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Code", "Reward"])
            for code, reward in zip(codes, rewards):
                writer.writerow([code, reward])
    else:
        message = "Пока нет активных кодов :("
    await update.message.reply_text(message)

async def get_chat_id(update, context):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Твой CHAT_ID: {chat_id}")

def main():
    # Создаём приложение
    app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("codes", send_codes))
    app.add_handler(CommandHandler("getid", get_chat_id))

    # Запускаем бота
    print("Бот запущен! Напиши ему в Telegram.")
    app.run_polling()

if __name__ == "__main__":
    main()
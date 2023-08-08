import os

import dotenv
import telegram

if __name__ == "__main__":
    dotenv.load_dotenv()
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    bot.send_message(text="Test", chat_id=os.environ["TELEGRAM_CHAT"])

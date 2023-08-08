import os
import shutil
import time
from random import shuffle

import dotenv
import telegram
import argparse

from nasa_api import fetch_nasa_apod, fetch_nasa_epic
from spacex_api import fetch_spacex_last_launch


def send_photo(bot: telegram.Bot, dir_name: str):
    files = os.listdir(dir_name)
    shuffle(files)
    for file_name in files:
        file_path = os.path.join(dir_name, file_name)
        with open(file_path, "rb") as f:
            bot.send_photo(photo=f.read(), chat_id=os.getenv("TELEGRAM_CHAT_ID"))
            time.sleep(int(os.getenv("DELEY_SECONDS", 4 * 60 * 60)))


def run_bot():
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="NASA apod count",
        default=50,
    )
    parser.add_argument(
        "-d", "--dir_name", type=str, help="Directory path", default="images"
    )
    args = parser.parse_args()

    if os.path.isdir("images"):
        shutil.rmtree("images")

    fetch_spacex_last_launch()
    fetch_nasa_apod(count=args.count, dir_name=args.dir_name)
    fetch_nasa_epic(dir_name=args.dir_name)

    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    while True:
        send_photo(bot, dir_name=args.dir_name)


if __name__ == "__main__":
    run_bot()

import argparse
import os
import shutil
import time
from random import shuffle

import dotenv
import telegram

from nasa_api import fetch_nasa_apod, fetch_nasa_epic
from spacex_api import fetch_spacex_last_launch


def send_photo(bot: telegram.Bot, chat_id: str, file_path: str):
    with open(file_path, "rb") as f:
        bot.send_photo(photo=f.read(), chat_id=chat_id)


def send_photos(bot: telegram.Bot, chat_id: str, dir_name: str, deley_seconds: int):
    files = os.listdir(dir_name)
    shuffle(files)
    for file_name in files:
        file_path = os.path.join(dir_name, file_name)
        send_photo(bot, chat_id, file_path)
        time.sleep(deley_seconds)


def run_bot():
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="NASA apod count (default: 50)",
        default=50,
    )
    parser.add_argument(
        "-d",
        "--dir_name",
        type=str,
        help="Directory name (default: {DEFAULT_DIRECTORY_NAME})".format(**os.environ),
        default=os.getenv("DEFAULT_DIRECTORY_NAME"),
    )
    args = parser.parse_args()

    if os.path.isdir(args.dir_name):
        shutil.rmtree(args.dir_name)

    fetch_spacex_last_launch(dir_name=args.dir_name)
    fetch_nasa_apod(
        token=os.getenv("NASA_TOKEN"), count=args.count, dir_name=args.dir_name
    )
    fetch_nasa_epic(token=os.getenv("NASA_TOKEN"), dir_name=args.dir_name)

    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    while True:
        send_photos(
            bot,
            chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            dir_name=args.dir_name,
            deley_seconds=int(os.getenv("DELEY_SECONDS", 4 * 60 * 60)),
        )


if __name__ == "__main__":
    run_bot()

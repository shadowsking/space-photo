import argparse
import os
from datetime import datetime

import dotenv
import requests

from file_helper import download_file, get_file_extension


def fetch_nasa_apod(count: int, dir_name: str | None = None):
    dir_name = dir_name or "images"

    response = requests.get(
        "https://api.nasa.gov/planetary/apod",
        params={"api_key": os.environ["NASA_TOKEN"], "count": count},
    )
    response.raise_for_status()

    for index, apod in enumerate(response.json()):
        file_path = os.path.join(
            dir_name,
            "nasa_apod_{index}{ext}".format(
                index=index, ext=get_file_extension(apod.get("url"))
            ),
        )
        download_file(apod.get("url"), file_path)


def fetch_nasa_epic(dir_name: str | None = None):
    dir_name = dir_name or "images"

    response = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/images",
        params={
            "api_key": os.environ["NASA_TOKEN"],
        },
    )
    response.raise_for_status()

    for index, epic in enumerate(response.json()):
        date = datetime.fromisoformat(epic.get("date"))
        url = "https://api.nasa.gov/EPIC/archive/natural/{year}/{month:02}/{day:02}/png/{image}.png".format(
            year=date.year,
            month=round(date.month, 2),
            day=round(date.day, 2),
            index=index,
            **epic
        )
        file_path = os.path.join(
            dir_name,
            "nasa_epic_{index}{ext}".format(index=index, ext=get_file_extension(url)),
        )
        download_file(url, file_path, params={"api_key": os.environ["NASA_TOKEN"]})


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--apod", help="NASA apod photos", action="store_true")
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="NASA apod count",
        default=5,
    )
    parser.add_argument(
        "-d", "--dir_name", type=str, help="Directory path", default="images"
    )
    parser.add_argument(
        "-e",
        "--epic",
        help="NASA Epic photos",
        action="store_true",
    )

    args = parser.parse_args()
    if args.apod:
        fetch_nasa_apod(count=args.count, dir_name=args.dir_name)

    if args.epic:
        fetch_nasa_epic(dir_name=args.dir_name)

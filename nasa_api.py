import argparse
import os
from datetime import datetime

import dotenv
import requests

from file_helper import download_file, get_file_extension


def fetch_nasa_apod(token: str, count: int, dir_name: str):
    response = requests.get(
        "https://api.nasa.gov/planetary/apod",
        params={"api_key": token, "count": count},
    )
    response.raise_for_status()

    for index, apod in enumerate(response.json()):
        file_extension = get_file_extension(apod.get("url"))
        file_name = "nasa_apod_{index}{ext}".format(index=index, ext=file_extension)
        file_path = os.path.join(dir_name, file_name)
        download_file(apod.get("url"), file_path)


def fetch_nasa_epic(token: str, dir_name: str):
    payload = {
        "api_key": token,
    }
    response = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/images",
        params=payload,
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
        file_extension = get_file_extension(url)
        file_name = "nasa_epic_{index}{ext}".format(index=index, ext=file_extension)
        file_path = os.path.join(dir_name, file_name)
        download_file(url, file_path, params=payload)


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--apod", help="Downloads APOD images", action="store_true"
    )
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
    parser.add_argument(
        "-e",
        "--epic",
        help="Downloads Epic images",
        action="store_true",
    )

    args = parser.parse_args()
    if args.apod:
        fetch_nasa_apod(
            token=os.getenv("NASA_TOKEN"), count=args.count, dir_name=args.dir_name
        )

    if args.epic:
        fetch_nasa_epic(token=os.getenv("NASA_TOKEN"), dir_name=args.dir_name)

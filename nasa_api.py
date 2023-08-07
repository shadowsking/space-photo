import os
from datetime import datetime

import dotenv
import requests

from utils import download_image, get_file_extension


def fetch_nasa_apod(count: int, dir_name: str = "images"):
    response = requests.get(
        "https://api.nasa.gov/planetary/apod",
        params={"api_key": os.environ["NASA_API_KEY"], "count": count},
    )
    response.raise_for_status()

    for index, apod in enumerate(response.json()):
        file_path = os.path.join(
            dir_name,
            "nasa_apod_{index}.{ext}".format(
                index=index, ext=get_file_extension(apod.get("url"))
            ),
        )
        download_image(apod.get("url"), file_path)


def fetch_nasa_epic(dir_name: str = "images"):
    response = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/images",
        params={
            "api_key": os.environ["NASA_API_KEY"],
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
            "nasa_epic_{index}.{ext}".format(index=index, ext=get_file_extension(url)),
        )
        download_image(url, file_path, params={"api_key": os.environ["NASA_API_KEY"]})


if __name__ == "__main__":
    dotenv.load_dotenv()
    fetch_nasa_apod(count=5, dir_name="apod_folder_images")

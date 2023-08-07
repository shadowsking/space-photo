import os.path

import requests

from utils import download_image, get_file_extension


def get_latest_launch(has_images: bool = False) -> dict:
    payload = {
        "options": {"limit": 1, "sort": {"flight_number": "desc"}},
    }
    if has_images:
        payload.update({"query": {"links.flickr.original": {"$ne": []}}})

    response = requests.post(
        "https://api.spacexdata.com/v5/launches/query", json=payload
    )
    response.raise_for_status()
    return response.json()


def get_latest_images() -> list:
    docs = get_latest_launch(has_images=True).get("docs")
    if not docs:
        return []

    return docs[-1]["links"]["flickr"]["original"]


def fetch_spacex_last_launch(dir_name: str | None = "images"):
    for index, url in enumerate(get_latest_images()):
        file_path = os.path.join(
            dir_name,
            "spacex_{index}.{ext}".format(index=index, ext=get_file_extension(url)),
        )
        download_image(url, file_path)


if __name__ == "__main__":
    fetch_spacex_last_launch()

import argparse
import os.path

import requests

from file_helper import download_file, get_file_extension


def get_latest_launch(launch_uuid: str = None, has_images: bool = False) -> dict:
    payload = {
        "options": {"limit": 1, "sort": {"flight_number": "desc"}},
        "query": {},
    }

    if launch_uuid:
        payload["query"].update({"id": {"$eq": launch_uuid}})

    if has_images:
        payload["query"].update({"links.flickr.original": {"$ne": []}})

    response = requests.post(
        "https://api.spacexdata.com/v5/launches/query", json=payload
    )
    response.raise_for_status()
    return response.json()


def get_latest_images(launch_uuid: str = None) -> list:
    docs = get_latest_launch(launch_uuid=launch_uuid, has_images=True).get("docs")
    if not docs:
        return []

    return docs[-1]["links"]["flickr"]["original"]


def fetch_spacex_last_launch(launch_uuid: str = None, dir_name: str | None = None):
    dir_name = dir_name or "images"

    for index, url in enumerate(get_latest_images(launch_uuid)):
        file_path = os.path.join(
            dir_name,
            "spacex_{index}{ext}".format(index=index, ext=get_file_extension(url)),
        )
        download_file(url, file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--uuid",
        help="SpaceX launch uuid",
    )
    args = parser.parse_args()
    fetch_spacex_last_launch(launch_uuid=args.uuid)

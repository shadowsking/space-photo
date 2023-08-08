import os
from urllib.parse import urlparse

import requests


def download_file(url: str, file_path: str, params: dict | None = None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    if not os.path.isdir(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, "wb") as f:
        f.write(response.content)


def get_file_extension(url: str) -> str:
    _, extension = os.path.splitext(urlparse(url).path)
    return extension

import os
from urllib.parse import urlparse

import requests


def download_file(url: str, file_path: str, params: dict = None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(response.content)


def get_file_extension(url: str) -> str:
    _, extension = os.path.splitext(urlparse(url).path)
    return extension

import os
import shutil

import dotenv

from nasa_api import fetch_nasa_apod, fetch_nasa_epic
from spacex_api import fetch_spacex_last_launch


def main():
    dotenv.load_dotenv()

    if os.path.isdir("images"):
        shutil.rmtree("images")

    fetch_spacex_last_launch()
    fetch_nasa_apod(50)
    fetch_nasa_epic()


if __name__ == "__main__":
    main()

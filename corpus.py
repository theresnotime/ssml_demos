import json
import os

import requests


def get_words(data: object) -> list:
    """Return a list of all words in the corpus"""
    try:
        return dict(data["words"])
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


def get_corpus(url: str, data_file: str) -> object:
    """Get word corpus, or download if not already present"""
    try:
        if os.path.isfile(data_file) is False:
            print(f"{data_file} does not exist, downloading...")
            if download_corpus(url, data_file) is False:
                raise Exception("failed to get corpus data")
        else:
            print(f"{data_file} already exists")
        return open_data(data_file)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


def download_corpus(url: str, data_file: str) -> bool:
    """Download the corpus from the given URL and save it to the given file"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(data_file, "wb") as file:
                file.write(response.content)
                file.close()
            print(f"{data_file} downloaded")
            return True
        else:
            print(f"{response.status_code}: could not download {data_file}")
            return False
    except Exception as e:
        print(f"Error {e}")
        exit(1)


def open_data(data_file: str) -> object:
    """Open the given data file and return the contents as a JSON object"""
    try:
        with open(data_file, "rb") as file:
            data = json.load(file)
            file.close()
            return data
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

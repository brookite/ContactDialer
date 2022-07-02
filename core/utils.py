import os


def get_filename(path: str) -> str:
    return os.path.split(path)[-1]

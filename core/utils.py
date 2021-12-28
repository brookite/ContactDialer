import os

def get_filename(path):
    return os.path.split(path)[-1]
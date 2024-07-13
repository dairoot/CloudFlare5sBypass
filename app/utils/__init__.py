import os


def check_path(file_path):
    if file_path and not os.path.exists(file_path):
        os.makedirs(file_path)

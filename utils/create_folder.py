import os


def create_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)

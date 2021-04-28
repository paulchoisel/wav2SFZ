import os


def isFile(path):
    if os.path.isfile(path):
        return path
    raise ValueError('The given path does not lead to a file.')

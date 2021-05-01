import os


def isFile(path):
    if os.path.isfile(path):
        return path
    raise ValueError('The given path does not lead to a file.')


def isWriteableDirectory(path):
    if os.access(path, os.W_OK):
        return path
    raise ValueError('The given path does not lead to a writeable file/folder.')
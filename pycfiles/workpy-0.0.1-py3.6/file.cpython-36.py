# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\workpy\file.py
# Compiled at: 2019-08-10 00:30:46
# Size of source mod 2**32: 476 bytes
from .base import *

def home(a='', *b):
    return (os.path.join)(os.path.expanduser('~'), a, *b).rstrip('\\')


def desktop(a='', *b):
    return home('Desktop', a, *b)


def mkdir(path):
    if os.path.exists(path):
        print(f"{path} exists! continue.")
        return
    os.makedirs(path.strip().rstrip('\\'))
    print(f"{path} created.")


def rmdir(path):
    if os.path.exists(path):
        os.removedirs(path)
        print(f"{path} deleted.")


if __name__ == '__main__':
    print(home())
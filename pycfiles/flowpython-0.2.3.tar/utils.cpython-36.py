# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/misakawa/Doc/flowpython/flowpython/flowpy_switcher/utils.py
# Compiled at: 2017-08-18 13:47:58
# Size of source mod 2**32: 565 bytes
import os

def makedir_from(file):
    try:
        return os.path.split(file)[0]
    except:
        pass


def bin_copyto(file_from, file_to):
    if not os.path.exists(file_from):
        raise BaseException(f"{file_from} not exists!")
    print(f"writing {file_from} to {file_to}...")
    with open(file_to, 'wb') as (_to):
        with open(file_from, 'rb') as (_from):
            _to.write(_from.read())


def moveto(file_from, file_to):
    if not os.path.exists(file_from):
        raise BaseException(f"{file_from} not exists!")
    print(f"moving {file_from} to {file_to}...")
    os.rename(file_from, file_to)
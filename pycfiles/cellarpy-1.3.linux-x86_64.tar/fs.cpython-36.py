# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doomsday/git/cellarpy/venv/lib/python3.6/site-packages/cellar/fs.py
# Compiled at: 2017-10-03 06:24:58
# Size of source mod 2**32: 703 bytes
import os

def iswritable(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            return False

    return os.access(directory, os.W_OK | os.X_OK | os.R_OK)


def static_file_path(root, filename):
    root = os.path.abspath(root) + os.sep
    return os.path.abspath(os.path.join(root, filename.strip('/\\')))


def static_file_exists(root, filename):
    root = os.path.abspath(root) + os.sep
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    if not filename.startswith(root):
        return False
    else:
        if not os.path.exists(filename) or not os.path.isfile(filename):
            return False
        return True
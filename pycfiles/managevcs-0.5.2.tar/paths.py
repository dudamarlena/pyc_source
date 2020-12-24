# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/vcs/utils/paths.py
# Compiled at: 2015-05-15 06:06:58
import os
abspath = lambda *p: os.path.abspath(os.path.join(*p))

def get_dirs_for_path(*paths):
    """
    Returns list of directories, including intermediate.
    """
    for path in paths:
        head = path
        while head:
            head, tail = os.path.split(head)
            if head:
                yield head
            else:
                break


def get_dir_size(path):
    root_path = path
    size = 0
    for path, dirs, files in os.walk(root_path):
        for f in files:
            try:
                size += os.path.getsize(os.path.join(path, f))
            except OSError:
                pass

    return size


def get_user_home():
    """
    Returns home path of the user.
    """
    return os.getenv('HOME', os.getenv('USERPROFILE')) or ''
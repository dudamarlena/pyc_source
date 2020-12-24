# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pirx/utils.py
# Compiled at: 2013-12-06 18:51:18
import os

def setting(name):
    return name.upper()


def path(subpath):
    import __main__
    project_root = os.path.dirname(os.path.realpath(__main__.__file__))
    return os.path.join(project_root, subpath)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: microdrop\__init__.py
# Compiled at: 2015-10-23 13:16:51
from path_helpers import path

def base_path():
    return path(__file__).abspath().parent


def glade_path():
    """
    Return path to `.glade` files used by `gtk` to construct views.
    """
    return base_path().joinpath('gui', 'glade')
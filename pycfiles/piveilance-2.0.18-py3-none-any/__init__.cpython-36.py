# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\Repositories\carag\piveilance\piveilance\resources\__init__.py
# Compiled at: 2019-12-14 03:10:44
# Size of source mod 2**32: 431 bytes
import os, sys
from os.path import dirname, realpath, join
__name__ = dirname(__file__).split(os.sep)[(-1)]

def get_resource_dir():
    if getattr(sys, 'frozen', False):
        return join(sys._MEIPASS, __name__)
    else:
        return dirname(realpath(__file__))


def get_resource(name):
    return join(get_resource_dir(), name)


def get_image(name):
    return join(get_resource_dir(), 'image', name)
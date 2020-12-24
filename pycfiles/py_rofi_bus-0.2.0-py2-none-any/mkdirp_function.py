# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjharries/Code/@wizardsoftheweb/py-rofi-bus/py_rofi_bus/utils/mkdirp_function.py
# Compiled at: 2018-06-02 23:19:31
from errno import EEXIST
from os import makedirs
from os.path import isdir

def mkdirp(directory=None):
    if directory:
        try:
            makedirs(directory)
        except OSError as error:
            if EEXIST == error.errno and isdir(directory):
                pass
            else:
                raise
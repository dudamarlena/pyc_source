# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/envconf.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 186 bytes
from os import environ

def envconf(srcdict):
    newdict = {}
    for k, v in srcdict.items():
        if k in environ.keys():
            newdict[v] = environ[k]

    return newdict
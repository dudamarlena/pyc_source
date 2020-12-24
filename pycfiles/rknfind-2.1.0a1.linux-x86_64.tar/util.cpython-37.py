# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scpketer/Dev/rknfind/.env/lib/python3.7/site-packages/rknfind/util.py
# Compiled at: 2019-09-18 12:37:20
# Size of source mod 2**32: 41 bytes


def json(obj):
    return obj.__json__()
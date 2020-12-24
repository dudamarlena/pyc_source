# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nekos\dict.py
# Compiled at: 2018-05-15 13:23:12
# Size of source mod 2**32: 164 bytes


class JsonDict:

    def __init__(self, my_dict: dict):
        self._dict = my_dict

    def __getattr__(self, key):
        return self._dict.get(key, None)
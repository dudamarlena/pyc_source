# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/models/Cipher.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 304 bytes
from json import loads as json_loads

class Cipher:
    iv: str
    data: str
    json: dict
    enc: str

    def __init__(self, json_string):
        self.json = json_loads(json_string)
        self.iv = self.json['iv']
        self.data = self.json['data']
        self.enc = self.json['enc']
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/OnePasswordResult.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 278 bytes
import onepassword_local_search.models.Item as Item

class OnePasswordResult(Item):
    overview: str
    details: str
    uuid: str
    vaultUuid: str

    def __init__(self, response):
        for attr in response.keys():
            setattr(self, attr, response[attr])
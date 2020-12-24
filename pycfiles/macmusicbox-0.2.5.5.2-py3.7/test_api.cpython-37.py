# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/w3/yc8mtbd91vs80rp79zfgk8x00000gn/T/pip-install-aqb0355v/NetEase-MusicBox/NEMbox/tests/test_api.py
# Compiled at: 2020-03-01 00:57:53
# Size of source mod 2**32: 1302 bytes
from hashlib import md5
import unittest
from NEMbox.api import NetEase, Parse

class TestApi(unittest.TestCase):

    def test_api(self):
        api = NetEase()
        ids = [347230, 496619464, 405998841, 28012031]
        print(api.songs_url(ids))
        print(api.songs_detail(ids))
        print(Parse.song_url(api.songs_detail(ids)[0]))
        print(api.songs_url([561307346]))
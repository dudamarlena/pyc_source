# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyotify\main.py
# Compiled at: 2020-02-21 17:48:56
# Size of source mod 2**32: 232 bytes
from pyotify import Spotify
import json, os
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
sp = Spotify(client_id, client_secret)
print(json.dumps(response, indent=4, sort_keys=True))
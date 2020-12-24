# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyotify\main.py
# Compiled at: 2020-02-21 17:48:56
# Size of source mod 2**32: 232 bytes
from pyotify import Spotify
import json, os
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
sp = Spotify(client_id, client_secret)
print(json.dumps(response, indent=4, sort_keys=True))
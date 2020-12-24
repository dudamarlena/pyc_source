# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./client.py
# Compiled at: 2019-03-06 08:24:52
# Size of source mod 2**32: 693 bytes
from pystrava import Strava
import os

class Client:

    def __init__(self):
        self._strava = None

    @property
    def strava(self):
        if not self._strava:
            self._strava = Strava(client_id=(os.environ['CLIENT_ID']), client_secret=(os.environ['SECRET']),
              callback=(os.environ['CALLBACK_URL']),
              scope=(os.environ['SCOPE']),
              email=(os.environ['EMAIL']),
              password=(os.environ['PASSWORD']))
        return self._strava

    @property
    def activities(self):
        return self.strava.get_activities(limit=500)
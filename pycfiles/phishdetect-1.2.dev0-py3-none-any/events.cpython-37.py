# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/models/events.py
# Compiled at: 2020-01-02 09:24:20
# Size of source mod 2**32: 655 bytes
from .model import Model
from ..endpoints import API_PATH

class Events(Model):

    def fetch(self, limit=0, offset=0):
        """Fetch all events stored by PhishDetect Node.
        :param limit: Set an integer to use as limit of records to retrieve.
        :param offset: Set an integer to use as offset of records to retrieve.
        """
        params = {'limit':limit, 
         'offset':offset}
        return self._phishdetect.get((API_PATH['events_fetch']), params=params)
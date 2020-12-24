# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/models/raw.py
# Compiled at: 2019-12-26 02:25:33
# Size of source mod 2**32: 749 bytes
from .model import Model
from ..endpoints import API_PATH

class Raw(Model):

    def fetch(self, limit=0, offset=0):
        """Fetch all raw messages stored by PhishDetect Node.
        :param limit: Set an integer to use as limit of records to retrieve.
        :param offset: Set an integer to use as offset of records to retrieve.
        """
        params = {'limit':limit, 
         'offset':offset}
        return self._phishdetect.get((API_PATH['raw_fetch']), params=params)

    def details(self, uuid):
        """Get details of a raw message, including content.
        :param uuid: Identifier of the message to fetch.
        """
        return self._phishdetect.get(API_PATH['raw_details'].format(uuid=uuid))
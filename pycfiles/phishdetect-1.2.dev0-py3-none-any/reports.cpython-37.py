# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/models/reports.py
# Compiled at: 2019-12-26 11:47:17
# Size of source mod 2**32: 945 bytes
from .model import Model
from ..endpoints import API_PATH

class Reports(Model):

    def fetch(self, limit=0, offset=0, report_type=''):
        """Fetch all reports stored by PhishDetect Node.
        :param limit: Set an integer to use as limit of records to retrieve.
        :param offset: Set an integer to use as offset of records to retrieve.
        """
        params = {'limit':limit, 
         'offset':offset, 
         'type':report_type}
        return self._phishdetect.get((API_PATH['reports_fetch']), params=params)

    def details(self, uuid):
        """Get details of a report, including content.
        :param uuid: Identifier of the message to fetch.
        """
        return self._phishdetect.get(API_PATH['reports_details'].format(uuid=uuid))
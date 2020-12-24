# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/models/indicators.py
# Compiled at: 2019-12-26 17:49:10
# Size of source mod 2**32: 1629 bytes
from .model import Model
from ..endpoints import API_PATH

class Indicators(Model):

    def add(self, indicators, indicators_type, tags=[]):
        """Add new indicators to PhishDetect Node.
        :param indicators: list of indicators, e.g. ["domain1.com", "domain2.com"].
        :param indicators_type: the indicator format, e.g.: "domain" or "email".
        :param tags: List of tags to assign to all these indicators.
        """
        json = {'indicators':indicators, 
         'type':indicators_type, 
         'tags':tags}
        return self._phishdetect.post((API_PATH['indicators_add']), json=json)

    def fetch(self):
        """Fetch the default set of indicators (should be, from last 6 months.)
        """
        return self._phishdetect.get(API_PATH['indicators_fetch'])

    def fetch_recent(self):
        """Fetch only the indicators from the last 24 hours.
        """
        return self._phishdetect.get(API_PATH['indicators_fetch_recent'])

    def fetch_all(self):
        """Fetch all the indicators stored in the Node.
        This API should be avoided unless strictly necessary.
        """
        return self._phishdetect.get(API_PATH['indicators_fetch_all'])

    def details(self, sha256):
        """Retrieve details on a given indicator (by hash).
        :param sha256: SHA256 hash of the indicator.
        """
        return self._phishdetect.get(API_PATH['indicators_details'].format(sha256=sha256))
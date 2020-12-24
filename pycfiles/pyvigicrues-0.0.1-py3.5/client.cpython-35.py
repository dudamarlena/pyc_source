# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyvigicrues/client.py
# Compiled at: 2019-01-01 19:33:18
# Size of source mod 2**32: 1223 bytes
import requests, json, datetime
VIGICRUES_OBS_URL = 'https://www.vigicrues.gouv.fr/services/observations.json/index.php'

class PyVigicruesError(Exception):
    pass


class VigicruesClient(object):

    def __init__(self, stationid, type, timeout=None):
        """Initialize the client object."""
        self.stationid = stationid
        self.type = type
        self._timeout = timeout

    def get_data(self):
        """Get data."""
        try:
            payload = {'CdStationHydro': self.stationid, 'GrdSerie': self.type, 'FormatSortie': 'json'}
            headers = {'content-type': 'application/json'}
            raw_data = requests.get(VIGICRUES_OBS_URL, params=payload, headers=headers, allow_redirects=False, timeout=self._timeout)
        except OSError:
            raise PyVigicruesError('Can not get data')

        try:
            json_output = raw_data.json()
            return json_output
        except (OSError, json.decoder.JSONDecodeError):
            raise PyVigicruesError('Could not get data')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/abenkevich/defender/alertlogic-cli/alertlogic/region.py
# Compiled at: 2019-02-11 11:11:42
"""
    alertlogic.region
    ~~~~~~~~~~~~~~
    alertlogic region management
"""
REGIONS = {'us': 'https://api.cloudinsight.alertlogic.com', 
   'uk': 'https://api.cloudinsight.alertlogic.co.uk'}

class Region:
    """
    Abstracts an alertlogic region, for now it only represents the api endpoint url
    """

    def __init__(self, api_endpoint):
        """
        :param api_endpint: either a region ("us" or "uk") or an insight api url
        """
        self._api_endpoint = api_endpoint

    def get_api_endpoint(self):
        """
        returns the region's api endpoint url
        """
        if self._api_endpoint in REGIONS:
            return REGIONS[self._api_endpoint]
        else:
            return self._api_endpoint
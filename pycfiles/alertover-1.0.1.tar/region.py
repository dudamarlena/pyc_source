# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/abenkevich/defender/alertlogic-cli/alertlogic/region.py
# Compiled at: 2019-02-11 11:11:42
__doc__ = '\n    alertlogic.region\n    ~~~~~~~~~~~~~~\n    alertlogic region management\n'
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
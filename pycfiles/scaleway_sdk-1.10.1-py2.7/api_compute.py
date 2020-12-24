# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/scaleway/apis/api_compute.py
# Compiled at: 2019-12-16 08:49:55
from . import API
REGIONS = {'par1': {'url': 'https://cp-par1.scaleway.com/'}, 
   'ams1': {'url': 'https://cp-ams1.scaleway.com/'}}

class ComputeAPI(API):
    """ The default region is par1 as it was the first availability zone
    provided by Scaleway, but it could change in the future.
    """

    def __init__(self, **kwargs):
        region = kwargs.pop('region', None)
        base_url = kwargs.pop('base_url', None)
        assert region is None or base_url is None, 'Specify either region or base_url, not both.'
        if base_url is None:
            region = region or 'par1'
            assert region in REGIONS, "'%s' is not a valid Scaleway region." % region
            base_url = REGIONS.get(region)['url']
        super(ComputeAPI, self).__init__(base_url=base_url, **kwargs)
        return
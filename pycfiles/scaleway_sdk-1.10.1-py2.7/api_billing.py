# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/scaleway/apis/api_billing.py
# Compiled at: 2019-12-16 08:49:55
from . import API

class BillingAPI(API):
    base_url = 'https://billing.scaleway.com'

    def __init__(self, **kwargs):
        base_url = kwargs.pop('base_url', BillingAPI.base_url)
        super(BillingAPI, self).__init__(base_url=base_url, **kwargs)
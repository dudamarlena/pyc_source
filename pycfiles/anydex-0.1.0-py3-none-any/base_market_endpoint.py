# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/restapi/base_market_endpoint.py
# Compiled at: 2019-05-25 07:28:23
from anydex.core.community import MarketCommunity
from ipv8.REST.base_endpoint import BaseEndpoint

class BaseMarketEndpoint(BaseEndpoint):
    """
    This class can be used as a base class for all Market community endpoints.
    """

    def __init__(self, session):
        BaseEndpoint.__init__(self)
        self.session = session

    def get_market_community(self):
        for overlay in self.session.overlays:
            if isinstance(overlay, MarketCommunity):
                return overlay

        raise RuntimeError('Market community not found!')
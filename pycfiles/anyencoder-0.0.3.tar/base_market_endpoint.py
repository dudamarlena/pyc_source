# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
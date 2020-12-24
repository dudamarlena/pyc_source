# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/restapi/state_endpoint.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import
import anydex.util.json_util as json
from anydex.core import VERSION
from anydex.restapi.base_market_endpoint import BaseMarketEndpoint

class StateEndpoint(BaseMarketEndpoint):
    """
    This class handles requests regarding the state of the dex.
    """

    def render_GET(self, request):
        return json.twisted_dumps({'version': VERSION})
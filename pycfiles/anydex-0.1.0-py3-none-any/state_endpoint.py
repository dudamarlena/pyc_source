# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
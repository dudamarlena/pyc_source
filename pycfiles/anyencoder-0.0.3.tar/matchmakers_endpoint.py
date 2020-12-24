# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/restapi/matchmakers_endpoint.py
# Compiled at: 2019-05-25 07:28:23
from __future__ import absolute_import
import anydex.util.json_util as json
from anydex.restapi.base_market_endpoint import BaseMarketEndpoint

class MatchmakersEndpoint(BaseMarketEndpoint):
    """
    This class handles requests regarding your known matchmakers in the market community.
    """

    def render_GET(self, request):
        """
        .. http:get:: /market/matchmakers

        A GET request to this endpoint will return all known matchmakers.

            **Example request**:

            .. sourcecode:: none

                curl -X GET http://localhost:8085/market/matchmakers

            **Example response**:

            .. sourcecode:: javascript

                {
                    "matchmakers": [{
                        "ip": "131.249.48.3",
                        "port": 7008
                    }]
                }
        """
        matchmakers = self.get_market_community().matchmakers
        matchmakers_json = [ {'ip': mm.address[0], 'port': mm.address[1]} for mm in matchmakers ]
        return json.twisted_dumps({'matchmakers': matchmakers_json})
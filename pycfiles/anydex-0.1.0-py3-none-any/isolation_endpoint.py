# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/../pyipv8/ipv8/REST/isolation_endpoint.py
# Compiled at: 2019-06-07 08:10:38
from __future__ import absolute_import
from twisted.web import http
from .base_endpoint import BaseEndpoint
from ..community import _DEFAULT_ADDRESSES
from ..messaging.anonymization.community import TunnelCommunity
from ..util import cast_to_chr

class IsolationEndpoint(BaseEndpoint):
    """
    This endpoint is responsible for on-demand adding of addresses for different services.

    We support:
     - POST: /isolation?ip=<IP>&port=<PORT>&bootstrapnode=1
     - POST: /isolation?ip=<IP>&port=<PORT>&exitnode=1

    These commands add a bootstrap node and an exit node respectively.
    The IP is a period-seperated string.
    An example call would be:

    curl -X POST "http://localhost:8085/isolation?ip=127.0.0.1&port=9999&bootstrapnode=1"
    """

    def __init__(self, session):
        super(IsolationEndpoint, self).__init__()
        self.session = session

    def add_exit_node(self, address):
        for overlay in self.session.overlays:
            if isinstance(overlay, TunnelCommunity):
                overlay.walk_to(address)

    def add_bootstrap_server(self, address):
        _DEFAULT_ADDRESSES.append(address)
        for overlay in self.session.overlays:
            overlay.walk_to(address)

    def render_POST(self, request):
        if not request.args or 'ip' not in request.args or 'port' not in request.args:
            request.setResponseCode(http.BAD_REQUEST)
            return self.twisted_dumps({'success': False, 'error': "Parameters 'ip' and 'port' are required"})
        if 'exitnode' not in request.args and 'bootstrapnode' not in request.args:
            request.setResponseCode(http.BAD_REQUEST)
            return self.twisted_dumps({'success': False, 'error': "Parameter 'exitnode' or 'bootstrapnode' is required"})
        try:
            address_str = cast_to_chr(request.args['ip'][0])
            port_str = cast_to_chr(request.args['port'][0])
            fmt_address = (address_str, int(port_str))
        except:
            import traceback
            request.setResponseCode(http.BAD_REQUEST)
            return self.twisted_dumps({'success': False, 'error': traceback.format_exc()})

        if 'exitnode' in request.args:
            self.add_exit_node(fmt_address)
        else:
            self.add_bootstrap_server(fmt_address)
        return self.twisted_dumps({'success': True})
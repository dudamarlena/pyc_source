# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/op/endpoint_collection.py
# Compiled at: 2019-11-15 09:41:29
# Size of source mod 2**32: 376 bytes
from oidcendpoint.client_authn import CLIENT_AUTHN_METHOD
from oidcendpoint.util import build_endpoints

class EndpointCollection:

    def __init__(self, conf, **kwargs):
        self.endpoint = build_endpoints((conf['endpoint']),
          endpoint_context=self,
          client_authn_method=CLIENT_AUTHN_METHOD,
          issuer=(conf['issuer']))
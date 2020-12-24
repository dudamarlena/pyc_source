# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/redfox/request.py
# Compiled at: 2009-10-20 11:31:07
from werkzeug import Request as WerkzeugRequest, BaseRequest

class MapAdapterMixin(object):
    """A request mixin that exposes a Werkzeug MapAdapter and its operations."""

    def __init__(self, map_adapter):
        self.map_adapter = map_adapter

    def build_url(self, endpoint, values=None, method=None, force_external=False):
        """Delegates to ``MapAdapter.build``."""
        return self.map_adapter.build(endpoint=endpoint, values=values, method=method, force_external=force_external)

    def dispatch_url(self, view_func, path_info=None, method=None, catch_http_exceptions=False):
        """Delegates to ``MapAdapter.dispatch``."""
        return self.map_adapter.dispatch(view_func=view_func, path_info=path_info, method=method, catch_http_exceptions=catch_http_exceptions)

    def test_url(self, path_info=None, method=None):
        """Delegates to ``MapAdapter.test``."""
        return self.map_adapter.test(path_info=path_info, method=method)

    def match_url(self, path_info=None, method=None):
        """Delegates to ``MapAdapter.match``."""
        return self.map_adapter.match(path_info=path_info, method=method)


class Request(WerkzeugRequest, MapAdapterMixin):
    """A request type containing all of the types covered by
    ``werkzeug.Request`` as well as ``MapAdapterMixin`` from this
    module."""

    def __init__(self, map_adapter, *args, **kwargs):
        MapAdapterMixin.__init__(self, map_adapter)
        WerkzeugRequest.__init__(self, *args, **kwargs)
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_response.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 2745 bytes
from __future__ import absolute_import, unicode_literals
from werkzeug.wrappers import Request
from ..tools.response import redirect, redirect_obj

class TestRedirect(object):

    def test_redirect_respects_location(self):
        """Test that redirect returns a 302 to location specified."""
        request = Request({})
        response = redirect(request, location='/test')
        assert response.status_code == 302
        assert response.location == '/test'

    def test_redirect_respects_querystring(self):
        """Test that redirect includes querystring in returned location."""
        request = Request({})
        response = redirect(request, location='', querystring='#baz')
        assert response.location == '#baz'

    def test_redirect_respects_urlgen_args(self):
        """Test that redirect returns a 302 to location from urlgen args."""

        def urlgen(endpoint, **kwargs):
            return '/test?foo=bar'

        request = Request({})
        request.urlgen = urlgen
        response = redirect(request, 'test-endpoint', foo='bar')
        assert response.status_code == 302
        assert response.location == '/test?foo=bar'

    def test_redirect_obj_calls_url_for_self(self):
        """Test that redirect_obj returns a 302 to obj's url_for_self()."""

        class Foo(object):

            def url_for_self(*args, **kwargs):
                return '/foo'

        request = Request({})
        request.urlgen = None
        response = redirect_obj(request, Foo())
        assert response.status_code == 302
        assert response.location == '/foo'
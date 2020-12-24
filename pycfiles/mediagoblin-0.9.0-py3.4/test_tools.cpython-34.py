# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_tools.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 2530 bytes
from __future__ import absolute_import, unicode_literals
from werkzeug.wrappers import Request
from werkzeug.test import EnvironBuilder
from mediagoblin.tools.request import decode_request

class TestDecodeRequest(object):
    __doc__ = 'Test the decode_request function.'

    def test_form_type(self):
        """Try a normal form-urlencoded request."""
        builder = EnvironBuilder(method='POST', data={'foo': 'bar'})
        request = Request(builder.get_environ())
        data = decode_request(request)
        assert data['foo'] == 'bar'

    def test_json_type(self):
        """Try a normal JSON request."""
        builder = EnvironBuilder(method='POST', content_type='application/json', data='{"foo": "bar"}')
        request = Request(builder.get_environ())
        data = decode_request(request)
        assert data['foo'] == 'bar'

    def test_content_type_with_options(self):
        """Content-Type can also have options."""
        builder = EnvironBuilder(method='POST', content_type='application/x-www-form-urlencoded; charset=utf-8')
        request = Request(builder.get_environ())
        request.form = {'foo': 'bar'}
        data = decode_request(request)
        assert data['foo'] == 'bar'

    def test_form_type_is_default(self):
        """Assume form-urlencoded if blank in the request."""
        builder = EnvironBuilder(method='POST', content_type='')
        request = Request(builder.get_environ())
        request.form = {'foo': 'bar'}
        data = decode_request(request)
        assert data['foo'] == 'bar'
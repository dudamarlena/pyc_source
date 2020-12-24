# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fanart/tests/test_core.py
# Compiled at: 2019-03-12 04:24:44
# Size of source mod 2**32: 973 bytes
from unittest import TestCase
from fanart.core import Request
from fanart.errors import RequestFanartError, ResponseFanartError
from httpretty import httprettified, HTTPretty

class RequestTestCase(TestCase):

    def test_valitate_error(self):
        self.assertRaises(RequestFanartError, Request, 'key', 'id', 'sport')

    @httprettified
    def test_response_error(self):
        request = Request('apikey', 'objid', 'tv')
        HTTPretty.register_uri((HTTPretty.GET),
          'http://webservice.fanart.tv/v3/tv/objid?api_key=apikey',
          body='Please specify a valid API key')
        try:
            request.response()
        except ResponseFanartError as e:
            try:
                self.assertEqual(repr(e), "ResponseFanartError('Expecting value: line 1 column 1 (char 0)',)")
                self.assertEqual(str(e), 'Expecting value: line 1 column 1 (char 0)')
            finally:
                e = None
                del e
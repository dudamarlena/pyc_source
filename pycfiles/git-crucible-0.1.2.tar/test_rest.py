# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joshbraegger/bc/git-crucible/crucible/tests/test_rest.py
# Compiled at: 2012-03-23 23:13:27
from mock import patch, MagicMock
from crucible import rest
import unittest

class TestRest(unittest.TestCase):

    @patch('crucible.rest.urllib2')
    def test_request(self, urllib2_mock):
        headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml', 
           'Authorization': 'Basic amltOmJvYg=='}
        rest.request('http://localhost/', 'POST', 'body', username='jim', password='bob')
        urllib2_mock.Request.assert_called_once_with(url='http://localhost/', data='body', headers=headers)
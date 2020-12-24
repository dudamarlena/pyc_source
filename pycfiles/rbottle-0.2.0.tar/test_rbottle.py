# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: test_rbottle.py
# Compiled at: 2014-11-30 01:15:35
import sys
from StringIO import StringIO
sys.path.append('../src/')
import pytest, rbottle

class MockRequest:

    def __init__(self, json):
        self.body = StringIO(json)


def test_decode_json_body():
    request = MockRequest("{'hello': 'there'}")
    rbottle.request = request
    reload(rbottle)
    assert rbottle.decode_json_body() == {'hello': 'there'}
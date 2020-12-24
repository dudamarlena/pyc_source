# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-hdcloud/tests/test_exceptions.py
# Compiled at: 2010-04-14 13:49:55
from __future__ import absolute_import
import mock, hdcloud.exceptions
from nose.tools import assert_equal
from .utils import assert_isinstance

def test_exception_from_response():
    resp = mock.Mock()
    resp.status = 500
    exc = hdcloud.exceptions.from_response(resp, {'errors': [{'message': 'Oops!'}]})
    assert_isinstance(exc, hdcloud.exceptions.HDCloudException)
    assert_equal(str(exc), 'Oops! (HTTP 500)')


def test_exception_from_response_no_body():
    resp = mock.Mock()
    resp.status = 500
    exc = hdcloud.exceptions.from_response(resp, None)
    assert_equal(str(exc), 'HDCloudException (HTTP 500)')
    return
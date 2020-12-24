# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smorin/Dropbox/code/dedup/filegardener/test_data/1dup/seconddir/tests/conftest.py
# Compiled at: 2016-07-21 23:59:52
import pytest
from requests.compat import urljoin

def prepare_url(value):
    httpbin_url = value.url.rstrip('/') + '/'

    def inner(*suffix):
        return urljoin(httpbin_url, ('/').join(suffix))

    return inner


@pytest.fixture
def httpbin(httpbin):
    return prepare_url(httpbin)


@pytest.fixture
def httpbin_secure(httpbin_secure):
    return prepare_url(httpbin_secure)
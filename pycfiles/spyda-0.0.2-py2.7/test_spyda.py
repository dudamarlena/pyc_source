# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/tests/test_spyda.py
# Compiled at: 2013-06-24 00:59:24
import pytest
from spyda.utils import fetch_url, get_links
from .helpers import urljoin
SAMPLE_CONTENT = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n\n<html xmlns="http://www.w3.org/1999/xhtml">\n\n<head>\n <title>/</title>\n</head>\n\n<body>\n <p>Hello World!</p>\n <p><a href=".">.</a></p>\n <p><a href="..">..</a></p>\n <p><a href="foo/">foo/</a></p>\n <p>\n  Test suite created by\n  <a href="mailto:foo@bar.com">\n   Foo Bar, foo at bar dot com\n  </a>\n </p>\n</body>\n</html>\n'
SAMPLE_LINKS = [
 '.', '..', 'foo/', 'mailto:foo@bar.com']

@pytest.fixture()
def sample_content():
    return SAMPLE_CONTENT


@pytest.fixture()
def sample_links():
    return SAMPLE_LINKS


def test_fetch_url(webapp):
    res, data = fetch_url(urljoin(webapp.server.base, 'hello'))
    assert res.status == 200
    assert data == 'Hello World!'


def test_fetch_url_unicode(webapp):
    res, data = fetch_url(urljoin(webapp.server.base, 'unicode'))
    assert res.status == 200
    assert data == 'Hello World!'


def test_get_links(sample_content, sample_links):
    actual_links = list(get_links(sample_content))
    assert actual_links == sample_links
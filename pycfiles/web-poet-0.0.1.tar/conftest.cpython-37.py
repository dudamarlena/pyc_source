# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victortorres/git/shub/core-po/tests/conftest.py
# Compiled at: 2020-04-27 10:50:12
# Size of source mod 2**32: 428 bytes
import os, pytest
from web_poet.page_inputs import ResponseData

def read_fixture(path):
    path = os.path.join(os.path.dirname(__file__), path)
    with open(path) as (f):
        return f.read()


@pytest.fixture
def book_list_html():
    return read_fixture('fixtures/book_list.html')


@pytest.fixture
def book_list_html_response(book_list_html):
    return ResponseData('http://book.toscrape.com/', book_list_html)
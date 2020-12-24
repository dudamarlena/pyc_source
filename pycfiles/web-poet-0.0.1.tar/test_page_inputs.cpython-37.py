# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victortorres/git/shub/core-po/tests/test_page_inputs.py
# Compiled at: 2020-04-27 10:50:12
# Size of source mod 2**32: 191 bytes
from web_poet.page_inputs import ResponseData

def test_html_response():
    response = ResponseData('url', 'content')
    assert response.url == 'url'
    assert response.html == 'content'
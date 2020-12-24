# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/util/formatter/html_reader_lxml.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 359 bytes
from lxml import html
HTMLNode = html.HtmlElement

def read_html(data: str) -> HTMLNode:
    return html.fromstring(data)
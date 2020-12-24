# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reddit2ebook/ebooklib_patched/utils.py
# Compiled at: 2016-05-13 06:16:04
# Size of source mod 2**32: 1224 bytes
import io
from lxml import etree

def debug(obj):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(obj)


def parse_string(s):
    try:
        tree = etree.parse(io.BytesIO(s.encode('utf-8')))
    except:
        tree = etree.parse(io.BytesIO(s))

    return tree


def parse_html_string(s):
    from lxml import html
    utf8_parser = html.HTMLParser(encoding='utf-8')
    html_tree = html.document_fromstring(s, parser=utf8_parser)
    return html_tree
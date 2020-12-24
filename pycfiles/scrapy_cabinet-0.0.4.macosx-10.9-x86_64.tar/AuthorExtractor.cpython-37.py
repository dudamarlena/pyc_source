# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/libs/gne/extractor/AuthorExtractor.py
# Compiled at: 2019-11-07 04:07:05
# Size of source mod 2**32: 475 bytes
import re
from lxml.html import HtmlElement
from scrapy_cabinet.libs.defaults import AUTHOR_PATTERN

class AuthorExtractor:

    def __init__(self):
        self.author_pattern = AUTHOR_PATTERN

    def extractor(self, element: HtmlElement):
        text = ''.join(element.xpath('.//text()'))
        for pattern in self.author_pattern:
            author_obj = re.search(pattern, text)
            if author_obj:
                return author_obj.group(1)

        return ''
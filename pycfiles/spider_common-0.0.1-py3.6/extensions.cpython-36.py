# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider_common/clue/scrapy/extensions.py
# Compiled at: 2019-04-16 05:50:15
# Size of source mod 2**32: 234 bytes
from ..api import ClueApi

class ClueApiExtension:
    __doc__ = '\n    do ClueApi initialization\n    '

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        ClueApi(api=(settings.get('CLUE_API')))
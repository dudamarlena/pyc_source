# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\implements\ip.py
# Compiled at: 2018-03-10 15:11:33
# Size of source mod 2**32: 391 bytes
from ..core import ItemProcessor
__all__ = ['LogIP', 'CountItemIP']

class LogIP(ItemProcessor):

    async def process(self, item):
        self.saver.logger.info(str(item))


class CountItemIP(ItemProcessor):

    async def process(self, item):
        c = self.saver.runtime_data.setdefault('item_count', 0)
        c += 1
        self.saver.runtime_data['item_count'] = c
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\core\processor.py
# Compiled at: 2018-03-10 13:44:21
# Size of source mod 2**32: 913 bytes
from .fetsav import Fetcher, Saver
from .reqrep import Request
from .item import Item
import weakref
__all__ = ['RequestProcessor', 'ItemProcessor']

class BaseProcessor:

    def on_start(self):
        pass

    def on_stop(self):
        pass

    async def process(self, value):
        pass


class RequestProcessor(BaseProcessor):

    def __init__(self, fetcher):
        BaseProcessor.__init__(self)
        self._fetcher = weakref.proxy(fetcher)

    @property
    def fetcher(self) -> Fetcher:
        return self._fetcher

    async def process(self, request: Request):
        pass


class ItemProcessor(BaseProcessor):

    def __init__(self, saver):
        BaseProcessor.__init__(self)
        self._saver = weakref.proxy(saver)

    @property
    def saver(self) -> Saver:
        return self._saver

    async def process(self, item: Item):
        pass
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\implements\item.py
# Compiled at: 2018-03-10 15:31:10
# Size of source mod 2**32: 333 bytes
from ..core import Item, Field, Spider
__all__ = ['ImageItem']

class ImageItem(Item):
    url = Field()
    content = Field()

    @classmethod
    async def load(cls, spider: Spider, img_url, **kwargs):
        resp = await (spider.fetch)('get', img_url, **kwargs)
        return cls(url=(resp.url), content=(resp.content))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sogubaby/.virtualenvs/scrapy_middlewares/lib/python3.7/site-packages/scrapy_cabinet/types.py
# Compiled at: 2019-11-07 01:23:44
# Size of source mod 2**32: 548 bytes
from typing import Union, Sequence, AnyStr, Dict, Iterator
from scrapy import Spider, Request, Item
from scrapy.crawler import Crawler
from scrapy.http import Response
from scrapy_redis.spiders import RedisSpider
_Proxies = Union[(Sequence[AnyStr], AnyStr)]
_Crawler = Crawler
_Spider = Union[(Spider, RedisSpider)]
_Request = Request
_Response = Response
_Item = Item
_Result = Iterator[Union[(_Request, Dict, _Item)]]
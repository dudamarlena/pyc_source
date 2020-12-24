# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/cached_spider.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 337 bytes
from tzutil.cached_req import Req
from tzutil.spider import Spider

class CachedSpider(Spider):

    def __init__(self, path, expire=None, vaild=lambda html: 1, *args, **kwds):
        (super(CachedSpider, self).__init__)(*args, **kwds)
        self._get = Req(path, expire, vaild).async_get
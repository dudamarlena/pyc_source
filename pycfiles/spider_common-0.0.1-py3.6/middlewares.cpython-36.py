# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider_common/clue/scrapy/middlewares.py
# Compiled at: 2019-04-16 05:50:15
# Size of source mod 2**32: 693 bytes
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from ..api import ClueApi

class ClueRetryMiddleware(RetryMiddleware):

    def __init__(self, settings):
        super().__init__(settings)
        self.api = ClueApi()

    def _retry(self, request, reason, spider):
        ret = super()._retry(request, reason, spider)
        if ret:
            return ret
        clue_id = request.meta.get('clue_id')
        if clue_id:
            clue = self.api.get_by_id(clue_id)
            if clue['status'] == 200:
                spider.debug('!!!retry a successful clue!!!')
            else:
                clue.fail()
                self.api.update(clue)
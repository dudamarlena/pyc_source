# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/middlewares/retry.py
# Compiled at: 2018-09-05 23:09:36
import traceback, logging
from scrapy_redis import connection
from scrapy.downloadermiddlewares.retry import RetryMiddleware
logger = logging.getLogger(__name__)

class retryToStartMiddleware(RetryMiddleware):
    """

    [请求失败后被重置是放在队尾，也就是 rpush]
    """

    def __init__(self, settings):
        super(retryToStartMiddleware, self).__init__(settings)
        self.server = connection.from_settings(settings)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= self.max_retry_times:
            logger.debug('Retrying %(request)s (failed %(retries)d times): %(reason)s', {'request': request, 'retries': retries, 'reason': reason}, extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            logger.debug('Gave up retrying %(request)s (failed %(retries)d times): %(reason)s', {'request': request, 'retries': retries, 'reason': reason}, extra={'spider': spider})
            msg = traceback.format_exc(reason)
            easyspider = request.meta.get('easyspider') or {}
            if not easyspider:
                request.meta['easyspider'] = {'from_retry': 999}
            else:
                request.meta['easyspider']['from_retry'] = 999
            spider.put_back_2_start_url(request, exc_info={'request': request.url, 
               'traceback': msg, 
               'body': None})
            return
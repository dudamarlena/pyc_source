# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/core/easyscheduler.py
# Compiled at: 2018-03-18 08:01:29
import logging
from scrapy_redis.scheduler import Scheduler
from twisted.internet.threads import deferToThread
logger = logging.getLogger(__name__)

class easyScheduler(Scheduler):

    def has_pending_requests(self):
        """in this method, you should only return True regardless what len(self) is

        because in a extreme case, spider machine may lost connection with the redis
        (ADSL dailing interval or even worse case: the ADSL interface had crush down and must reboot to resume),

        if can not connect to redis, len(self) will casuse Exception, because of the Exception, crawler can not
        run into next_request, and run into a useless loop, never require more request from redis anymore(because next_requsts not called)
        """
        try:
            return len(self) > 0
        except Exception:
            logger.exception('in easyScheduler: check has_pending_requests,  len(self) failed, return false')
            return False

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        return deferToThread(self.defer_push, request)

    def defer_push(self, request):
        while True:
            try:
                self.queue.push(request)
                return True
            except Exception:
                logger.exception('in easyScheduler: enqueue_request,  self.queue.push(request) failed, return True %s' % request)
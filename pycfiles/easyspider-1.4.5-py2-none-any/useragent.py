# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/middlewares/useragent.py
# Compiled at: 2017-08-24 09:47:41
from easyspider.utils.userAgentList import UA_headers
import random

class userAgentMiddleware(object):

    def process_request(self, request, spider):
        this_time_ua = random.choice(UA_headers)
        if this_time_ua:
            request.headers.setdefault('User-Agent', this_time_ua['User-Agent'])
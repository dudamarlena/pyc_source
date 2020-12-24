# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/pipelines/pipelines.py
# Compiled at: 2017-09-08 23:28:21
from datetime import datetime
from easyspider.utils.tools import get_time
import socket
flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) or isinstance(L, tuple) else [L]

class ExamplePipeline(object):

    def process_item(self, item, spider):
        item['crawled_time'] = get_time()
        item['spider'] = spider.name
        item['crawled_server'] = (';').join(flat(socket.gethostbyname_ex(socket.gethostname())))
        return item
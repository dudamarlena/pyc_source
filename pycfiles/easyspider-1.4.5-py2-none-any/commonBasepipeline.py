# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/pipelines/commonBasepipeline.py
# Compiled at: 2018-03-18 08:45:55
from easyspider.pipelines.commonpipeline import commonpipeline
from easyspider.utils.tools import get_time
import socket
flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) or isinstance(L, tuple) else [L]

class commonBasepipeline(commonpipeline):

    def _process_item(self, item, spider, response):
        item['crawled_time'] = get_time()
        item['spider'] = spider.name
        try:
            item['crawled_server'] = (';').join(flat(socket.gethostbyname_ex(socket.gethostname())))
        except Exception:
            item['crawled_server'] = socket.gethostname()

        return item
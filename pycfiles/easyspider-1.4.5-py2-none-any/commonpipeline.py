# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/pipelines/commonpipeline.py
# Compiled at: 2018-03-19 09:49:49
import json
from scrapy.utils.request import referer_str
from twisted.internet.threads import deferToThread

class commonpipeline(object):
    """通过继承 commonpipeline 来保证

    1. pipeline 是异步同时进行的
    2. 一旦出错，能及时汇报上去，汇报到 failed_urls

    注意, commonpipeline 调用的都是 _process_item  前面有一个 _ 下划线
    """

    def process_item(self, item, spider, response):
        d = deferToThread(self._process_item, item, spider, response)

        def error_back(err):
            r_copy = response.copy()
            if 'easyspider' not in r_copy.request.meta:
                r_copy.request.meta['easyspider'] = {}
            r_copy.request.meta['easyspider']['from_retry'] = 9999
            msg = {'request': '%(request)s (referer: %(referer)s)' % {'request': response.request, 'referer': referer_str(response.request)}, 
               'body': spider.get_unicode_response_body(response), 
               'traceback': 'Error processing %s ; %s' % (json.dumps(item), err.getTraceback())}
            spider.put_back_2_start_url(r_copy, exc_info=msg)
            return item

        d.addErrback(error_back)
        return d
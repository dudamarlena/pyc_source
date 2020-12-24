# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/spiders/easyCrawlSpider.py
# Compiled at: 2018-09-05 23:25:25
from scrapy_redis.spiders import RedisCrawlSpider
from easyspider.utils.tools import get_time
from easyspider.utils.tools import flat
from scrapy.http import Response
from bs4 import UnicodeDammit
from scrapy import Request
import traceback, urlparse, urllib, socket, time, json, copy

class easyCrawlSpider(RedisCrawlSpider):
    """所有爬虫最全的基类
    提供了一系列优秀简便的方法，来使编码过程更加友好快捷
    base spider of easyspider
    have provied multi useful method to make crawler more easier
    """
    name = 'easyCrawlSpider'
    start_key = 'start_urls'
    priority_start_key = 'priority_start_urls'
    successed_key = 'successed_urls'
    failed_key = 'failed_urls'
    retry_max_time = 1
    fetch_unit = 16
    fetch_from_redis_method = lambda self, server: server.rpop
    save_into_redis_method = lambda self, server: server.lpush
    fetch_from_priority_queue = lambda self, server, key_name, fetch_unit: server.zrevrangebyscore(key_name, float('inf'), float('-inf'), 0, fetch_unit)
    delete_from_priority_queue = lambda self, server, key_name, val: server.zrem(key_name, val)
    save_into_priority_queue = lambda self, server, key_name, val, data: server.zadd(key_name, val, data)

    def next_requests(self):
        u"""
        整个的心跳函数
        heartbeat of engine, called every 5s, to generate new request in crawler process

        next_requests will [r]pop the spider_name:start_key list queue from redis (attention, operation is lpop,
        so when you need to push into redis, you should use lpush instead)
        """
        count = 0
        while count < self.fetch_unit:
            try:
                start_map = self.fetch_from_priority_queue(self.server, '%s:%s' % (self.name, self.priority_start_key), 1)
                if start_map:
                    start_map = start_map[0]
                    self.delete_from_priority_queue(self.server, '%s:%s' % (self.name, self.priority_start_key), start_map)
                else:
                    start_map = self.fetch_from_redis_method(self.server)('%s:%s' % (self.name, self.start_key))
            except Exception:
                self.logger.exception('in easyCrawlSpider: next_requests,  start_map = self.fetch_from_redis_method(self.server)(u"%s:%s" % (self.name, self.start_key)) failed, continue')
                count += 1
                continue

            req = self.convert_startmap_2_request(start_map)
            if isinstance(req, Request):
                yield req
                count += 1
            else:
                break

        self.logger.debug("Read %s requests from '%s:%s'" % (count, self.name, self.start_key))

    def convert_startmap_2_request(self, start_map):
        u"""爬虫任务的解析函数。redis 中存储的任务，及任务附带的信息，在这里被解码，从而
        真正提交到引擎去执行抓取。
        注意这个解析是非常复杂的，涉及了非常多的方面。
        """
        if not start_map:
            return
        else:
            try:
                start_map = json.loads(start_map)
            except Exception:
                self.logger.exception('convert start url -> dict failed, start_map source is %s' % start_map)

            try:
                if not start_map.get('dont_filter'):
                    from_retry = int(start_map.get('easyspider', {}).get('from_retry', 0))
                    if from_retry > 0:
                        close_filter = True
                    else:
                        close_filter = False
                elif start_map.get('dont_filter') in ['True', 'true', True]:
                    close_filter = True
                else:
                    close_filter = False
                callback_fun = start_map.get('callback') or 'self.parse'
                req_callback_method = eval(callback_fun)
                req_url = start_map.get('url')
                req_method = start_map.get('method') or 'GET'
                req_headers = start_map.get('headers') or {}
                req_cookies = start_map.get('cookies') or None
                if req_method.upper() != 'GET':
                    post_data = start_map.get('body', '')
                    if isinstance(post_data, dict):
                        req_body = urllib.urlencode(post_data)
                    elif isinstance(post_data, unicode) or isinstance(post_data, str):
                        req_body = post_data
                    if 'application/json' in req_headers.get('Content-Type', ''):
                        req_body = json.loads(req_body)
                else:
                    req_body = None
                req_meta = start_map.get('meta', {}) or {}
                return Request(url=req_url, callback=req_callback_method, method=req_method, meta=req_meta, body=req_body, headers=req_headers, cookies=req_cookies, dont_filter=close_filter)
            except Exception:
                self.logger.exception('parse start url error, source start url is %s' % start_map)

            return

    def is_blocked_spider(self, response):
        u"""检测爬虫是否被屏蔽的方法。每个成功的请求，都会进入这个函数
        默认为 False, 即爬虫没有被屏蔽，没有被屏蔽，那么就会进入正常流程，接下来调用对应callback

        可以重写这个函数，来检测爬虫是否被屏蔽，比如检测
        u"次数过多" in resposne.body
        出现这个情况的时候，就是True，爬虫就被屏蔽，就不会进入接下来的callback正常流程
        接下里就会调用blocked_call_back， 来进行屏蔽处理

        method is called every time to check if blocked the spider, default to be False or None
        """
        pass

    def blocked_call_back(self, response, reason='spider was blocked', exc_info=None, extra=None):
        u"""兼容历史老代码的api
        """
        self.blocked_callback(response, reason, exc_info, extra)

    def blocked_callback(self, response, reason='spider was blocked', exc_info=None, extra=None):
        u"""如果检测到爬虫被屏蔽，那么就会调用这个函数来对进行处理
        默认的操作是重新放回 任务队列的队尾，可以通过重写这个方法，来完成自定义的 屏蔽处理逻辑

        注意一点：这个函数，并不只是在被屏蔽的时候可以调用，它是 【通用的】
        即，当你需要重新抓取某个链接的时候，可以通过 【假装这个链接被屏蔽了】，来达到重新抓取的效果

        一个典型应用就是： 我在列表页list发现了新的任务，通过调用blocked_call_back 的put_back_2_start_url, 达到添加任务的效果

        method called when spider is blocked, also can be used to record other error situation"""
        self.report_this_crawl_2_log(response, reason, exc_info)
        if not exc_info:
            exc_info = '%s; response.body %s' % (reason, response.body)
        self.put_back_2_start_url(response, exc_info)

    def report_this_crawl_2_log(self, response, reason, exc_info=None):
        u"""记录此次请求
        log this response
        """
        if not exc_info:
            exc_info = reason
        report_template = '\n            response body -> %(response_body)s\n            %(response)s is recorded, because %(reason)s happended, following are detail info:\n            response url -> %(response_url)s,\n            status code -> %(status_code)s,\n            request url -> %(request_url)s,\n            original request url -> %(original_request_url)s\n\n            request headers -> %(request_headers)s,\n            request body -> %(request_body)s,\n\n            request callback -> %(request_callback)s,\n\n            exc_info -> %(exc_info)s\n            '
        report_info = {'response': response.url, 
           'reason': reason, 
           'response_url': response.url, 
           'status_code': response.status, 
           'request_url': response.request.url, 
           'original_request_url': self.get_source_url(response), 
           'request_headers': response.request.headers, 
           'request_body': self.get_request_body(response), 
           'request_callback': self.get_last_request_callback(response), 
           'response_body': self.get_unicode_response_body(response), 
           'exc_info': exc_info}
        self.logger.warning(report_template % report_info)

    def get_common_request(self, r):
        u"""兼容Reques和Response 的状态，统一变为request状态
        避免修改，返回的都是副本

        注意：Request object can't use copy
        """
        if isinstance(r, Response):
            r_copy = r.request.copy()
        else:
            r_copy = r.copy()
        return r_copy

    def get_source_url(self, r):
        u"""获得最原始的的请求链接
        因为在302跳转的情况下，当前的链接，并不是最开始的任务链接
        to get the original url, because 302 will modified the request url
        """
        r_copy = self.get_common_request(r)
        source_url = r_copy.meta.get('easyspider', {}).get('source_start_url')
        redirect_urls = r_copy.meta.get('redirect_urls') or []
        if source_url:
            return source_url
        else:
            if len(redirect_urls) > 0:
                return redirect_urls[0]
            return r_copy.url

    def get_request_body(self, r):
        u"""把字符串的请求体，变成字典类型，方便人类查看
        return str/unicode request body -> dict
        """
        r_copy = self.get_common_request(r)
        dict_body = self.parse_query_2_dict(r_copy.body)
        if not dict_body:
            try:
                dict_body = json.dumps(r_copy.body, ensure_ascii=False)
            except Exception:
                self.logger.exception('convert request body failed... source body is %s' % r_copy.body)

        return dict_body

    def parse_query_2_dict(self, query):
        """parse url query to dict format"""
        try:
            return dict([ (k, v[0]) for k, v in urlparse.parse_qs(query).items() ])
        except Exception:
            self.logger.exception("can't parse url -> dict, source url data is %s" % query)

    def detect_encoding(self, body):
        dammit = UnicodeDammit(body)
        return dammit.original_encoding

    def get_unicode_response_body(self, response):
        u"""避免乱码，在保存的时候，所有的body 都会被解码成unicode形式
        """
        encoding = self.detect_encoding(response.body)
        if encoding:
            try:
                return response.body.decode(encoding)
            except Exception:
                msg = traceback.format_exc()
                return 'decode response error, msg is %s' % msg

        return response.body

    def put_back_2_start_url(self, r, exc_info=None, last_response=None):
        u"""非常有效的核心通用函数
        这个函数不只是在 检测是否被屏蔽的时候可以调用

        还可以被充当，添加新任务的功能。
        如果需要添加一个新的任务，那么直接调用这个函数就可以了

        reput request to redis
        """
        r_copy = self.get_common_request(r)
        if not last_response:
            last_response_copy = r_copy
        else:
            last_response_copy = self.get_common_request(last_response)
        if hasattr(r_copy, 'priority'):
            priority = r_copy.priority or 0
        else:
            priority = 0
        reput_request = {'url': self.get_source_url(r_copy), 
           'callback': self.get_last_request_callback(r_copy), 
           'method': r_copy.method, 
           'headers': r_copy.headers, 
           'dont_filter': True if not hasattr(r, 'dont_filter') or r.dont_filter is None else r.dont_filter, 
           'priority': priority}
        reput_request['body'] = self.get_request_body(r_copy)
        if reput_request.get('method') == 'GET':
            reput_request.pop('body')
        meta = copy.deepcopy(r_copy.meta)
        last_easyspider = meta.get('easyspider') or {}
        last_easyspider.update({'from_retry': int(last_easyspider.get('from_retry', -1)) + 1, 
           'source_start_url': self.get_source_url(r_copy), 
           'remark': last_easyspider.get('remark'), 
           'crawled_urls_path': last_easyspider.get('crawled_urls_path', []) + [last_response_copy.url], 
           'exc_info': exc_info})
        try:
            last_easyspider['crawled_server'] = (';').join(flat(socket.gethostbyname_ex(socket.gethostname())))
        except Exception:
            last_easyspider['crawled_server'] = socket.gethostname()

        last_easyspider['crawled_time'] = get_time()
        meta['easyspider'] = last_easyspider
        reput_request['meta'] = meta
        if self.settings.get('COOKIES_ENABLED'):
            reput_request['cookies'] = r_copy.cookies
        while True:
            try:
                max_retry_time = self.retry_max_time + 1
                current_retry_time = reput_request.get('meta').get('easyspider').get('from_retry')
                if current_retry_time >= max_retry_time:
                    self.save_into_redis_method(self.server)('%s:%s' % (self.name, self.failed_key), json.dumps(reput_request))
                elif reput_request.get('priority') > 0:
                    self.save_into_priority_queue(self.server, '%s:%s' % (self.name, self.priority_start_key), float(reput_request.get('priority')), json.dumps(reput_request))
                else:
                    self.save_into_redis_method(self.server)('%s:%s' % (self.name, self.start_key), json.dumps(reput_request))
                break
            except Exception:
                self.logger.exception('in easyCrawlSpider: put_back_2_start_url,  self.save_into_redis_method failed, loop until it successed.. reput_request is %s' % reput_request)
                break

        put_back_logging_template = 'reput crawl task into start url, detail info are %s'
        self.logger.info(put_back_logging_template % reput_request)
        return

    def get_last_request_callback(self, r):
        r_copy = self.get_common_request(r)
        if not r_copy.callback:
            return 'self.parse'
        return 'self.%s' % r_copy.callback.__name__

    def parse_request_to_dict(self, r):
        u"""这家伙不能删除。。。在 core/easyScraper.py 中会调用。。坑爹
        return error request to start step
        """
        if isinstance(r, Response):
            r_copy = r.request.copy()
        else:
            r_copy = r.copy()
        reput_request = {'url': self.get_source_url(r_copy), 
           'callback': self.get_last_request_callback(r_copy), 
           'method': r_copy.method, 
           'body': self.get_request_body(r_copy), 
           'headers': r_copy.headers, 
           'dont_filter': True}
        meta = copy.deepcopy(r.meta)
        meta.get('easyspider', {}).update({'from_retry': int(meta.get('easyspider', {}).get('from_retry', 0) or 0) + 1, 
           'source_start_url': self.get_source_url(r_copy), 
           'remark': meta.get('easyspider', {}).get('remark')})
        reput_request['meta'] = meta
        if self.settings.get('COOKIES_ENABLED'):
            reput_request['cookies'] = r_copy.cookies
        else:
            reput_request['cookies'] = None
        return reput_request

    def extract_text_and_strip(self, xpath_exp):
        u"""用来方便的获取某个下面所有的text"""
        return ('').join(xpath_exp.xpath('.//text()').extract()).strip()

    def text_strip(self, t):
        u"""增强型strip 用来方便的过滤掉其他的乱字符"""
        return t.strip().replace('\r', '').replace('\n', '').replace('\t', '')
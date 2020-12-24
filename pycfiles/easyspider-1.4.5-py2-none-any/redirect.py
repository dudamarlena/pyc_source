# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/middlewares/redirect.py
# Compiled at: 2017-09-08 23:28:21
import logging
from six.moves.urllib.parse import urljoin
from scrapy.downloadermiddlewares.redirect import BaseRedirectMiddleware
logger = logging.getLogger(__name__)

class myBaseRedirectMiddleware(BaseRedirectMiddleware):

    def _redirect(self, redirected, request, spider, reason, response):
        ttl = request.meta.setdefault('redirect_ttl', self.max_redirect_times)
        redirects = request.meta.get('redirect_times', 0) + 1
        if ttl and redirects <= self.max_redirect_times:
            redirected.meta['redirect_times'] = redirects
            redirected.meta['redirect_ttl'] = ttl - 1
            redirected.meta['redirect_urls'] = request.meta.get('redirect_urls', []) + [
             request.url]
            redirected.priority = request.priority + self.priority_adjust
            logger.debug('Redirecting (%(reason)s) to %(redirected)s from %(request)s', {'reason': reason, 'redirected': redirected, 'request': request})
            return redirected
        else:
            response.request = request.copy()
            spider.report_this_crawl_2_log(response, 'Discarding %(request)s: max redirections reached' % {'request': request})
            return response


class directReturnRedirectMiddleware(myBaseRedirectMiddleware):
    """Handle redirection of requests based on response status and meta-refresh html tag"""

    def process_response(self, request, response, spider):
        if request.meta.get('dont_redirect', False):
            return response
        if request.method == 'HEAD':
            if response.status in (301, 302, 303, 307) and 'Location' in response.headers:
                redirected_url = urljoin(request.url, response.headers['location'])
                redirected = request.replace(url=redirected_url)
                redirected = redirected.replace(dont_filter=True)
                return self._redirect(redirected, request, spider, response.status, response)
            else:
                return response

        if response.status in (302, 303) and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected = self._redirect_request_using_get(request, redirected_url)
            redirected = redirected.replace(dont_filter=True)
            return self._redirect(redirected, request, spider, response.status, response)
        if response.status in (301, 307) and 'Location' in response.headers:
            redirected_url = urljoin(request.url, response.headers['location'])
            redirected = request.replace(url=redirected_url)
            redirected = redirected.replace(dont_filter=True)
            return self._redirect(redirected, request, spider, response.status, response)
        return response
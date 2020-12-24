# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/url/handlers.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 3312 bytes
try:
    from urllib.parse import urlparse
    from urllib import robotparser
except ImportError:
    from urlparse import urlparse
    import robotparser

from tornado import gen, httpclient, web
from tornado.log import app_log
from tornado.escape import url_unescape
from ...utils import quote, response_text
from ..base import cached, RenderingHandler

class URLHandler(RenderingHandler):
    __doc__ = 'Renderer for /url or /urls'

    @cached
    @gen.coroutine
    def get(self, secure, netloc, url):
        proto = 'http' + secure
        netloc = url_unescape(netloc)
        if '/?' in url:
            url, query = url.rsplit('/?', 1)
        else:
            query = None
        remote_url = '{}://{}/{}'.format(proto, netloc, quote(url))
        if query:
            remote_url = remote_url + '?' + query
        if not url.endswith('.ipynb'):
            refer_url = self.request.headers.get('Referer', '').split('://')[(-1)]
            if refer_url.startswith(self.request.host + '/url'):
                self.redirect(remote_url)
                return
        parse_result = urlparse(remote_url)
        robots_url = parse_result.scheme + '://' + parse_result.netloc + '/robots.txt'
        public = False
        try:
            robots_response = yield self.fetch(robots_url)
            robotstxt = response_text(robots_response)
            rfp = robotparser.RobotFileParser()
            rfp.set_url(robots_url)
            rfp.parse(robotstxt.splitlines())
            public = rfp.can_fetch('*', remote_url)
        except httpclient.HTTPError as e:
            app_log.debug(('Robots.txt not available for {}'.format(remote_url)), exc_info=True)
            public = True
        except Exception as e:
            app_log.error(e)

        response = yield self.fetch(remote_url)
        try:
            nbjson = response_text(response, encoding='utf-8')
        except UnicodeDecodeError:
            app_log.error('Notebook is not utf8: %s', remote_url, exc_info=True)
            raise web.HTTPError(400)

        yield self.finish_notebook(nbjson, download_url=remote_url, msg=('file from url: %s' % remote_url),
          public=public,
          request=(self.request),
          format=(self.format))


def default_handlers(handlers=[]):
    """Tornado handlers"""
    return handlers + [
     (
      '/url([s]?)/([^/]+)/(.*)', URLHandler)]


def uri_rewrites(rewrites=[]):
    return rewrites + [
     ('^http(s?)://(.*)$', '/url{0}/{1}'),
     ('^(.*)$', '/url/{0}')]
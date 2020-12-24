# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/comhandler.py
# Compiled at: 2016-11-30 13:23:02
# Size of source mod 2**32: 2710 bytes
import logging
from otest import FatalError
from otest.contenthandler import HandlerResponse
from otest.events import EV_HTTP_RESPONSE
__author__ = 'roland'
logger = logging.getLogger(__name__)

class ComHandler(object):

    def __init__(self, contenthandlers, conv=None, auto_close_urls=None):
        self.content_handlers = contenthandlers
        self.conv = conv
        self.auto_close_urls = auto_close_urls or []
        self.verify_ssl = True

    def __call__(self, http_response, target_url='', auto_close_urls=None, conv=None, **kwargs):
        if not http_response:
            return
        auto_close_urls = auto_close_urls or []
        auto_close_urls.extend(self.auto_close_urls)
        rdseq = []
        while 1:
            if http_response.status_code >= 400:
                return http_response
            while http_response.status_code in (300, 301, 302):
                url = http_response.headers['location']
                if url in rdseq:
                    raise FatalError('Loop detected in redirects')
                else:
                    rdseq.append(url)
                    if len(rdseq) > 8:
                        raise FatalError('Too long sequence of redirects: %s' % rdseq)
                    else:
                        logger.info('HTTP %d Location: %s' % (http_response.status_code,
                         url))
                        if url in auto_close_urls:
                            return http_response
                        try:
                            logger.info('GET %s' % url)
                            http_response = self.conv.entity.send(url, 'GET')
                        except Exception as err:
                            try:
                                raise FatalError('%s' % err)
                            finally:
                                err = None
                                del err

                    self.conv.events(EV_HTTP_RESPONSE, http_response)
                if http_response.status_code >= 400:
                    return http_response

            handled = False
            for ct in self.content_handlers:
                resp = ct.handle_response(http_response, auto_close_urls, conv=(self.conv),
                  verify_ssl=(self.verify_ssl),
                  cookie_jar=(self.conv.entity.cookiejar))
                if resp.content_processed:
                    if resp.cookie_jar:
                        self.conv.entity.cookie_jar = resp.cookie_jar
                    elif resp.http_response:
                        http_response = resp.http_response
                    else:
                        return resp
                    handled = True
                    break

            if not handled:
                return HandlerResponse(False)
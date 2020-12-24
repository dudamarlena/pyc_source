# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/utils/google.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import cookielib, httplib, re, socket, urllib, urllib2
from lib.core.common import getUnicode
from lib.core.common import urlencode
from lib.core.data import conf
from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.exception import SqlmapConnectionException
from lib.core.exception import SqlmapGenericException
from lib.core.settings import GOOGLE_REGEX
from lib.core.settings import UNICODE_ENCODING
from lib.request.basic import decodePage

class Google(object):
    """
    This class defines methods used to perform Google dorking (command
    line option '-g <google dork>'
    """

    def __init__(self, handlers):
        self._cj = cookielib.CookieJar()
        handlers.append(urllib2.HTTPCookieProcessor(self._cj))
        self.opener = urllib2.build_opener(*handlers)
        self.opener.addheaders = conf.httpHeaders
        try:
            conn = self.opener.open('http://www.google.com/ncr')
            conn.info()
        except urllib2.HTTPError as e:
            e.info()
        except urllib2.URLError:
            errMsg = 'unable to connect to Google'
            raise SqlmapConnectionException(errMsg)

    def search(self, dork):
        """
        This method performs the effective search on Google providing
        the google dork and the Google session cookie
        """
        gpage = conf.googlePage if conf.googlePage > 1 else 1
        logger.info('using Google result page #%d' % gpage)
        if not dork:
            return
        url = 'http://www.google.com/search?'
        url += 'q=%s&' % urlencode(dork, convall=True)
        url += 'num=100&hl=en&complete=0&safe=off&filter=0&btnG=Search'
        url += '&start=%d' % ((gpage - 1) * 100)
        try:
            conn = self.opener.open(url)
            requestMsg = 'HTTP request:\nGET %s' % url
            requestMsg += ' %s' % httplib.HTTPConnection._http_vsn_str
            logger.log(CUSTOM_LOGGING.TRAFFIC_OUT, requestMsg)
            page = conn.read()
            code = conn.code
            status = conn.msg
            responseHeaders = conn.info()
            page = decodePage(page, responseHeaders.get('Content-Encoding'), responseHeaders.get('Content-Type'))
            responseMsg = 'HTTP response (%s - %d):\n' % (status, code)
            if conf.verbose <= 4:
                responseMsg += getUnicode(responseHeaders, UNICODE_ENCODING)
            elif conf.verbose > 4:
                responseMsg += '%s\n%s\n' % (responseHeaders, page)
            logger.log(CUSTOM_LOGGING.TRAFFIC_IN, responseMsg)
        except urllib2.HTTPError as e:
            try:
                page = e.read()
            except socket.timeout:
                warnMsg = 'connection timed out while trying '
                warnMsg += 'to get error page information (%d)' % e.code
                logger.critical(warnMsg)
                return

        except (urllib2.URLError, socket.error, socket.timeout):
            errMsg = 'unable to connect to Google'
            raise SqlmapConnectionException(errMsg)

        retVal = [ urllib.unquote(match.group(1)) for match in re.finditer(GOOGLE_REGEX, page, re.I | re.S) ]
        if not retVal and 'detected unusual traffic' in page:
            warnMsg = "Google has detected 'unusual' traffic from "
            warnMsg += 'used IP address disabling further searches'
            raise SqlmapGenericException(warnMsg)
        return retVal
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/request/basic.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import codecs, gzip, logging, re, StringIO, struct, zlib
from lib.core.common import extractErrorMessage
from lib.core.common import extractRegexResult
from lib.core.common import getUnicode
from lib.core.common import readInput
from lib.core.common import resetCookieJar
from lib.core.common import singleTimeLogMessage
from lib.core.common import singleTimeWarnMessage
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
from lib.core.enums import HTTP_HEADER
from lib.core.enums import PLACE
from lib.core.exception import SqlmapCompressionException
from lib.core.settings import DEFAULT_COOKIE_DELIMITER
from lib.core.settings import EVENTVALIDATION_REGEX
from lib.core.settings import MAX_CONNECTION_TOTAL_SIZE
from lib.core.settings import ML
from lib.core.settings import META_CHARSET_REGEX
from lib.core.settings import PARSE_HEADERS_LIMIT
from lib.core.settings import VIEWSTATE_REGEX
from lib.parse.headers import headersParser
from lib.parse.html import htmlParser
from lib.utils.htmlentities import htmlEntities
from thirdparty.chardet import detect

def forgeHeaders(items=None):
    """
    Prepare HTTP Cookie, HTTP User-Agent and HTTP Referer headers to use when performing
    the HTTP requests
    """
    items = items or {}
    for _ in items.keys():
        if items[_] is None:
            del items[_]

    headers = dict(conf.httpHeaders)
    headers.update(items or {})
    headers = dict((('-').join(_.capitalize() for _ in key.split('-')), value) for key, value in headers.items())
    if conf.cj:
        if HTTP_HEADER.COOKIE in headers:
            for cookie in conf.cj:
                if cookie.domain_specified and not conf.hostname.endswith(cookie.domain):
                    continue
                if '%s=' % cookie.name in headers[HTTP_HEADER.COOKIE]:
                    if conf.loadCookies:
                        conf.httpHeaders = filter(None, ((item if item[0] != HTTP_HEADER.COOKIE else None) for item in conf.httpHeaders))
                    elif kb.mergeCookies is None:
                        message = 'you provided a HTTP %s header value. ' % HTTP_HEADER.COOKIE
                        message += 'The target URL provided its own cookies within '
                        message += 'the HTTP %s header which intersect with yours. ' % HTTP_HEADER.SET_COOKIE
                        message += 'Do you want to merge them in futher requests? [Y/n] '
                        _ = readInput(message, default='Y')
                        kb.mergeCookies = not _ or _[0] in ('y', 'Y')
                    if kb.mergeCookies:
                        _ = lambda x: re.sub('(?i)%s=[^%s]+' % (cookie.name, conf.cDel or DEFAULT_COOKIE_DELIMITER), '%s=%s' % (cookie.name, cookie.value), x)
                        headers[HTTP_HEADER.COOKIE] = _(headers[HTTP_HEADER.COOKIE])
                        if PLACE.COOKIE in conf.parameters:
                            conf.parameters[PLACE.COOKIE] = _(conf.parameters[PLACE.COOKIE])
                        conf.httpHeaders = [ (item[0], item[1] if item[0] != HTTP_HEADER.COOKIE else _(item[1])) for item in conf.httpHeaders ]
                elif not kb.testMode:
                    headers[HTTP_HEADER.COOKIE] += '%s %s=%s' % (conf.cDel or DEFAULT_COOKIE_DELIMITER, cookie.name, cookie.value)

        if kb.testMode:
            resetCookieJar(conf.cj)
    return headers


def parseResponse(page, headers):
    """
    @param page: the page to parse to feed the knowledge base htmlFp
    (back-end DBMS fingerprint based upon DBMS error messages return
    through the web application) list and absFilePaths (absolute file
    paths) set.
    """
    if headers:
        headersParser(headers)
    if page:
        htmlParser(page)


def checkCharEncoding(encoding, warn=True):
    """
    Checks encoding name, repairs common misspellings and adjusts to
    proper namings used in codecs module

    >>> checkCharEncoding('iso-8858', False)
    'iso8859-1'
    >>> checkCharEncoding('en_us', False)
    'utf8'
    """
    if encoding:
        encoding = encoding.lower()
    else:
        return encoding
    translate = {'windows-874': 'iso-8859-11', 'en_us': 'utf8', 'macintosh': 'iso-8859-1', 'euc_tw': 'big5_tw', 'th': 'tis-620', 'unicode': 'utf8', 'utc8': 'utf8', 'ebcdic': 'ebcdic-cp-be', 'iso-8859': 'iso8859-1'}
    for delimiter in (';', ',', '('):
        if delimiter in encoding:
            encoding = encoding[:encoding.find(delimiter)].strip()

    if '8858' in encoding:
        encoding = encoding.replace('8858', '8859')
    else:
        if '8559' in encoding:
            encoding = encoding.replace('8559', '8859')
        else:
            if '5889' in encoding:
                encoding = encoding.replace('5889', '8859')
            elif '5589' in encoding:
                encoding = encoding.replace('5589', '8859')
            elif '2313' in encoding:
                encoding = encoding.replace('2313', '2312')
            elif encoding.startswith('x-'):
                encoding = encoding[len('x-'):]
            elif 'windows-cp' in encoding:
                encoding = encoding.replace('windows-cp', 'windows')
            if encoding.startswith('8859'):
                encoding = 'iso-%s' % encoding
            elif encoding.startswith('cp-'):
                encoding = 'cp%s' % encoding[3:]
            elif encoding.startswith('euc-'):
                encoding = 'euc_%s' % encoding[4:]
            elif encoding.startswith('windows') and not encoding.startswith('windows-'):
                encoding = 'windows-%s' % encoding[7:]
            elif encoding.find('iso-88') > 0:
                encoding = encoding[encoding.find('iso-88'):]
            elif encoding.startswith('is0-'):
                encoding = 'iso%s' % encoding[4:]
            elif encoding.find('ascii') > 0:
                encoding = 'ascii'
            elif encoding.find('utf8') > 0:
                encoding = 'utf8'
            if encoding in translate:
                encoding = translate[encoding]
            elif encoding in ('null', '{charset}', '*'):
                return
        try:
            codecs.lookup(encoding)
        except LookupError:
            if warn:
                warnMsg = "unknown web page charset '%s'. " % encoding
                warnMsg += 'Please report by e-mail to %s.' % ML
                singleTimeLogMessage(warnMsg, logging.WARN, encoding)
            encoding = None

    return encoding


def getHeuristicCharEncoding(page):
    """
    Returns page encoding charset detected by usage of heuristics
    Reference: http://chardet.feedparser.org/docs/
    """
    retVal = detect(page)['encoding']
    if retVal:
        infoMsg = "heuristics detected web page charset '%s'" % retVal
        singleTimeLogMessage(infoMsg, logging.INFO, retVal)
    return retVal


def decodePage(page, contentEncoding, contentType):
    """
    Decode compressed/charset HTTP response
    """
    if not page or conf.nullConnection and len(page) < 2:
        return getUnicode(page)
    if isinstance(contentEncoding, basestring) and contentEncoding.lower() in ('gzip',
                                                                               'x-gzip',
                                                                               'deflate'):
        if not kb.pageCompress:
            return
        try:
            if contentEncoding.lower() == 'deflate':
                data = StringIO.StringIO(zlib.decompress(page, -15))
            else:
                data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(page))
                size = struct.unpack('<l', page[-4:])[0]
                if size > MAX_CONNECTION_TOTAL_SIZE:
                    raise Exception('size too large')
            page = data.read()
        except Exception as msg:
            errMsg = 'detected invalid data for declared content '
            errMsg += "encoding '%s' ('%s')" % (contentEncoding, msg)
            singleTimeLogMessage(errMsg, logging.ERROR)
            warnMsg = 'turning off page compression'
            singleTimeWarnMessage(warnMsg)
            kb.pageCompress = False
            raise SqlmapCompressionException

    if not conf.charset:
        httpCharset, metaCharset = (None, None)
        if contentType and contentType.find('charset=') != -1:
            httpCharset = checkCharEncoding(contentType.split('charset=')[(-1)])
        metaCharset = checkCharEncoding(extractRegexResult(META_CHARSET_REGEX, page))
        if any((httpCharset, metaCharset)) and not all((httpCharset, metaCharset)) or httpCharset == metaCharset and all((httpCharset, metaCharset)):
            kb.pageEncoding = httpCharset or metaCharset
            debugMsg = "declared web page charset '%s'" % kb.pageEncoding
            singleTimeLogMessage(debugMsg, logging.DEBUG, debugMsg)
        else:
            kb.pageEncoding = None
    else:
        kb.pageEncoding = conf.charset
    if contentType and not isinstance(page, unicode) and 'text/' in contentType.lower():
        if '&#' in page:
            page = re.sub('&#(\\d{1,3});', lambda _: chr(int(_.group(1))) if int(_.group(1)) < 256 else _.group(0), page)
        if '%' in page:
            page = re.sub('%([0-9a-fA-F]{2})', lambda _: _.group(1).decode('hex'), page)
        page = re.sub('&([^;]+);', lambda _: chr(htmlEntities[_.group(1)]) if htmlEntities.get(_.group(1), 256) < 256 else _.group(0), page)
        kb.pageEncoding = kb.pageEncoding or checkCharEncoding(getHeuristicCharEncoding(page))
        page = getUnicode(page, kb.pageEncoding)
        if '&#' in page:

            def _(match):
                retVal = match.group(0)
                try:
                    retVal = unichr(int(match.group(1)))
                except ValueError:
                    pass

                return retVal

            page = re.sub('&#(\\d+);', _, page)
        page = re.sub('&([^;]+);', lambda _: unichr(htmlEntities[_.group(1)]) if htmlEntities.get(_.group(1), 0) > 255 else _.group(0), page)
    return page


def processResponse(page, responseHeaders):
    kb.processResponseCounter += 1
    parseResponse(page, responseHeaders if kb.processResponseCounter < PARSE_HEADERS_LIMIT else None)
    if conf.parseErrors:
        msg = extractErrorMessage(page)
        if msg:
            logger.warning("parsed DBMS error message: '%s'" % msg)
    if kb.originalPage is None:
        for regex in (EVENTVALIDATION_REGEX, VIEWSTATE_REGEX):
            match = re.search(regex, page)
            if match and PLACE.POST in conf.parameters:
                name, value = match.groups()
                if PLACE.POST in conf.paramDict and name in conf.paramDict[PLACE.POST]:
                    if conf.paramDict[PLACE.POST][name] in page:
                        continue
                    conf.paramDict[PLACE.POST][name] = value
                conf.parameters[PLACE.POST] = re.sub('(?i)(%s=)[^&]+' % name, '\\g<1>%s' % value, conf.parameters[PLACE.POST])

    return
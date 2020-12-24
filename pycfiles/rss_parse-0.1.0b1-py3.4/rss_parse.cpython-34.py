# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rss_parse.py
# Compiled at: 2016-09-01 21:26:28
# Size of source mod 2**32: 4430 bytes
import re, arrow, logging, requests, datetime
from lxml import etree
from dateutil import parser

class RSSParser(list):

    def __init__(self, url, xpath_config):
        self._url = url
        self._xpath_config = xpath_config
        self.refresh()

    def refresh(self):
        self.clear()
        result = None
        try:
            result = requests.get(self._url)
            if result.status_code == 200:
                root = etree.fromstring(result.content)
            else:
                raise requests.exceptions.ConnectionError
        except requests.exceptions.ConnectionError as e:
            logging.error(LogMessages.E_UNABLE_TO_FETCH % (result.status_code if result else '<timeout>', self._url))
        except etree.XMLSyntaxError as e:
            logging.error(LogMessages.E_INVALID_XML % self._url)
        else:
            for e in root.xpath(self._xpath_config[C.XPATH_CONFIG][C.ITEM_ELEM]):
                args = self._parse(e, self._xpath_config[C.XPATH_CONFIG])
                if args:
                    self.append(*args)
                    continue

    def _parse(self, e, xpath_config):
        url = (self._safe_xpath(e, xpath_config[C.XP_URL], xpath_config[C.NAMESPACE]) or b'').decode()
        title = (self._safe_xpath(e, xpath_config[C.XP_TITLE], xpath_config[C.NAMESPACE]) or b'').decode()
        body = (self._safe_xpath(e, xpath_config[C.XP_BODY], xpath_config[C.NAMESPACE]) or b'').decode()
        date = (self._safe_xpath(e, xpath_config[C.XP_DATE], xpath_config[C.NAMESPACE]) or b'').decode()
        image = (self._safe_xpath(e, xpath_config[C.XP_IMAGE], xpath_config[C.NAMESPACE]) or b'').decode()
        body = C.STRIP_HTML_RE.sub('', body) if xpath_config[C.STRIP_HTML] else body
        if not date:
            date = datetime.date.today().strftime('%Y-%m-%dT00:00:00')
        if url and title:
            return (url, title, body, parser.parse(date), image)

    @staticmethod
    def _safe_xpath(e, xp, ns):
        try:
            item = e.xpath(xp, namespaces=ns)
        except etree.XPathEvalError:
            logging.error(LogMessages.E_INVALID_XPATH % (xp, e.tag))
            return

        if item:
            return item[0].encode('ascii', 'ignore')

    def append(self, url, title, body, date, image=None):
        return super().append(self._Story(url, title, body, date, image))

    class _Story(object):

        def __init__(self, url, title, body, date, image):
            self.url = url
            self.title = title
            self.body = body
            self.date = arrow.get(date)
            self.image = image if not image or image.lower().startswith('http') else 'http://' + image


class C(object):
    NAMESPACE = 'namespace'
    STRIP_HTML = 'stripHTML'
    ITEM_ELEM = 'item'
    XPATH_CONFIG = 'xpathParse'
    XP_TITLE = 'title'
    XP_URL = 'url'
    XP_BODY = 'body'
    XP_DATE = 'date'
    XP_IMAGE = 'image'
    STRIP_HTML_RE = re.compile('<[^>]+>', flags=re.I)


class LogMessages(object):
    E_UNABLE_TO_FETCH = 'Unable to fetch URL. Got status %s: %s'
    E_INVALID_XML = 'Could not parse XML from feed: %s'
    E_INVALID_XPATH = 'Invalid xpath %s while processing tag %s'
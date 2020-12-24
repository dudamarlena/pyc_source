# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/utils/crawler.py
# Compiled at: 2020-04-12 10:43:04
# Size of source mod 2**32: 8798 bytes
"""
Crawler application
"""
import logging, re
from abc import abstractmethod
from concurrent import futures
from urllib.parse import urlparse, urljoin
import cloudscraper
from requests import Session
from bs4 import BeautifulSoup, Comment
logger = logging.getLogger(__name__)

class Crawler:
    __doc__ = 'Blueprint for creating new crawlers'

    def __init__(self):
        self._destroyed = False
        self.executor = futures.ThreadPoolExecutor(max_workers=2)
        self.scraper = cloudscraper.create_scraper(browser={'browser':'firefox', 
         'mobile':False})
        self.novel_title = 'N/A'
        self.novel_author = 'N/A'
        self.novel_cover = None
        self.is_rtl = False
        self.volumes = []
        self.chapters = []
        self.home_url = ''
        self.novel_url = ''
        self.last_visited_url = None

    def destroy(self):
        self._destroyed = True
        self.volumes.clear()
        self.chapters.clear()
        self.scraper.close()
        self.executor.shutdown(False)

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def login(self, email, password):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def search_novel(self, query):
        """Gets a list of results matching the given query"""
        pass

    @abstractmethod
    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        pass

    @abstractmethod
    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        pass

    def get_chapter_index_of(self, url):
        """Return the index of chapter by given url or 0"""
        url = (url or '').strip().strip('/')
        for chapter in self.chapters:
            if chapter['url'] == url:
                return chapter['id']

        return 0

    @property
    def headers(self):
        return self.scraper.headers.copy()

    @property
    def cookies(self):
        return {x.name:x.value for x in self.scraper.cookies}

    def absolute_url(self, url, page_url=None):
        url = (url or '').strip()
        if not page_url:
            page_url = self.last_visited_url
        return urljoin(page_url, url)

    def is_relative_url(self, url):
        page = urlparse(self.novel_url)
        url = urlparse(url)
        return page.hostname == url.hostname and url.path.startswith(page.path)

    def get_response(self, url, **kargs):
        if self._destroyed:
            return
        else:
            kargs = kargs or dict()
            kargs['timeout'] = kargs.get('timeout', 150)
            self.last_visited_url = url.strip('/')
            response = (self.scraper.get)(url, **kargs)
            response.encoding = 'utf-8'
            self.cookies.update({x.name:x.value for x in response.cookies})
            response.raise_for_status()
            return response

    def submit_form(self, url, data={}, multipart=False, headers={}):
        """Submit a form using post request"""
        if self._destroyed:
            return
        else:
            headers.update({'Content-Type': 'multipart/form-data' if multipart else 'application/x-www-form-urlencoded; charset=UTF-8'})
            response = self.scraper.post(url, data=data, headers=headers)
            response.encoding = 'utf-8'
            self.cookies.update({x.name:x.value for x in response.cookies})
            response.raise_for_status()
            return response

    def get_soup(self, *args, parser='lxml', **kargs):
        response = (self.get_response)(*args, **kargs)
        return self.make_soup(response)

    def make_soup(self, response, parser='lxml'):
        html = response.content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html, parser)
        if not soup.find('body'):
            raise ConnectionError('HTML document was not loaded properly')
        return soup

    def get_json(self, *args, **kargs):
        response = (self.get_response)(*args, **kargs)
        return response.json()

    def download_cover(self, output_file):
        response = self.get_response(self.novel_cover)
        with open(output_file, 'wb') as (f):
            f.write(response.content)

    blacklist_patterns = [
     '^[\\W\\D]*(volume|chapter)[\\W\\D]+\\d+[\\W\\D]*$']
    bad_tags = [
     'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
     'button', 'input', 'amp-auto-ads', 'pirate']
    block_tags = [
     'h3', 'div', 'p']

    def is_blacklisted(self, text):
        if len(text.strip()) == 0:
            return True
        else:
            for pattern in self.blacklist_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return True

            return False

    def clean_contents(self, div):
        if not div:
            return div
        else:
            div.attrs = {}
            for tag in div.findAll(True):
                if isinstance(tag, Comment):
                    tag.extract()
                else:
                    if tag.name == 'br':
                        next_tag = getattr(tag, 'next_sibling')
                        if next_tag and getattr(next_tag, 'name') == 'br':
                            tag.extract()
                        else:
                            if tag.name in self.bad_tags:
                                tag.extract()
                            else:
                                if not tag.text.strip():
                                    tag.extract()
                                else:
                                    if self.is_blacklisted(tag.text):
                                        tag.extract()
                                    elif hasattr(tag, 'attrs'):
                                        tag.attrs = {}

            return div

    def extract_contents(self, tag, level=0):
        body = []
        if level == 0:
            self.clean_contents(tag)
        for elem in tag.contents:
            if self.block_tags.count(elem.name):
                body += self.extract_contents(elem, level + 1)
            else:
                text = ''
                if not elem.name:
                    text = str(elem).strip()
                else:
                    text = '<%s>%s</%s>'
                    text = text % (elem.name, elem.text.strip(), elem.name)
                if text:
                    body.append(text)

        if level > 0:
            return body
        else:
            return [x for x in body if len(x.strip())]

    def cleanup_text(self, text):
        return re.sub('[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]', '',
          (str(text)), flags=(re.UNICODE))
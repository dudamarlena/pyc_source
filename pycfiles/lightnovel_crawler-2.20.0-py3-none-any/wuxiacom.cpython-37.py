# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\wuxiacom.py
# Compiled at: 2020-03-23 13:52:11
# Size of source mod 2**32: 5088 bytes
import json, logging, re, requests
from bs4 import BeautifulSoup
from utils.crawler import Crawler
logger = logging.getLogger('WUXIA_WORLD')
book_url = 'https://www.wuxiaworld.com/novel/%s'
search_url = 'https://www.wuxiaworld.com/api/novels/search?query=%s&count=5'

class WuxiaComCrawler(Crawler):
    base_url = [
     'https://www.wuxiaworld.com/']

    def initialize(self):
        self.home_url = 'https://www.wuxiaworld.com'

    def search_novel(self, query):
        """Gets a list of {title, url} matching the given query"""
        url = search_url % query
        logger.info('Visiting %s ...', url)
        data = requests.get(url).json()
        logger.debug(data)
        results = []
        for item in data['items'][:5]:
            results.append({'title':item['name'], 
             'url':book_url % item['slug'], 
             'info':self.search_novel_info(book_url % item['slug'])})

        return results

    def search_novel_info(self, url):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        volumes = []
        chapters = []
        for panel in soup.select('#accordion .panel-default'):
            vol_id = int(panel.select_one('h4.panel-title .book').text)
            vol_title = panel.select_one('h4.panel-title .title a').text
            volumes.append({'id':vol_id, 
             'title':vol_title})
            for a in panel.select('ul.list-chapters li.chapter-item a'):
                chap_id = len(self.chapters) + 1
                chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'url':self.absolute_url(a['href']), 
                 'title':a.text.strip() or 'Chapter %d' % chap_id})

        info = 'Volume : %s, Chapter : %s, Latest: %s' % (
         len(volumes), len(chapters), chapters[(-1)]['title'])
        return info

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        self.novel_id = self.novel_url.split('wuxiaworld.com/novel/')[1].split('/')[0]
        logger.info('Novel Id: %s', self.novel_id)
        self.novel_url = book_url % self.novel_id
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('.section-content h2').text
        logger.info('Novel title: %s', self.novel_title)
        try:
            self.novel_cover = self.absolute_url(soup.select_one('img.media-object')['src'])
            logger.info('Novel cover: %s', self.novel_cover)
        except Exception:
            logger.debug('Failed to get cover: %s', self.novel_url)

        authors = ''
        for d in soup.select_one('.media-body dl, .novel-body').select('dt, dd'):
            authors += d.text.strip()
            authors += ' ' if d.name == 'dt' else '; '

        self.novel_author = authors.strip().strip(';')
        logger.info('Novel author: %s', self.novel_author)
        for panel in soup.select('#accordion .panel-default'):
            vol_id = int(panel.select_one('h4.panel-title .book').text)
            vol_title = panel.select_one('h4.panel-title .title a').text
            if re.search('table of contents', vol_title, flags=(re.I)):
                vol_title = 'Volume %s' % vol_id
            self.volumes.append({'id':vol_id, 
             'title':vol_title.strip()})
            for a in panel.select('ul.list-chapters li.chapter-item a'):
                chap_id = len(self.chapters) + 1
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'url':self.absolute_url(a['href']), 
                 'title':a.text.strip()})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format"""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        body = soup.select_one('#chapterContent')
        if not body:
            body = soup.select_one('#chapter-content')
        else:
            if not body:
                body = soup.select_one('.panel-default .fr-view')
            return body or ''
        for nav in soup.select('.chapter-nav') or []:
            nav.extract()

        self.blacklist_patterns = [
         '^<span>(...|\\u2026)</span>$',
         '^translat(ed by|or)',
         '(volume|chapter) .?\\d+']
        self.clean_contents(body)
        return '\n'.join([str(x) for x in body.contents])
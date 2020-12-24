# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\wuxialeague.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 2077 bytes
import logging, re
from utils.crawler import Crawler
logger = logging.getLogger('WUXIA_LEAGUE')

class WuxiaLeagueCrawler(Crawler):
    base_url = 'https://www.wuxialeague.com/'

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('#bookinfo .d_title h1').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('#bookimg img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        possible_authors = [a.text for a in soup.select('#bookinfo a[href*="/author/"]')]
        self.novel_author = ', '.join(possible_authors)
        logger.info('Novel author: %s', self.novel_author)
        for a in soup.select('#chapterList li a'):
            chap_id = 1 + len(self.chapters)
            vol_id = 1 + len(self.chapters) // 100
            if chap_id % 100 == 1:
                self.volumes.append({'id': vol_id})
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'title':a.text.strip(), 
             'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format"""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        body = ''
        title_found = False
        for p in soup.select('#TextContent > p'):
            if not p.text.strip():
                continue
            clean_first = ''.join(re.findall('([a-z0-9]+)', p.text.lower()))
            clean_title = ''.join(re.findall('([a-z0-9]+)', chapter['title'].lower()))
            if clean_first == clean_title:
                continue
            body += str(p).strip()

        return body
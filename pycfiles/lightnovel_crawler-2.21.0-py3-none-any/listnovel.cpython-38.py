# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\listnovel.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 1981 bytes
import json, logging, re
from urllib.parse import urlparse
from utils.crawler import Crawler
logger = logging.getLogger('LIST_NOVEL')

class ListNovelCrawler(Crawler):
    base_url = 'https://listnovel.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        possible_title = soup.select_one('.post-title h1')
        for span in possible_title.select('span'):
            span.extract()
        else:
            self.novel_title = possible_title.text.strip()
            logger.info('Novel title: %s', self.novel_title)
            self.novel_cover = self.absolute_url(soup.select_one('.summary_image a img')['data-src'])
            logger.info('Novel cover: %s', self.novel_cover)
            self.novel_author = ' '.join([a.text.strip() for a in soup.select('.author-content a[href*="manga-author"]')])
            logger.info('%s', self.novel_author)
            for a in reversed(soup.select('.main-col li.wp-manga-chapter a')):
                chap_id = len(self.chapters) + 1
                vol_id = 1 + len(self.chapters) // 100
                if chap_id % 100 == 1:
                    self.volumes.append({'id': vol_id})
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'title':a.text.strip(), 
                 'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select('.reading-content p')
        return ''.join([str(p) for p in contents])
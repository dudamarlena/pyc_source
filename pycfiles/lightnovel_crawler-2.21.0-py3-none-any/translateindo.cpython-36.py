# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/translateindo.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2929 bytes
import logging, re
from urllib.parse import quote, urlparse
import urllib.parse
from bs4 import BeautifulSoup
from ..utils.crawler import Crawler
logger = logging.getLogger('TRANSLATEINDO')

class TranslateIndoCrawler(Crawler):
    base_url = 'https://www.translateindo.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h1.entry-title').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        possible_cover = soup.select_one('div.entry-content img')['src']
        if possible_cover:
            self.novel_cover = self.absolute_url(possible_cover)
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = soup.select_one('div.entry-content p span').text
        self.novel_author = re.sub('[\\(\\s\\)]+', ' ', self.novel_author).strip()
        self.novel_author = re.sub('Author: ', '', self.novel_author)
        logger.info('Novel author: %s', self.novel_author)
        chapters = soup.select_one('div#comments').find_previous_sibling('div').select('a')
        for a in chapters:
            chap_id = len(self.chapters) + 1
            vol_id = chap_id // 100 + 1
            if len(self.chapters) % 100 == 0:
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({'id':vol_id, 
                 'title':vol_title})
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'url':self.absolute_url(a['href']), 
             'title':a.text.strip() or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format"""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select('div.entry-content p')
        body = [str(p) for p in contents if p.text.strip()]
        return '<p>' + '</p><p>'.join(body) + '</p>'
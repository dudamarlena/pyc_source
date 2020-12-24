# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/worldnovelonline.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 5372 bytes
import logging, re, json
from urllib.parse import quote, urlparse
import urllib.parse
from bs4 import BeautifulSoup
from ..utils.crawler import Crawler
logger = logging.getLogger('WORLDNOVEL_ONLINE')
search_url = 'https://www.worldnovel.online/wp-json/writerist/v1/novel/search?keyword=%s'
chapter_list_url = 'https://www.worldnovel.online/wp-json/writerist/v1/chapters?category=%s&perpage=100&order=ASC&paged=%s'

class WorldnovelonlineCrawler(Crawler):
    base_url = 'https://www.worldnovel.online/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('.breadcrumb-item.active').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        possible_cover = soup.select_one('img.lazy[alt*="Thumbnail"]')
        if possible_cover:
            self.novel_cover = self.absolute_url(possible_cover['data-src'])
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = soup.select_one('a[href*="/authorr/"]').text.strip()
        logger.info('Novel author: %s', self.novel_author)
        path = urllib.parse.urlsplit(self.novel_url)[2]
        book_id = path.split('/')[2]
        logger.info('Bookid = %s' % book_id)
        page = len(soup.select('div.d-flex div.jump-to.mr-2'))
        data = []
        for x in range(page):
            list_url = chapter_list_url % (book_id, x + 1)
            logger.debug('Visiting %s', list_url)
            data.extend(self.get_json(list_url))

        volumes = set()
        for item in data:
            vol_id = len(self.chapters) // 100 + 1
            volumes.add(vol_id)
            self.chapters.append({'id':len(self.chapters) + 1, 
             'volume':vol_id, 
             'url':item['permalink'], 
             'title':item['post_title']})

        self.volumes = [{'id': x} for x in volumes]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format"""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select_one(', '.join([
         '.post-content.cha-words',
         '.cha-content',
         '.chapter-fill',
         '.entry-content.cl',
         '#content']))
        if not contents:
            return ''
        else:
            for codeblock in contents.select('div.code-block'):
                codeblock.decompose()

            return str(contents)
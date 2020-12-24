# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\aixdzs.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2317 bytes
import json, logging, re
from urllib.parse import urlparse
import requests
from utils.crawler import Crawler
logger = logging.getLogger('AIXDZS_CRAWLER')
chapter_list_url = 'https://read.aixdzs.com/%s'

class AixdzsCrawler(Crawler):
    base_url = 'https://www.aixdzs.com'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        if not self.novel_url.endswith('/'):
            self.novel_url += '/'
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_cover = soup.select_one('meta[property="og:image"]')['content']
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_title = soup.select_one('meta[property="og:novel:book_name"]')['content']
        logger.info('Novel title: %s', self.novel_title)
        self.novel_author = soup.select_one('meta[property="og:novel:author"]')['content']
        logger.info('%s', self.novel_author)
        parsed_url = urlparse(self.novel_url)
        parsed_path = parsed_url.path.strip('/').split('/')
        chapter_url = chapter_list_url % '/'.join(parsed_path[1:])
        logger.debug('Visiting %s', chapter_url)
        soup = self.get_soup(chapter_url)
        volumes = set([])
        for a in reversed(soup.select('div.catalog li a')):
            ch_id = len(self.chapters) + 1
            vol_id = 1 + len(self.chapters) // 100
            volumes.add(vol_id)
            self.chapters.append({'id':ch_id, 
             'volume':vol_id, 
             'title':a.text, 
             'url':self.absolute_url(a['href'], page_url=chapter_url)})
        else:
            self.volumes = [{'id':x,  'title':''} for x in volumes]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        chapter['body_lock'] = True
        contents = soup.select('.content > p')
        contents = [str(p) for p in contents if p.text.strip()]
        return ''.join(contents)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/wuxiaonline.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2889 bytes
import json, logging, re
from ..utils.crawler import Crawler
logger = logging.getLogger('WUXIA_ONLINE')
search_url = 'https://wuxiaworld.online/search.ajax?type=&query=%s'

class WuxiaOnlineCrawler(Crawler):
    base_url = 'https://wuxiaworld.online/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        url = self.novel_url
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        self.novel_title = soup.select_one('h1.entry-title').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.info_image img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        last_vol = -1
        for a in reversed(soup.select('.chapter-list .row span a')):
            chap_id = len(self.chapters) + 1
            vol_id = 1 + (chap_id - 1) // 100
            volume = {'id':vol_id,  'title':''}
            if last_vol != vol_id:
                self.volumes.append(volume)
                last_vol = vol_id
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'title':a['title'], 
             'url':self.absolute_url(a['href'])})

        logger.info('%d chapters and %d volumes found', len(self.chapters), len(self.volumes))

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        parts = soup.select_one('#list_chapter .content-area')
        body = self.extract_contents(parts)
        return '<p>' + '</p><p>'.join(body) + '</p>'
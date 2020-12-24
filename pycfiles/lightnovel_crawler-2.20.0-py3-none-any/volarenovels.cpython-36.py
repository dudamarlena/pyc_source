# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/volarenovels.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 2414 bytes
import json, logging, re
from ..utils.crawler import Crawler
logger = logging.getLogger('VOLARE_NOVELS')

class VolareNovelsCrawler(Crawler):
    base_url = 'https://www.volarenovels.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('#content-container h3.title').text
        logger.info('Novel title: %s', self.novel_title)
        try:
            self.novel_author = soup.select('#content-container .p-tb-10-rl-30 p')[1].text.strip()
        except Exception:
            pass

        logger.info('Novel author: %s', self.novel_author)
        try:
            self.novel_cover = self.absolute_url(soup.select_one('#content-container .md-d-table img')['src'])
        except Exception:
            pass

        logger.info('Novel cover: %s', self.novel_cover)
        chapter_urls = set([])
        for div in soup.select('#TableOfContents #accordion .panel'):
            vol_id = len(self.volumes) + 1
            vol_title = div.select_one('h4.panel-title .title a').text.strip()
            try:
                vol_id = int(div.select('h4.panel-title span')[0].text.strip())
            except Exception:
                pass

            self.volumes.append({'id':vol_id, 
             'title':vol_title})
            for a in div.select('.list-chapters li a'):
                chap_id = len(self.chapters) + 1
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'title':a.text.strip(), 
                 'url':self.absolute_url(a['href'])})
                chapter_urls.add(a['href'])

    def download_chapter_body(self, chapter):
        logger.info('Visiting: %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        content = soup.select_one('.panel .panel-body .fr-view')
        return str(content)
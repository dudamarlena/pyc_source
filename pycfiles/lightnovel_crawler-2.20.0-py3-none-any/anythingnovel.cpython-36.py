# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/anythingnovel.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 1782 bytes
import re, logging
from concurrent import futures
from ..utils.crawler import Crawler
logger = logging.getLogger('ANYTHING_NOVEL')

class AnythingNovelCrawler(Crawler):
    base_url = 'https://anythingnovel.com/'

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select('#wrap .breadcrumbs span')[(-1)].text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = soup.select_one('#content a img')['src']
        logger.info('Novel cover: %s', self.novel_cover)
        volumes = set([])
        for a in reversed(soup.select('#content div li a')):
            title = a.text.strip()
            chapter_id = len(self.chapters) + 1
            volume_id = 1 + (chapter_id - 1) // 100
            volumes.add(volume_id)
            self.chapters.append({'id':chapter_id, 
             'volume':volume_id, 
             'title':title, 
             'url':a['href']})

        self.chapters.sort(key=(lambda x: x['id']))
        self.volumes = [{'id':x,  'title':''} for x in volumes]

    def download_chapter_body(self, chapter):
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        content = soup.select_one('div#content')
        self.clean_contents(content)
        body = content.select('p')
        body = [str(p) for p in body if self.should_take(p)]
        return '<p>' + '</p><p>'.join(body) + '</p>'

    def should_take(self, p):
        txt = p.text.strip().lower()
        return txt and txt != 'advertisement'
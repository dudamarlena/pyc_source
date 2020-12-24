# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/fourscanlation.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 2652 bytes
import logging, re
from urllib.parse import urlparse
from ..utils.crawler import Crawler
logger = logging.getLogger('4SCANLATION')
novel_page = 'https://4scanlation.com/%s'

class FourScanlationCrawler(Crawler):
    base_url = 'https://4scanlation.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        path_fragments = urlparse(self.novel_url).path.split('/')
        novel_hash = path_fragments[1]
        if novel_hash == 'category':
            novel_hash = path_fragments[2]
        self.novel_url = novel_page % novel_hash
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one(', '.join([
         'header h1',
         '.header-post-title-class'])).text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_author = 'Source: 4scanlation'
        logger.info('Novel author: %s', self.novel_author)
        possible_image = soup.select_one('#primary article img.wp-post-image')
        if possible_image:
            self.novel_cover = self.absolute_url(possible_image['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        volumes = set()
        for a in soup.select('article.page p a'):
            possible_url = self.absolute_url(a['href'])
            if not self.is_relative_url(possible_url):
                pass
            else:
                chap_id = 1 + len(self.chapters)
                vol_id = 1 + len(self.chapters) // 100
                volumes.add(vol_id)
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'url':possible_url, 
                 'title':a.text.strip()})

        self.volumes = [{'id': x} for x in volumes]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select_one('article div.entry-content')
        if not contents:
            return ''
        else:
            for d in contents.findAll('div'):
                d.extract()

            try:
                chapter['title'] = soup.select_one('header h1').text
                logger.debug(chapter['title'])
            except Exception:
                pass

            return str(contents or '')
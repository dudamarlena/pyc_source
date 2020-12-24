# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/novelv.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 2589 bytes
import re, logging
from concurrent import futures
from ..utils.crawler import Crawler
logger = logging.getLogger('NOVELV')

class NovelvCrawler(Crawler):
    base_url = 'https://www.novelv.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('.panel-default .info .info2 h1').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.panel-default .info .info1 img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        authors = []
        for a in soup.select('.panel-default .info .info2 h3 a'):
            if a['href'].startswith('/author/'):
                authors.append(a.text.strip())

        self.novel_author = ', '.join(authors)
        logger.info('Novel author: %s', self.novel_author)
        volumes = set([])
        for a in soup.select('.panel-default ul.list-charts li a'):
            possible_url = self.absolute_url(a['href'].lower())
            if not possible_url.startswith(self.novel_url):
                pass
            else:
                chapter_id = len(self.chapters) + 1
                volume_id = (chapter_id - 1) // 100 + 1
                volumes.add(volume_id)
                self.chapters.append({'id':chapter_id, 
                 'title':a.text.strip(), 
                 'url':possible_url, 
                 'volume':volume_id})

        self.volumes = [{'id':x,  'title':''} for x in list(volumes)]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        chapter['title'] = self.clean_text(chapter['title'])
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        content = soup.select_one('.panel-body.content-body')
        body = self.extract_contents(content)
        body = '<p>%s</p>' % '</p><p>'.join(body)
        return self.clean_text(body)

    def clean_text(self, text):
        text = re.sub('\\ufffd\\ufffd\\ufffd+', '**', text)
        text = re.sub('\\ufffd\\ufffd', '"', text)
        text = re.sub('\\u00a0\\u00a0', '–', text)
        text = re.sub('\\ufffdC', '', text)
        return text
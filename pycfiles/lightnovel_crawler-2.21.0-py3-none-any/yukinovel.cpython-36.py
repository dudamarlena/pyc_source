# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/yukinovel.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2729 bytes
import json, logging, re
from bs4 import Comment
from ..utils.crawler import Crawler
logger = logging.getLogger('YUKI_NOVEL')

class YukiNovelCrawler(Crawler):
    base_url = 'https://yukinovel.id/'

    def initialize(self):
        self.home_url = 'https://yukinovel.id/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        url = self.novel_url.replace('https://yukinovel.me', 'https://yukinovel.id')
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h1.entry-title').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_author = 'Translated by Yukinovel'
        logger.info('Novel author: %s', self.novel_author)
        self.novel_cover = self.absolute_url(soup.select_one('div.lightnovel-thumb img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        chapters = soup.select('div.lightnovel-episode ul li a')
        chapters.reverse()
        for a in chapters:
            chap_id = len(self.chapters) + 1
            if len(self.chapters) % 100 == 0:
                vol_id = chap_id // 100 + 1
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({'id':vol_id, 
                 'title':vol_title})
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'url':self.absolute_url(a['href']), 
             'title':a.text.strip() or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select_one('div.entry-content.cl')
        for d in contents.findAll('div'):
            d.decompose()

        for comment in contents.find_all(string=(lambda text: isinstance(text, Comment))):
            comment.extract()

        if contents.findAll('p')[0].text.strip().startswith('Bab'):
            chapter['title'] = contents.findAll('p')[0].text.strip()
            contents.findAll('p')[0].extract()
        else:
            chapter['title'] = chapter['title']
        logger.debug(chapter['title'])
        return str(contents)
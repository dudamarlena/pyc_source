# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\novelplanet.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 3691 bytes
import json, logging, re
from slugify import slugify
from utils.crawler import Crawler
logger = logging.getLogger('NOVEL_PLANET')
search_url = 'https://novelplanet.com/NovelList?order=mostpopular&name=%s'

class NovelPlanetCrawler(Crawler):
    base_url = 'https://novelplanet.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('section a.title').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.post-previewInDetails img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        for span in soup.find_all('span', {'class': 'infoLabel'}):
            if span.text == 'Author:':
                author = span.findNext('a').text
                author2 = span.findNext('a').findNext('a').text

        if author2 != 'Ongoing' or author2 != 'Completed':
            self.novel_author = author + ' (' + author2 + ')'
        else:
            self.novel_author = author
        logger.info('Novel author: %s', self.novel_author)
        chapters = soup.find_all('div', {'class': 'rowChapter'})
        chapters.reverse()
        for x in chapters:
            chap_id = len(self.chapters) + 1
            if len(self.chapters) % 100 == 0:
                vol_id = chap_id // 100 + 1
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({'id':vol_id, 
                 'title':vol_title})
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'url':self.absolute_url(x.find('a')['href']), 
             'title':x.find('a')['title'] or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select_one('#divReadContent')
        logger.debug(soup.title.string)
        if soup.select_one('h4').text:
            chapter['title'] = soup.select_one('h4').text
        else:
            if chapter['title'].startswith('Read'):
                chapter['title'].replace('Read Novel ', '')
            else:
                chapter['title'] = chapter['title']
        for ads in contents.findAll('div', {'style': 'text-align: center; margin-bottom: 10px'}):
            ads.decompose()

        return str(contents)
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\scribblehub.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3605 bytes
import json, logging, re
from urllib.parse import quote
from utils.crawler import Crawler
from math import ceil
logger = logging.getLogger('SCRIBBLEHUB')
search_url = 'https://www.scribblehub.com/?s=%s&post_type=fictionposts'

class ScribbleHubCrawler(Crawler):
    base_url = 'https://www.scribblehub.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.find('div', {'class': 'fic_title'})['title'].strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.find('div', {'class': 'fic_image'}).find('img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = soup.find('span', {'class': 'auth_name_fic'}).text.strip()
        logger.info('Novel author: %s', self.novel_author)
        chapter_count = soup.find('span', {'class': 'cnt_toc'}).text
        chapter_count = -1 if not chapter_count else int(chapter_count)
        page_count = ceil(chapter_count / 15)
        logger.info('Chapter list pages: %d' % page_count)
        logger.info('Getting chapters...')
        chapters = []
        for i in range(page_count):
            chapters.extend(self.download_chapter_list(i + 1))
        else:
            for x in reversed(chapters):
                chap_id = len(self.chapters) + 1
                vol_id = len(self.chapters) // 100 + 1
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'url':self.absolute_url(x['href']), 
                 'title':x.text.strip() or 'Chapter %d' % chap_id})
            else:
                self.volumes = [{'id': x + 1} for x in range(len(self.chapters) // 100 + 1)]

    def download_chapter_list(self, page):
        """Download list of chapters and volumes."""
        url = self.novel_url.split('?')[0].strip('/')
        url += '?toc=%s#content1' % page
        soup = self.get_soup(url)
        logger.debug('Crawling chapters url in page %s' % page)
        return soup.select('a.toc_a')

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        logger.debug(soup.title.string)
        contents = soup.find('div', {'id': 'chp_contents'})
        return str(contents)
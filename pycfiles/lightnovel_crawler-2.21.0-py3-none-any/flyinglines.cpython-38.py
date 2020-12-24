# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\flyinglines.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2131 bytes
import json, logging, re
from urllib.parse import urlparse
from utils.crawler import Crawler
logger = logging.getLogger('FLYING LINES')
chapter_body_url = 'https://www.flying-lines.com/h5/novel/%s/%s?accessToken=&isFirstEnter=1&webdriver=0'

class FlyingLinesCrawler(Crawler):
    base_url = 'https://www.flying-lines.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('.novel-info .title h2').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.novel .novel-thumb img')['data-src'])
        logger.info('Novel cover: %s', self.novel_cover)
        authors = [x.text.strip() for x in soup.select('.novel-info ul.profile li')]
        self.novel_author = ', '.join(authors)
        logger.info('%s', self.novel_author)
        self.novel_id = urlparse(self.novel_url).path.split('/')[2]
        logger.info('Novel id: %s', self.novel_id)
        for a in soup.select('ul.volume-chapters li a'):
            chap_id = int(a['data-chapter-number'])
            vol_id = 1 + (chap_id - 1) // 100
            if len(self.chapters) % 100 == 0:
                self.volumes.append({'id': vol_id})
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'title':a.text.strip(), 
             'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        url = chapter_body_url % (self.novel_id, chapter['id'])
        logger.info('Downloading %s', url)
        response = self.submit_form(url)
        data = response.json()
        print(data)
        return data['data']['content']
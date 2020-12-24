# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\idqidian.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 2705 bytes
import json, logging, re
from utils.crawler import Crawler
logger = logging.getLogger('IDQIDIAN')

class IdqidianCrawler(Crawler):
    base_url = 'https://www.idqidian.us/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.find_all('span', {'typeof': 'v:Breadcrumb'})[(-1)].text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = 'https://www.idqidian.us/images/noavailable.jpg'
        logger.info('Novel cover: %s', self.novel_cover)
        author = soup.select('p')[3].text
        self.novel_author = author[20:len(author) - 22]
        logger.info('Novel author: %s', self.novel_author)
        chapters = soup.find('div', {'style': '-moz-border-radius: 5px 5px 5px 5px; border: 1px solid #333; color: black; height: 400px; margin: 5px; overflow: auto; padding: 5px; width: 96%;'}).findAll('a')
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
        for a in soup.find_all('a'):
            a.decompose()

        body_parts = soup.select('p')
        body_parts = ''.join([str(p.extract()) for p in body_parts if p.text.strip() if 'Advertisement' not in p.text if 'JavaScript!' not in p.text])
        if body_parts == '':
            texts = [str.strip(x) for x in soup.strings if str.strip(x) != '']
            unwanted_text = [str.strip(x.text) for x in soup.find_all()]
            my_texts = set(texts).difference(unwanted_text)
            body_parts = ''.join([str(p) for p in my_texts if p.strip() if 'Advertisement' not in p if 'JavaScript!' not in p])
        return body_parts
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/novelspread.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 2536 bytes
import hashlib, json, logging, re
from concurrent.futures import ThreadPoolExecutor
from ..utils.crawler import Crawler
logger = logging.getLogger('NOVEL_SPREAD')
book_info_url = 'https://api.novelspread.com/api/novel/path/%s'
chapter_list_url = 'https://api.novelspread.com/api/novel/%s/chapter/menu'
chapter_body_url = 'https://api.novelspread.com/api/novel/%s/chapter/%d/content?fingerprint='

class NovelSpreadCrawler(Crawler):
    base_url = 'https://www.novelspread.com/'

    def make_cover_url(self, image):
        a = '360'
        b = '512'
        c = '1'
        d = '90'
        r = a + b + c + d + image
        for i in range(2):
            m = hashlib.md5()
            m.update(r.encode())
            r = m.hexdigest()

        url = 'https://www.novelspread.com/image/%sx%s/%s/%s/%s/%s' % (
         a, b, d, c, r[:16], image)
        return url

    def read_novel_info(self):
        self.novel_id = self.novel_url.strip('/').split('/')[(-1)]
        logger.info('Novel id: %s' % self.novel_id)
        data = self.get_json(book_info_url % self.novel_id)
        self.novel_title = data['data']['name']
        logger.info('Title: %s' % self.novel_title)
        self.novel_author = 'Author: %s, Translator: %s' % (
         data['data']['author'], data['data']['translator'])
        logger.info(self.novel_author)
        self.novel_cover = self.make_cover_url(data['data']['img'])
        logger.info('Novel cover: %s', self.novel_cover)
        logger.info('Getting chapters...')
        data = self.get_json(chapter_list_url % self.novel_id)
        volumes = set([])
        for chap in data['data']:
            volumes.add(chap['volume'])
            self.chapters.append({'id':chap['chapter_number'], 
             'volume':chap['volume'], 
             'title':chap['title'], 
             'url':self.absolute_url(chap['link'])})

        self.volumes = [{'id':x,  'title':''} for x in volumes]
        logger.debug('%d chapters and %d volumes found', len(self.chapters), len(self.volumes))

    def download_chapter_body(self, chapter):
        url = chapter_body_url % (self.novel_id, chapter['id'])
        logger.info('Getting chapter... %s [%s]', chapter['title'], url)
        data = self.get_json(url)
        return data['data']['chapter_content']
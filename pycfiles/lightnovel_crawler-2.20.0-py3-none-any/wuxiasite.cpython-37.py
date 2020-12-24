# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\wuxiasite.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 3028 bytes
import json, logging, re
from utils.crawler import Crawler
logger = logging.getLogger('WUXIA-SITE')
search_url = 'https://wuxiaworld.site/?s=%s&post_type=wp-manga'

class WuxiaSiteCrawler(Crawler):
    base_url = 'https://wuxiaworld.site/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = ' '.join([str(x) for x in soup.select_one('.post-title h3').contents if not x.name]).strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.summary_image img')['data-src'])
        logger.info('Novel cover: %s', self.novel_cover)
        author = soup.find('div', {'class': 'author-content'}).findAll('a')
        if len(author) == 2:
            self.novel_author = author[0].text + ' (' + author[1].text + ')'
        else:
            self.novel_author = author[0].text
        logger.info('Novel author: %s', self.novel_author)
        chapters = soup.select('ul.main li.wp-manga-chapter a')
        chapters.reverse()
        for a in chapters:
            chap_id = len(self.chapters) + 1
            vol_id = chap_id // 100 + 1
            if len(self.chapters) % 100 == 0:
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
        contents = soup.select('.text-left p, .cha-words p')
        body = [str(p) for p in contents if p.text.strip()]
        return '<p>' + '</p><p>'.join(body) + '</p>'
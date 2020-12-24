# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/shinsori.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2867 bytes
import json, logging, re
from ..utils.crawler import Crawler
logger = logging.getLogger('SHINSORI')

class ShinsoriCrawler(Crawler):
    base_url = 'https://www.shinsori.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('span.the-section-title').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = None
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = 'Author : %s, Translator: Shinsori' % soup.select('div.entry.clearfix p strong')[1].next_sibling.strip()
        logger.info('Novel author: %s', self.novel_author)
        p_range = int(soup.select('ul.lcp_paginator li')[(-2)].text)
        chapters = []
        for x in range(p_range):
            p_url = '%s?lcp_page0=%d#lcp_instance_0 x+1' % (self.novel_url, x + 1)
            p_soup = self.get_soup(p_url)
            chapters.extend(p_soup.select('ul.lcp_catlist')[1].select('li a'))

        for x in chapters:
            chap_id = len(self.chapters) + 1
            vol_id = len(self.chapters) // 100 + 1
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'url':self.absolute_url(x['href']), 
             'title':x['title'] or 'Chapter %d' % chap_id})

        self.volumes = [{'id': x + 1} for x in range(len(self.chapters) // 100 + 1)]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        logger.debug(soup.title.string)
        content = soup.select_one('div.entry-content')
        for item in content.findAll('div', attrs={'class': None}):
            item.decompose()

        for item in content.findAll('style'):
            item.decompose()

        subs = 'tab'
        for item in content.findAll('div'):
            res = [x for x in item['class'] if re.search(subs, x)]
            if len(res) == 0:
                item.extract()

        for item in content.findAll('p'):
            if item.has_attr('style'):
                item.decompose()

        return str(content)
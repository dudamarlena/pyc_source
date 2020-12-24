# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/zenithnovels.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 3103 bytes
import json, logging, re, requests
from ..utils.crawler import Crawler
logger = logging.getLogger('ZENITH_NOVELS')
novel_url = 'http://zenithnovels.com/%s/'

class ZenithNovelsCrawler(Crawler):
    base_url = 'http://zenithnovels.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        self.novel_id = re.search('(?<=zenithnovels.com/)[^/]+', self.novel_url).group(0)
        logger.info('Novel id: %s', self.novel_id)
        url = novel_url % self.novel_id
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        self.novel_title = soup.select_one('article#the-post h1.name').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('article#the-post .entry img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        while True:
            self.parse_chapter_list(soup)
            next_link = soup.select_one('ul.lcp_paginator a.lcp_nextlink')
            if next_link:
                soup = self.get_soup(next_link['href'])
            else:
                break

        self.chapters.sort(key=(lambda x: x['volume'] * 1000000.0 + x['id']))
        self.volumes = [{'id':x,  'title':''} for x in set(self.volumes)]

    def parse_chapter_list(self, soup):
        for a in soup.select('ul.lcp_catlist li a'):
            ch_title = a['title']
            ch_id = [int(''.join(x).strip()) for x in re.findall('((?<=ch) \\d+)|((?<=chapter) \\d+)', ch_title, re.IGNORECASE)]
            ch_id = ch_id[0] if len(ch_id) else len(self.chapters) + 1
            vol_id = [int(''.join(x).strip()) for x in re.findall('((?<=book) \\d+)|((?<=volume) \\d+)', ch_title, re.IGNORECASE)]
            vol_id = vol_id[0] if len(vol_id) else 1 + (ch_id - 1) // 100
            self.volumes.append(vol_id)
            self.chapters.append({'id':ch_id, 
             'volume':vol_id, 
             'title':ch_title, 
             'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        entry = soup.select_one('article#the-post .entry')
        try:
            self.clean_contents(entry)
            for note in entry.select('.footnote'):
                note.decompose()

        except Exception:
            pass

        body = ''
        for tag in entry.children:
            if tag.name == 'p' and len(tag.text.strip()):
                p = ' '.join(self.extract_contents(tag))
                if len(p.strip()):
                    body += '<p>%s</p>' % p

        return body
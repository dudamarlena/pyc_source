# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\litnet.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 3150 bytes
import logging
from utils.crawler import Crawler
logger = logging.getLogger('LITNET')
search_url = 'https://litnet.com/en/search?q=%s'

class LitnetCrawler(Crawler):
    base_url = 'https://litnet.com/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)
        results = []
        for a in soup.select('div.l-container ul a'):
            results.append({'title':a.text.strip(), 
             'url':self.absolute_url(a['href'])})

        return results

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h1').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        img_src = soup.select_one('div.book-view-cover img')
        if not img_src:
            img_src = soup.select_one('div.book-cover img')
        if img_src:
            self.novel_cover = self.absolute_url(img_src['src'])
        else:
            logger.info('Novel cover: %s', self.novel_cover)
            author = soup.select_one('div.book-view-info a.author')
            if not author:
                author = soup.select_one('div.book-head-content a.book-autor')
            if author:
                self.novel_author = author.text.strip()
            logger.info('Novel author: %s', self.novel_author)
            chapters = soup.find('select', {'name': 'chapter'})
            if chapters is None:
                chapters = soup.select('div.collapsible-body a.collection-item')
            else:
                chapters = chapters.find_all('option')
            chapters = [c for c in chapters if c.attrs['value']]
        for a in chapters:
            chap_id = len(self.chapters) + 1
            if len(self.chapters) % 100 == 0:
                vol_id = chap_id // 100 + 1
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({'id':vol_id, 
                 'title':vol_title})
            abs_url = self.last_visited_url.replace('book', 'reader')
            chap_url = abs_url + '?c=%s' % a.attrs['value'] if a.has_attr('value') else self.home_url + a['href']
            self.chapters.append({'id':chap_id, 
             'volume':1, 
             'url':chap_url, 
             'title':a.text.strip() or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select_one('div.reader-text')
        if contents is None:
            contents = soup.select_one('div.demo-txt')
        return str(contents)
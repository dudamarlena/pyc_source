# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\novelall.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3547 bytes
import json, logging, re
from utils.crawler import Crawler
logger = logging.getLogger('NOVEL_All')
search_url = 'https://www.novelall.com/search/?name=%s'

class NovelAllCrawler(Crawler):
    base_url = 'https://www.novelall.com/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)
        results = []
        for a in soup.select('.cover-info p.title a')[:5]:
            url = self.absolute_url(a['href'])
            results.append({'url':url, 
             'title':a.text.strip(), 
             'info':self.search_novel_info(url)})
        else:
            return results

    def search_novel_info(self, url):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        chapters = soup.select_one('div.manga-detailchapter').findAll('a', title=True)
        info = '%d chapters' % len(chapters)
        latest = soup.select_one('div.manga-detailchapter').findAll('a', title=True)
        if latest:
            info += ' | Latest: ' + latest[0]['title']
        return info

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url + '?waring=1')
        self.novel_title = soup.find('div', {'class': 'manga-detail'}).find('h1').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.find('div', {'class': 'manga-detail'}).find('img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        author = soup.find('div', {'class': 'detail-info'}).find('a').text.split(',')
        if len(author) == 2:
            self.novel_author = author[0] + ' (' + author[1] + ')'
        else:
            self.novel_author = ' '.join(author)
        logger.info('Novel author: %s', self.novel_author)
        chapters = soup.find('div', {'class': 'manga-detailchapter'}).findAll('a', title=True)
        chapters.reverse()
        for a in chapters:
            for span in a.findAll('span'):
                span.decompose()

        else:
            for x in chapters:
                chap_id = len(self.chapters) + 1
                if len(self.chapters) % 100 == 0:
                    vol_id = chap_id // 100 + 1
                    vol_title = 'Volume ' + str(vol_id)
                    self.volumes.append({'id':vol_id, 
                     'title':vol_title})
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'url':self.absolute_url(x['href']), 
                 'title':x['title'] or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.find('div', {'class': 'reading-box'})
        self.clean_contents(contents)
        return str(contents)
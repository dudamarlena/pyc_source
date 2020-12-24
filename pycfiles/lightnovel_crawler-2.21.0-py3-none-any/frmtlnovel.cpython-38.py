# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\frmtlnovel.py
# Compiled at: 2020-05-04 18:46:42
# Size of source mod 2**32: 3534 bytes
import json, logging, re
from utils.crawler import Crawler
logger = logging.getLogger('IDMTLNOVEL')
search_url = 'https://fr.mtlnovel.com/wp-admin/admin-ajax.php?action=autosuggest&q=%s'

class FrMtlnovelCrawler(Crawler):
    base_url = 'https://fr.mtlnovel.com/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '%20')
        list_url = search_url % query
        data = self.get_json(list_url)['items'][0]['results']
        results = []
        for item in data:
            url = self.absolute_url('https://fr.mtlnovel.com/?p=%s' % item['id'])
            results.append({'url':url, 
             'title':item['title'], 
             'info':self.search_novel_info(url)})
        else:
            return results

    def search_novel_info(self, url):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        chapters = soup.select('div.info-wrap div')[1].text.replace('Chapters', '')
        info = '%s chapters' % chapters
        return info

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h1.entry-title').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select('div.nov-head amp-img')[1]['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = soup.select('table.info tr')[3].find('a').text
        logger.info('Novel author: %s', self.novel_author)
        chapter_list = soup.select('div.ch-list amp-list')
        for item in chapter_list:
            data = self.get_json(item['src'])
            for chapter in data['items']:
                chap_id = len(self.chapters) + 1
                if len(self.chapters) % 100 == 0:
                    vol_id = chap_id // 100 + 1
                    vol_title = 'Volume ' + str(vol_id)
                    self.volumes.append({'id':vol_id, 
                     'title':vol_title})
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'url':chapter['permalink'], 
                 'title':chapter['title'].strip(': ') or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        logger.debug(soup.title.string)
        contents = soup.select('div.par p')
        body = [str(p) for p in contents if p.text.strip()]
        return '<p>' + '</p><p>'.join(body) + '</p>'
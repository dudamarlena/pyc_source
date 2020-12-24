# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\9kqw.py
# Compiled at: 2020-05-04 18:37:19
# Size of source mod 2**32: 2645 bytes
import logging, re
from urllib.parse import parse_qsl, urlparse
from utils.crawler import Crawler
logger = logging.getLogger('9KQW')
chapter_details_url = 'https://9kqw.com/book/ajaxchap'

class TikNovelCrawler(Crawler):
    base_url = [
     'https://9kqw.com/',
     'http://www.tiknovel.com/',
     'https://www.tiknovel.com/']

    def initialize(self):
        self.base_url = 'https://9kqw.com/'

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('#content .detail-wrap h1.detail-tit').text
        logger.info('Novel title: %s', self.novel_title)
        possible_authors = soup.select('#content table.detail-profile td')
        for td in possible_authors:
            if '作者' in td.find('strong').text:
                td.find('strong').extract()
                self.novel_author = td.text.strip()
                break
            logger.info('Novel author: %s', self.novel_author)
            self.novel_cover = self.absolute_url(soup.select_one('#content .detail-thumb-box img')['data-echo'])
            logger.info('Novel cover: %s', self.novel_cover)
            volumes = set()

        for a in soup.select('#content .contents-lst li a'):
            ch_id = int(a.find('span').text.strip())
            vol_id = 1 + (ch_id - 1) // 100
            volumes.add(vol_id)
            self.chapters.append({'id':ch_id, 
             'volume':vol_id, 
             'title':a['title'], 
             'url':self.absolute_url(a['href'])})
        else:
            self.volumes = [{'id': x} for x in volumes]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        chapter['body_lock'] = True
        query_str = urlparse(chapter['url']).query
        data_params = {int(x[1]):x[0] for x in parse_qsl(query_str)}
        logging.debug('Requesting body with: %s', data_params)
        response = self.submit_form(chapter_details_url, data=data_params)
        data = response.json()
        chap_desc = data['data']['chap']['desc']
        chap_desc = re.sub('((<br\\/>)|\\n)+', '\n\n', chap_desc, flags=(re.I))
        contents = chap_desc.split('\n\n')
        contents = [p for p in contents if p if p.strip()]
        return '<p>' + '</p><p>'.join(contents) + '</p>'
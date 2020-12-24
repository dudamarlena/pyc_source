# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\novelraw.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 3417 bytes
import logging, re
from concurrent import futures
from urllib.parse import quote, urlparse
from utils.crawler import Crawler
logger = logging.getLogger('NOVELRAW_BLOGSPOT')
chapter_list_limit = 150
chapter_list_url = 'https://novelraw.blogspot.com/feeds/posts/default/-/%s?alt=json&start-index=%d&max-results=' + str(chapter_list_limit) + '&orderby=published'

class NovelRawCrawler(Crawler):
    base_url = 'https://novelraw.blogspot.com/'

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        for script in soup.select('#tgtPost script'):
            text = script.text.strip()
            pre = 'var label="'
            post = '";'
            if text.startswith(pre) and text.endswith(post):
                self.novel_title = text[len(pre):-len(post)]
                break

        logger.info('Novel title: %s', self.novel_title)
        url = chapter_list_url % (self.novel_title, 1)
        logger.debug('Visiting %s', url)
        data = self.get_json(url)
        self.novel_author = ', '.join([x['name']['$t'] for x in data['feed']['author']])
        logger.info('Novel author: %s', self.novel_author)
        self.novel_cover = soup.select_one('#tgtPost .separator img')['src']
        logger.info('Novel cover: %s', self.novel_cover)
        total_chapters = int(data['feed']['openSearch$totalResults']['$t'])
        logger.info('Total chapters = %d', total_chapters)
        logger.info('Getting chapters...')
        futures_to_check = {self.executor.submit(self.download_chapter_list, i):str(i) for i in range(1, total_chapters + 1, chapter_list_limit)}
        all_entry = dict()
        for future in futures.as_completed(futures_to_check):
            page = int(futures_to_check[future])
            all_entry[page] = future.result()

        for page in reversed(sorted(all_entry.keys())):
            for entry in reversed(all_entry[page]):
                possible_urls = [x['href'] for x in entry['link'] if x['rel'] == 'alternate']
                if not len(possible_urls):
                    continue
                self.chapters.append({'id':len(self.chapters) + 1, 
                 'volume':len(self.chapters) // 100 + 1, 
                 'title':entry['title']['$t'], 
                 'url':possible_urls[0]})

        self.volumes = [{'id': x + 1} for x in range(len(self.chapters) // 100 + 1)]

    def download_chapter_list(self, index):
        url = chapter_list_url % (self.novel_title, index)
        logger.debug('Visiting %s', url)
        data = self.get_json(url)
        return data['feed']['entry']

    def download_chapter_body(self, chapter):
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = self.extract_contents(soup.select_one('#tgtPost'))
        return '<p>' + '</p><p>'.join(contents) + '</p>'
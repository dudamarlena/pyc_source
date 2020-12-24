# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\fu_kemao.py
# Compiled at: 2020-05-04 20:02:42
# Size of source mod 2**32: 3993 bytes
import logging, re
from base64 import decodestring as b64decode
from concurrent import futures
from urllib.parse import quote_plus
from utils.crawler import Crawler
logger = logging.getLogger(__name__)
novel_search_url = b64decode('aHR0cHM6Ly9jb21yYWRlbWFvLmNvbS8/cG9zdF90eXBlPW5vdmVsJnM9'.encode()).decode()

class Fu_kCom_ademao(Crawler):
    base_url = b64decode('aHR0cHM6Ly9jb21yYWRlbWFvLmNvbS8='.encode()).decode()

    def search_novel(self, query):
        url = novel_search_url + quote_plus(query)
        soup = self.get_soup(url)
        results = []
        for a in soup.select('#novel a'):
            results.append({'title':a.text.strip(), 
             'url':self.absolute_url(a['href'])})
        else:
            return results

    def read_novel_info(self):
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('#novel-info h5, #recentnovels h5').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('#novel-info amp-img, #recentnovels amp-img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        page_count = 1
        pagination = soup.select_one('.pagination')
        if pagination:
            next_tag = pagination.select_one('.next')
            page_count = int(next_tag.findPrevious('a').text)
        logger.info('Total chapter pages: %d' % page_count)

        def parse_chapter_list(soup):
            temp_list = []
            for a in soup.select('#chapterList td a'):
                temp_list.append({'title':a.text.strip(), 
                 'url':self.absolute_url(a['href'])})
            else:
                return temp_list

        def download_chapter_list(page):
            url = self.novel_url.split('?')[0].strip('/') + '/page/%d' % page
            soup = self.get_soup(url)
            return parse_chapter_list(soup)

        logger.info('Getting chapters...')
        temp_chapters = dict()
        futures_to_check = dict()
        for page in range(1, page_count + 1):
            if page == 1:
                future = self.executor.submit(parse_chapter_list, soup)
            else:
                future = self.executor.submit(download_chapter_list, page)
            futures_to_check[page] = future
        else:
            for page, future in futures_to_check.items():
                temp_chapters[page] = future.result()
            else:
                logger.info('Building sorted chapter list...')
                for page in reversed(sorted(temp_chapters.keys())):
                    for chap in reversed(temp_chapters[page]):
                        chap['volume'] = page
                        chap['id'] = len(self.chapters) + 1
                        self.chapters.append(chap)

                else:
                    self.volumes = [{'id': i + 1} for i in range(page_count)]

    def download_chapter_body(self, chapter):
        soup = self.get_soup(chapter['url'])
        body = soup.select_one('#content, article')
        paragraphs = []
        for p in body.select('p'):
            if 'class' not in p.attrs and p.text.strip():
                paragraphs.append(str(p))
            return ''.join(paragraphs)
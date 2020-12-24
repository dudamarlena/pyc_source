# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/boxnovelorg.py
# Compiled at: 2020-03-05 23:56:06
# Size of source mod 2**32: 4948 bytes
import logging, re
from concurrent import futures
from ..utils.crawler import Crawler
logger = logging.getLogger('BOXNOVEL.ORG')
search_url = 'http://boxnovel.org/search?keyword=%s'

class BoxNovelOrgCrawler(Crawler):
    base_url = 'http://boxnovel.org/'

    def search_novel(self, query):
        query = query.lower().replace(' ', '+')
        soup = self.get_soup(search_url % query)
        results = []
        for tab in soup.select('.col-novel-main .list-novel .row'):
            search_title = tab.select_one('.novel-title a')
            latest = tab.select_one('.text-info a').text.strip()
            results.append({'title':search_title.text.strip(), 
             'url':self.absolute_url(tab.select_one('.novel-title a')['href']), 
             'info':'Latest chapter: %s' % latest})

        return results

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = ' '.join([str(x) for x in soup.select_one('.title').contents if not x.name]).strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.book img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        author = soup.find_all(href=(re.compile('author')))
        if len(author) == 2:
            self.novel_author = author[0].text + ' (' + author[1].text + ')'
        else:
            self.novel_author = author[0].text
        logger.info('Novel author: %s', self.novel_author)
        pagination_links = soup.select('.pagination li a')
        pagination_page_numbers = []
        for pagination_link in pagination_links:
            if pagination_link.text.isdigit():
                pagination_page_numbers.append(int(pagination_link.text))

        page_count = max(pagination_page_numbers) if pagination_page_numbers else 0
        logger.info('Chapter list pages: %d' % page_count)
        logger.info('Getting chapters...')
        futures_to_check = {self.executor.submit(self.download_chapter_list, i + 1):str(i) for i in range(page_count + 1)}
        [x.result() for x in futures.as_completed(futures_to_check)]
        logger.info('Sorting chapters...')
        self.chapters.sort(key=(lambda x: x['id']))
        logger.info('Adding volumes...')
        mini = self.chapters[0]['volume']
        maxi = self.chapters[(-1)]['volume']
        for i in range(mini, maxi + 1):
            self.volumes.append({'id':i, 
             'title':'Volume %d' % i, 
             'volume':str(i)})

    def download_chapter_list(self, page):
        """Download list of chapters and volumes."""
        url = self.novel_url.split('?')[0].strip('/')
        url += '?page=%d&per-page=50' % page
        soup = self.get_soup(url)
        for a in soup.select('ul.list-chapter li a'):
            title = a['title'].strip()
            chapter_id = len(self.chapters) + 1
            match = re.findall('ch(apter)? (\\d+)', title, re.IGNORECASE)
            if len(match) == 1:
                chapter_id = int(match[0][1])
            volume_id = 1 + (chapter_id - 1) // 100
            match = re.findall('(book|vol|volume) (\\d+)', title, re.IGNORECASE)
            if len(match) == 1:
                volume_id = int(match[0][1])
            data = {'title':title, 
             'id':chapter_id, 
             'volume':volume_id, 
             'url':self.absolute_url(a['href'])}
            self.chapters.append(data)

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select_one('div.chr-c')
        return str(contents)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/noveluniverse.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3709 bytes
import re, logging
from concurrent import futures
from ..utils.crawler import Crawler
logger = logging.getLogger('NOVEL_UNIVERSE')
novel_info_url = 'https://www.noveluniverse.com/index/novel/info/id/%s.html'
chapter_page_url = '%s?id=%s&page_c=%d'

class NovelUniverseCrawler(Crawler):
    base_url = 'https://www.noveluniverse.com/'

    def read_novel_info(self):
        self.novel_id = self.novel_url.split('/')[(-1)].split('.')[0]
        logger.info('Novel Id: %s', self.novel_id)
        self.novel_url = novel_info_url % self.novel_id
        logger.info('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        book_info = soup.select_one('.book_info')
        if not book_info:
            raise Exception('Invalid content')
        else:
            self.novel_title = book_info.select_one('h1.books_name').text.strip()
            logger.info('Title: %s', self.novel_title)
            self.novel_author = []
            for tag in book_info.select_one('.info_more'):
                if not tag.name and len(str(tag).strip()):
                    self.novel_author.append(str(tag))

            self.novel_author = ', '.join(self.novel_author).strip()
            logger.info(self.novel_author)
            self.novel_cover = self.absolute_url(book_info.select_one('.img img')['src'])
            logger.info('Cover: %s', self.novel_cover)
            max_page = soup.select('.allPagesStyle a')
            if len(max_page) > 1:
                max_page = int(max_page[(-2)].text)
            else:
                max_page = 1
        logger.info('Pagination length: %d', max_page)
        tasks = {self.executor.submit(self.get_chapter_list, chapter_page_url % (self.novel_url, self.novel_id, i)):i for i in range(1, max_page + 1)}
        [x.result() for x in futures.as_completed(tasks)]
        self.chapters.sort(key=(lambda x: x['id']))
        self.volumes = [{'id':x,  'title':''} for x in set(self.volumes)]
        logger.info('%d chapters and %d volumes found', len(self.chapters), len(self.volumes))

    def get_chapter_list(self, url):
        logger.info('Visiting %s', url)
        soup = self.get_soup(url)
        for a in soup.select('ul#chapters li a'):
            chapter_id = a.select_one('span').text
            chapter_id = int([x for x in re.findall('\\d+', chapter_id)][0])
            volume_id = 1 + (chapter_id - 1) // 100
            chapter_title = ' '.join([str(x).strip() for x in a.contents if not x.name if str(x).strip()]).strip()
            chapter_title = 'Chapter %d: %s' % (chapter_id, chapter_title)
            self.volumes.append(volume_id)
            self.chapters.append({'id':chapter_id, 
             'url':self.absolute_url(a['href']), 
             'title':chapter_title, 
             'volume':volume_id})

    def download_chapter_body(self, chapter):
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        body = []
        for p in soup.select('div#content .overHide p.data-discuss'):
            para = ' '.join(self.extract_contents(p))
            if len(para):
                body.append(para)

        return '<p>%s</p>' % '</p><p>'.join(body)
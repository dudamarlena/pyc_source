# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\novelsrock.py
# Compiled at: 2020-05-04 19:33:14
# Size of source mod 2**32: 3401 bytes
import json, logging, re
from urllib.parse import quote_plus
from utils.crawler import Crawler
logger = logging.getLogger('NOVELSROCK')
search_url = 'https://novelsrock.com/?s=%s&post_type=wp-manga&op=&author=&artist=&release=&adult='
post_chapter_url = 'https://novelsrock.com/wp-admin/admin-ajax.php'

class NovelsRockCrawler(Crawler):
    base_url = 'https://novelsrock.com/'

    def search_novel(self, query):
        query = quote_plus(query.lower())
        soup = self.get_soup(search_url % query)
        results = []
        for tab in soup.select('.c-tabs-item__content')[:10]:
            a = tab.select_one('.post-title .h4 a')
            latest = tab.select_one('.latest-chap .chapter a').text
            votes = tab.select_one('.rating .total_votes').text
            results.append({'title':a.text.strip(), 
             'url':self.absolute_url(a['href']), 
             'info':'%s | Rating: %s' % (latest, votes)})
        else:
            return results

    def read_novel_info(self):
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = ' '.join([str(x) for x in soup.select_one('.post-title h1').contents if not x.name]).strip()
        logger.info('Novel title: %s', self.novel_title)
        try:
            self.novel_cover = self.absolute_url(soup.select_one('.summary_image img')['data-src'])
        except Exception:
            pass
        else:
            logger.info('Novel cover: %s', self.novel_cover)
            author = soup.select('.author-content a')
            if len(author) == 2:
                self.novel_author = author[0].text + ' (' + author[1].text + ')'
            else:
                self.novel_author = author[0].text
            logger.info('Novel author: %s', self.novel_author)
            self.novel_id = soup.select_one('.wp-manga-action-button[data-action=bookmark]')['data-post']
            logger.info('Novel id: %s', self.novel_id)
            for span in soup.select('.page-content-listing span'):
                span.decompose()
            else:
                logger.info('Sending post request to %s', post_chapter_url)
                response = self.submit_form(post_chapter_url, data={'action':'manga_get_chapters', 
                 'manga':int(self.novel_id)})
                soup = self.make_soup(response)
                for a in reversed(soup.select('.wp-manga-chapter > a')):
                    chap_id = len(self.chapters) + 1
                    vol_id = chap_id // 100 + 1
                    if len(self.chapters) % 100 == 0:
                        self.volumes.append({'id': vol_id})
                    self.chapters.append({'id':chap_id, 
                     'volume':vol_id, 
                     'title':a.text.strip(), 
                     'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        contents = soup.select('div.reading-content p')
        body = []
        for p in contents:
            for ad in p.select('h3, .code-block, .adsense-code'):
                ad.decompose()
            else:
                body.append(str(p))

        else:
            return ''.join(body)
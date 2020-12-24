# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/tomotrans.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 2452 bytes
import logging, re
from ..utils.crawler import Crawler
logger = logging.getLogger('TOMO_TRANSLATIONS')

class TomoTransCrawler(Crawler):
    base_url = 'https://tomotranslations.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('article h1.title').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('article figure.wp-block-image img')['data-orig-file'])
        logger.info('Novel cover: %s', self.novel_cover)
        author = 'Tomo Translations'
        logger.info('Novel author: %s', self.novel_author)
        volumes = set()
        for a in soup.select('article section.entry a[href^="%s"]' % self.home_url):
            chap_id = len(self.chapters) + 1
            chap_url = self.absolute_url(a['href'])
            possible_vol = re.findall('-volume-(\\d+)-', chap_url)
            if not len(possible_vol):
                pass
            else:
                vol_id = int(possible_vol[0])
                volumes.add(vol_id)
                self.chapters.append({'id':chap_id, 
                 'volume':vol_id, 
                 'url':chap_url, 
                 'title':a.text.strip()})

        self.volumes = [{'id': x} for x in volumes]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        body = ''
        for tag in soup.select('article section.entry > *'):
            if tag.name == 'hr' and tag.has_attr('class') and 'is-style-dots' in tag.get('class'):
                body += '<p>—————–</p>'
            else:
                if tag.name == 'p':
                    if tag.find('strong'):
                        chapter['title'] = tag.text.strip()
                    else:
                        if tag.find('a'):
                            if re.match('Previous|Next', tag.find('a').text):
                                continue
                        body += str(tag)

        return body
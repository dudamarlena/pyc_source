# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\webnovelonlinecom.py
# Compiled at: 2020-05-04 20:16:36
# Size of source mod 2**32: 2079 bytes
import re, json, logging
from utils.crawler import Crawler
logger = logging.getLogger('WEBNOVELONLINE_DOT_COM')

class WebnovelOnlineDotComCrawler(Crawler):
    base_url = 'https://webnovelonline.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        url = self.novel_url
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        self.novel_title = soup.select_one('.novel-info .novel-desc h1').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = soup.select_one('meta[property="og:image"]')['content']
        logger.info('Novel cover: %s', self.novel_title)
        volumes = set([])
        for a in reversed(soup.select('.chapter-list .item a')):
            chap_id = len(self.chapters) + 1
            vol_id = 1 + len(self.chapters) // 100
            volumes.add(vol_id)
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'title':a.text.strip(), 
             'url':self.absolute_url(a['href'])})
        else:
            self.volumes = [{'id':x,  'title':''} for x in volumes]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        for script in soup.select('script'):
            text = script.text.strip()
            print(text)
            if not text.startswith('window._INITIAL_DATA_'):
                pass
            else:
                content = re.findall(',"chapter":(".+")},', text)[0]
                content = json.loads(content).strip()
                return '<p>' + '</p><p>'.join(content.split('\n\n')) + '</p>'
                return ''
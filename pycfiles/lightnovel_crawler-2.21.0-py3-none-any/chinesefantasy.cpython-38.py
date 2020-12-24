# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\chinesefantasy.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 1914 bytes
from utils.crawler import Crawler
import requests, re, logging, json
logger = logging.getLogger('CHINESE_FANTASY_NOVELS')

class ChineseFantasyNovels(Crawler):
    base_url = 'https://m.chinesefantasynovels.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        if not self.novel_url.endswith('/'):
            self.novel_url += '/'
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('.btitle h1').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_author = soup.select_one('.bookinfo .status').text
        logger.info('%s', self.novel_author)
        volumes = set([])
        for a in reversed(soup.select('dl.chapterlist a')):
            ch_title = a.text.strip()
            ch_id = [int(x) for x in re.findall('\\d+', ch_title)]
            ch_id = ch_id[0] if len(ch_id) else len(self.chapters) + 1
            vol_id = 1 + len(self.chapters) // 100
            volumes.add(vol_id)
            self.chapters.append({'id':ch_id, 
             'volume':vol_id, 
             'title':ch_title, 
             'url':self.absolute_url(a['href'])})
        else:
            self.volumes = [{'id':x,  'title':''} for x in volumes]

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        content = soup.select_one('#BookText')
        content.select_one('.link').decompose()
        body = self.extract_contents(content)
        return '<p>' + '</p><p>'.join(body) + '</p'
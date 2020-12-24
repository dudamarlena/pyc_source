# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\webnovelonline.py
# Compiled at: 2020-01-01 14:22:44
# Size of source mod 2**32: 1992 bytes
import re, logging
from utils.crawler import Crawler
logger = logging.getLogger('WEBNOVEL_ONLINE')

class WebnovelOnlineCrawler(Crawler):
    base_url = 'https://webnovel.online/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        url = self.novel_url
        logger.debug('Visiting %s', url)
        soup = self.get_soup(url)
        img = soup.select_one('main img.cover')
        self.novel_title = img['title'].strip()
        self.novel_cover = self.absolute_url(img['src'])
        span = soup.select_one('header span.send-author-event')
        if span:
            self.novel_author = span.text.strip()
        chap_id = 0
        for a in soup.select('#info a.on-navigate-part'):
            vol_id = chap_id // 100 + 1
            if vol_id > len(self.volumes):
                self.volumes.append({'id':vol_id, 
                 'title':'Volume %d' % vol_id})
            chap_id += 1
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'title':a.text.strip(), 
             'url':self.absolute_url(a['href'])})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        strong = soup.select_one('#story-content strong')
        if strong:
            if re.search('Chapter \\d+', strong.text):
                chapter['title'] = strong.text.strip()
                logger.info('Updated title: %s', chapter['title'])
        self.bad_tags += ['h1', 'h3', 'hr']
        contents = soup.select_one('#story-content')
        body = self.extract_contents(contents)
        return '<p>' + '</p><p>'.join(body) + '</p>'
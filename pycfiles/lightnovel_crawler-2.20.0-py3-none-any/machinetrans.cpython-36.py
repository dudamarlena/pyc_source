# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/machinetrans.py
# Compiled at: 2020-03-23 11:49:43
# Size of source mod 2**32: 2683 bytes
import json, logging, re
from ..utils.crawler import Crawler
logger = logging.getLogger('MACHINE_NOVEL_TRANSLATION')
search_url = 'http://www.machinenoveltranslation.com/search/autocomplete'

class MachineNovelTrans(Crawler):
    base_url = 'http://www.machinenoveltranslation.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('.desc h5').text
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('.about-author .row img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        for div in soup.select('#chapters #accordion .panel'):
            vol_title = div.select_one('h4.panel-title a').text
            vol_id = [int(x) for x in re.findall('\\d+', vol_title)]
            vol_id = vol_id[0] if len(vol_id) else len(self.volumes) + 1
            self.volumes.append({'id':vol_id, 
             'title':vol_title})
            for a in div.select('ul.navigate-page li a'):
                ch_title = a.text
                ch_id = [int(x) for x in re.findall('\\d+', ch_title)]
                ch_id = ch_id[0] if len(ch_id) else len(self.chapters) + 1
                self.chapters.append({'id':ch_id, 
                 'volume':vol_id, 
                 'title':ch_title, 
                 'url':self.absolute_url(a['href'])})

        logger.debug('%d chapters and %d volumes found', len(self.chapters), len(self.volumes))

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        body = soup.select('.about-author .desc .translated')
        body = [self.format_text(x.text) for x in body if x]
        body = '\n'.join(['<p>%s</p>' % x for x in body if len(x)])
        return body.strip()

    def format_text(self, text):
        """formats the text and remove bad characters"""
        text = re.sub('\\u00ad', '', text, flags=(re.UNICODE))
        text = re.sub('\\u201e[, ]*', '&ldquo;', text, flags=(re.UNICODE))
        text = re.sub('\\u201d[, ]*', '&rdquo;', text, flags=(re.UNICODE))
        text = re.sub('[ ]*,[ ]+', ', ', text, flags=(re.UNICODE))
        return text.strip()
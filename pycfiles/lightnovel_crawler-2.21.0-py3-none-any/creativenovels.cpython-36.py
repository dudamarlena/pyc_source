# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/creativenovels.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 4235 bytes
import logging, re
from concurrent import futures
from urllib.parse import parse_qs, urlparse
from ..utils.crawler import Crawler
logger = logging.getLogger('CREATIVE_NOVELS')
chapter_list_url = 'https://creativenovels.com/wp-admin/admin-ajax.php'
chapter_s_regex = 'var chapter_list_summon = {"ajaxurl":"https:\\/\\/creativenovels.com\\/wp-admin\\/admin-ajax.php","security":"([^"]+)"}'

class CreativeNovelsCrawler(Crawler):
    base_url = 'https://creativenovels.com/'

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        shortlink = soup.find('link', {'rel': 'shortlink'})['href']
        self.novel_id = parse_qs(urlparse(shortlink).query)['p'][0]
        logger.info('Id: %s', self.novel_id)
        self.novel_title = soup.select_one('head title').text
        self.novel_title = self.novel_title.split('–')[0].strip()
        logger.info('Novel title: %s', self.novel_title)
        try:
            self.novel_cover = self.absolute_url(soup.select_one('.x-bar-content-area img.book_cover')['src'])
            logger.info('Novel Cover: %s', self.novel_cover)
        except Exception:
            pass

        for div in soup.select('.x-bar-content .x-text.bK_C'):
            text = div.text.strip()
            if re.search('author|translator', text, re.I):
                self.novel_author = text
                break

        logger.info(self.novel_author)
        list_security_key = ''
        for script in soup.select('script'):
            text = script.text
            if 'var chapter_list_summon' not in text:
                continue
            p = re.findall('"([^"]+)"', text)
            if p[0] == 'ajaxurl' and p[1] == 'https:\\/\\/creativenovels.com\\/wp-admin\\/admin-ajax.php' and p[2] == 'security':
                list_security_key = p[3]

        logger.debug('Chapter list security = %s', list_security_key)
        response = self.submit_form(chapter_list_url,
          data=dict(action='crn_chapter_list',
          view_id=(self.novel_id),
          s=list_security_key))
        self.parse_chapter_list(response.content.decode('utf-8'))

    def parse_chapter_list(self, content):
        if not content.startswith('success'):
            return
        content = content[len('success.define.'):]
        for data in content.split('.end_data.'):
            parts = data.split('.data.')
            if len(parts) < 2:
                pass
            else:
                url = parts[0]
                title = parts[1]
                ch_id = len(self.chapters) + 1
                vol_id = (ch_id - 1) // 100 + 1
                self.volumes.append(vol_id)
                self.chapters.append({'id':ch_id, 
                 'url':url, 
                 'title':title, 
                 'volume':vol_id})

        self.volumes = [{'id': x} for x in set(self.volumes)]
        logger.info('%d chapters and %d volumes found', len(self.chapters), len(self.volumes))

    def download_chapter_body(self, chapter):
        logger.info('Visiting %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        body = soup.select_one('article .entry-content')
        for tag in body.select('.announcements_crn'):
            tag.decompose()

        for span in body.find_all('span'):
            span.decompose()

        for span in body.find_all('style'):
            span.decompose()

        self.clean_contents(body)
        return str(body)
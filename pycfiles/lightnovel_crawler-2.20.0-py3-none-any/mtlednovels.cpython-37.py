# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\sources\mtlednovels.py
# Compiled at: 2020-03-23 11:49:43
# Size of source mod 2**32: 4807 bytes
import json, logging, re
from bs4 import BeautifulSoup
from utils.crawler import Crawler
logger = logging.getLogger('MTLED-NOVELS')
search_url = 'https://mtled-novels.com/search_novel.php?q=%s'
login_url = 'https://mtled-novels.com/login/ajax/checklogin.php'
logout_url = 'https://mtled-novels.com/login/logout.php'

class MtledNovelsCrawler(Crawler):
    base_url = 'https://mtled-novels.com/'

    def login(self, username, password):
        """login to LNMTL"""
        logger.info('Visiting %s', self.home_url)
        self.get_response(self.home_url)
        logger.info('Logging in...')
        response = self.submit_form(login_url,
          data=dict(myusername=username,
          mypassword=password,
          remember=0))
        data = response.json()
        logger.debug(data)
        if 'response' in data and data['response'] == 'true':
            print('Logged In')
        else:
            soup = BeautifulSoup(data['response'], 'lxml')
            soup.find('button').extract()
            error = soup.find('div').text.strip()
            raise PermissionError(error)

    def logout(self):
        """logout as a good citizen"""
        logger.debug('Logging out...')
        self.get_response(logout_url)
        print('Logged out')

    def read_novel_info(self):
        """Get novel title, autor, cover etc"""
        logger.debug('Visiting %s', self.novel_url)
        soup = self.get_soup(self.novel_url)
        self.novel_title = soup.select_one('h1').text.strip()
        logger.info('Novel title: %s', self.novel_title)
        self.novel_cover = self.absolute_url(soup.select_one('div.profile__img img')['src'])
        logger.info('Novel cover: %s', self.novel_cover)
        self.novel_author = 'Downloaded from mtled-novels.com'
        logger.info('Novel author: %s', self.novel_author)
        chapters = soup.select('div#tab-profile-2 a')
        for a in chapters:
            chap_id = len(self.chapters) + 1
            if len(self.chapters) % 100 == 0:
                vol_id = chap_id // 100 + 1
                vol_title = 'Volume ' + str(vol_id)
                self.volumes.append({'id':vol_id, 
                 'title':vol_title})
            self.chapters.append({'id':chap_id, 
             'volume':vol_id, 
             'url':self.absolute_url(a['href']), 
             'title':a.text.strip() or 'Chapter %d' % chap_id})

    def download_chapter_body(self, chapter):
        """Download body of a single chapter and return as clean html format."""
        logger.info('Downloading %s', chapter['url'])
        soup = self.get_soup(chapter['url'])
        logger.debug(soup.title.string)
        if soup.h1.text.strip():
            chapter['title'] = soup.h1.text.strip()
        else:
            chapter['title'] = chapter['title']
        self.blacklist_patterns = [
         '^translat(ed by|or)',
         '(volume|chapter) .?\\d+']
        contents = soup.select('div.translated p')
        for p in contents:
            for span in p.findAll('span'):
                span.unwrap()

        body = [str(p) for p in contents if p.text.strip()]
        return '<p>' + '</p><p>'.join(body) + '</p>'
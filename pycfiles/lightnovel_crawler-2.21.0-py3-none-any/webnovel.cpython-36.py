# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/sources/webnovel.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 5786 bytes
import json, logging, re
from ..utils.crawler import Crawler
logger = logging.getLogger('WEBNOVEL')
book_info_url = 'https://www.webnovel.com/book/%s'
chapter_info_url = 'https://www.webnovel.com/book/%s/%s'
book_cover_url = 'https://img.webnovel.com/bookcover/%s/600/600.jpg'
chapter_list_url = 'https://www.webnovel.com/apiajax/chapter/GetChapterList?_csrfToken=%s&bookId=%s'
chapter_body_url = 'https://www.webnovel.com/apiajax/chapter/GetContent?_csrfToken=%s&bookId=%s&chapterId=%s'
search_url = 'https://www.webnovel.com/apiajax/search/AutoCompleteAjax'

class WebnovelCrawler(Crawler):
    base_url = 'https://www.webnovel.com'

    def get_csrf(self):
        logger.info('Getting CSRF Token')
        self.get_response(self.home_url)
        self.csrf = self.cookies['_csrfToken']
        logger.debug('CSRF Token = %s', self.csrf)

    def search_novel(self, query):
        self.get_csrf()
        response = self.submit_form(search_url, {'_csrfToken':self.csrf, 
         'keywords':query})
        data = response.json()
        logger.debug(data)
        results = []
        if 'books' not in data['data']:
            return results
        else:
            for book in data['data']['books']:
                results.append({'title':book['name'], 
                 'url':book_info_url % book['id']})

            return results

    def read_novel_info(self):
        self.get_csrf()
        url = self.novel_url
        self.novel_id = re.search('(?<=webnovel.com/book/)\\d+', url).group(0)
        logger.info('Novel Id: %s', self.novel_id)
        url = chapter_list_url % (self.csrf, self.novel_id)
        logger.info('Downloading novel info from %s', url)
        response = self.get_response(url)
        data = response.json()['data']
        if 'bookInfo' in data:
            self.novel_title = data['bookInfo']['bookName']
            self.novel_cover = book_cover_url % self.novel_id
        chapterItems = []
        if 'volumeItems' in data:
            for vol in data['volumeItems']:
                vol_id = vol['index'] or len(self.volumes) + 1
                vol_title = vol['name'].strip() or 'Volume %d' % vol_id
                self.volumes.append({'id':vol_id, 
                 'title':vol_title})
                for chap in vol['chapterItems']:
                    chap['volume'] = vol_id
                    chapterItems.append(chap)

        else:
            if 'chapterItems' in data:
                chapterItems = data['chapterItems']
                for vol in range(len(chapterItems) // 100 + 1):
                    self.volumes.append({'id':vol, 
                     'title':'Volume %d' % vol + 1})

        for i, chap in enumerate(chapterItems):
            if chap['isVip'] > 0:
                pass
            else:
                self.chapters.append({'id':i + 1, 
                 'hash':chap['id'], 
                 'title':'Chapter %s: %s' % (chap['index'], chap['name'].strip()), 
                 'url':chapter_body_url % (self.csrf, self.novel_id, chap['id']), 
                 'volume':chap['volume'] if 'volume' in chap else 1 + i // 100})

    def get_chapter_index_of(self, url):
        if not url:
            return 0
        else:
            url = url.replace('http://', 'https://')
            for chap in self.chapters:
                chap_url = chapter_info_url % (self.novel_id, chap['hash'])
                if url.startswith(chap_url):
                    return chap['id']

            return 0

    def download_chapter_body(self, chapter):
        url = chapter['url']
        logger.info('Getting chapter... %s [%s]', chapter['title'], chapter['id'])
        response = self.get_response(url)
        data = response.json()['data']
        if 'authorName' in data['bookInfo']:
            self.novel_author = data['bookInfo']['authorName'] or self.novel_author
        if 'authorItems' in data['bookInfo']:
            self.novel_author = ', '.join([x['name'] for x in data['bookInfo']['authorItems']]) or self.novel_author
        chapter_info = data['chapterInfo']
        if 'content' in chapter_info:
            body = chapter_info['content']
            body = re.sub('[\\n\\r]+', '\n', body)
            return self.format_text(body)
        if 'contents' in chapter_info:
            body = [re.sub('[\\n\\r]+', '\n', x['content']) for x in chapter_info['contents'] if x['content'].strip()]
            return self.format_text('\n'.join(body))

    def format_text(self, text):
        text = re.sub('Find authorized novels in Webnovel(.*)for visiting\\.', '', text, re.MULTILINE)
        text = re.sub('\\<pirate\\>(.*?)\\<\\/pirate\\>', '', text, re.MULTILINE)
        if not ('<p>' in text and '</p>' in text):
            text = re.sub('<', '&lt;', text)
            text = re.sub('>', '&gt;', text)
            text = [x.strip() for x in text.split('\n') if x.strip()]
            text = '<p>' + '</p><p>'.join(text) + '</p>'
        return text.strip()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\extractors\mangadex.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 11529 bytes
"""This module contains the MangaDex extractor class"""
import os, re, json
from argparse import Namespace
import multiprocessing.dummy as ThreadPool
from bs4 import BeautifulSoup
from komidl.status import prompt
from komidl.exceptions import ExtractorFailed
from .extractor import Extractor

class MangaDexEX(Extractor):
    __doc__ = '\n    An extractor for MangaDex.org\n    '
    _STATUS_DICT = {1:'Ongoing',  2:'Completed',  None:'Unknown'}
    _GENRE_DICT = {1:'4-Koma',  2:'Action',  3:'Adventure',  4:'Award Winning', 
     5:'Comedy',  6:'Cooking',  7:'Doujinshi', 
     8:'Drama',  9:'Ecchi',  10:'Fantasy', 
     11:'Gender Bender',  12:'Harem',  13:'Historical', 
     14:'Horror',  15:'Josei',  16:'Martial Arts', 
     17:'Mecha',  18:'Medical',  19:'Music', 
     20:'Mystery',  21:'Oneshot',  22:'Psychological', 
     23:'Romance',  24:'School Life', 
     25:'Sci-Fi',  26:'Seinen',  27:'Shoujo', 
     28:'Shoujo Ai',  29:'Shounen',  30:'Shounen Ai', 
     31:'Slice of Life',  32:'Smut',  33:'Sports', 
     34:'Supernatural',  35:'Tragedy',  36:'Webtoon', 
     37:'Yaoi',  38:'Yuri',  39:'[no chapters]', 
     40:'Game',  41:'Isekai'}

    def __init__(self):
        super().__init__()
        self.name = 'MangaDex'
        self.url = 'https://www.mangadex.org'
        self._PAGE_PATTERN = 'https?://(?:www\\.)?mangadex\\.org.*'
        self._CHAPTER_PATTERN = 'https?://(?:www\\.)?mangadex\\.org/chapter/[0-9]+/[0-9]+/?'
        self._MANGA_PATTERN = 'https?://(?:www\\.)?mangadex\\.org/title/[0-9]+/[a-z-]+/?'
        self._POST_API = 'https://mangadex.org/api/?id='
        self._IMG_DOMAIN = 'https://mangadex.org/data/'
        self._MangaDexEX__manga_data = None
        self._MangaDexEX__chapter_data = None
        self._MangaDexEX__chapter_data_list = []

    def is_gallery(self, url):
        return self._is_chapter(url) or self._is_manga(url)

    def _is_chapter(self, url):
        return bool(re.match(self._CHAPTER_PATTERN, url))

    def _is_manga(self, url):
        return bool(re.match(self._MANGA_PATTERN, url))

    @staticmethod
    def _is_multilang(m_data: dict) -> bool:
        """Return number of different languages for all chapters in m_data"""
        lang_list = {m_data['chapter'][ch_id]['lang_code'] for ch_id in m_data['chapter'].keys()}
        return len(lang_list) > 1

    def reset(self):
        """Clear all instance variables"""
        self._MangaDexEX__manga_data = None
        self._MangaDexEX__chapter_data = None
        self._MangaDexEX__chapter_data_list = []

    def _post_request(self, id_: int, type_: str) -> dict:
        """Make a POST request for JSON data and return decoded response"""
        data_url = f"{self._POST_API}{id_}&type={type_}"
        response = self._session.get(data_url, verify=False)
        response.raise_for_status()
        return json.loads(response.content.decode('utf-8'))

    def _chapter_data(self, chapter_id: int) -> dict:
        """Return the chapter data.

        If not stored in memory, makes a POST request.
        """
        if self._MangaDexEX__chapter_data is None:
            self._MangaDexEX__chapter_data = self._post_request(chapter_id, 'chapter')
        return self._MangaDexEX__chapter_data

    def _manga_data(self, manga_id: int) -> dict:
        """Return the manga data.

        If not stored in memory, makes a POST request.
        """
        if self._MangaDexEX__manga_data is None:
            self._MangaDexEX__manga_data = self._post_request(manga_id, 'manga')
        return self._MangaDexEX__manga_data

    def _chapter_data_list(self, m_data: dict, args: Namespace) -> dict:
        """Return the chapter data list"""
        if not self._MangaDexEX__chapter_data_list:
            pool = ThreadPool(args.thread_size)
            url_list = [ch_id for ch_id in m_data['chapter'].keys() if m_data['chapter'][ch_id]['lang_code'] in args.lang]
            if not url_list:
                if self._is_multilang(m_data):
                    raise ValueError(f"Preferred language ({args.lang[0]}) " + 'not found')
                print(f"Warning: Preferred language ({args.lang[(-1)]}) " + 'not found')
                dl = prompt('Download gallery in only available language?', skip=(args.yes))
                if not dl:
                    raise ValueError(f"Preferred language ({args.lang[0]}) " + 'not found')
                url_list = m_data['chapter']
            self._MangaDexEX__chapter_data_list = pool.starmap(self._chapter_data, url_list)
        return self._MangaDexEX__chapter_data_list

    @staticmethod
    def _get_data_id(url: str) -> int:
        """Get the ID of the for data GET request"""
        return int(url.split('/')[(-3)] if url[(-1)] == '/' else url.split('/')[(-2)])

    @staticmethod
    def _get_size_data(c_data: dict) -> int:
        """From a chapter data, retrieve size"""
        return int(len(c_data['page_array']))

    @staticmethod
    def _get_title(m_data: dict) -> str:
        """Get title of manga from manga_data"""
        return m_data['manga']['title']

    @staticmethod
    def _get_artist(m_data: dict) -> str:
        return m_data['manga']['artist']

    @staticmethod
    def _get_author(m_data: dict) -> str:
        return m_data['manga']['author']

    def get_size(self, url: str, soup: BeautifulSoup, args: Namespace) -> int:
        """Get the number of images to download"""
        if self._is_manga(url):
            m_id = self._get_data_id(url)
            m_data = self._manga_data(m_id)
            chapter_data_list = self._chapter_data_list(m_data, args)
            return sum((self._get_size_data(chapter) for chapter in chapter_data_list))
        if self._is_chapter(url):
            chapter_id = self._get_data_id(url)
            chapter_data = self._chapter_data(chapter_id)
            return self._get_size_data(chapter_data)
        raise ExtractorFailed(f"Could not get size of url: {url}")

    def _get_chapter_urls(self, c_data: dict, ch_path: str='') -> list:
        """Same output as get_gallery_urls, but for a single chapter"""
        url_list = []
        size = self._get_size_data(c_data)
        size_len = len(str(abs(size)))
        for img_num, sub_url in enumerate(c_data['page_array']):
            img_type = sub_url.split('.')[(-1)]
            img_name = f"{str(img_num + 1).zfill(size_len)}.{img_type}"
            filename = os.path.join(ch_path, img_name)
            img_host = c_data['server'] if c_data['server'] == '/data/' else self._IMG_DOMAIN
            img_url = f"{img_host}{c_data['hash']}/{sub_url}"
            url_list.append([filename, img_url])

        return url_list

    def _get_manga_urls(self, url: str, args: Namespace) -> list:
        """Same output as get_gallery_urls, but for all chapters of a manga"""
        url_list = []
        m_id = self._get_data_id(url)
        m_data = self._manga_data(m_id)
        chapter_data_list = self._MangaDexEX__chapter_data_list or self._request_cdl(m_data, args)
        for c_data in chapter_data_list:
            num = c_data['chapter']
            c_path = 'Chapter ' + num.zfill(4)
            url_list += self._get_chapter_urls(c_data, c_path)

        return url_list

    def get_gallery_urls(self, url, soup, args):
        if self._is_chapter(url):
            chapter_id = self._get_data_id(url)
            chapter_data = self._chapter_data(chapter_id)
            return self._get_chapter_urls(chapter_data)
        if self._is_manga(url):
            return self._get_manga_urls(url, args)
        raise ExtractorFailed(f"Could not get gallery URLs for {url}")

    def get_tags(self, url, soup, args):
        if self._is_chapter(url):
            chapter_id = self._get_data_id(url)
            c_data = self._chapter_data(chapter_id)
            m_data = self._manga_data(c_data['manga_id'])
        else:
            m_id = self._get_data_id(url)
            m_data = self._manga_data(m_id)
            c_data = None
        tags = {'URL': url}
        tags['Title'] = self._get_title(m_data)
        tags['Languages'] = self._get_langs(url, m_data, c_data, args)
        tags['Artists'] = self._get_artist(m_data)
        tags['Authors'] = self._get_author(m_data)
        tags['Chapters'] = self._get_chapters(url, m_data, c_data)
        tags['Category'] = self._get_categories(m_data)
        tags['Status'] = self._get_status(m_data)
        return tags

    def _get_langs(self, url, m_data, c_data, args):
        if self._is_chapter(url):
            return c_data['lang_name']
        cdl = self._chapter_data_list(m_data, args)
        return cdl[0]['lang_name']

    def _get_chapters(self, url, m_data, c_data):
        if self._is_chapter(url):
            return c_data['chapter'].zfill(4)
        if self._is_manga(url):
            last_chapter = sorted((m_data['chapter'].keys()), key=int)[(-1)]
            end = m_data['chapter'][last_chapter]['chapter'].zfill(4)
            return f"0001-{end}"
        raise ExtractorFailed(f"Could not get chapter data for url: {url}")

    def _get_categories(self, m_data):
        return [self._GENRE_DICT[genre] for genre in m_data['manga']['genres']]

    def _get_status(self, m_data):
        return self._STATUS_DICT[m_data['manga']['status']]
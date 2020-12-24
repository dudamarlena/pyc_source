# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\extractors\mangasushi.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 11763 bytes
"""This module contains the Imgur extractor class"""
import re
from .extractor import Extractor

class MangaSushiEX(Extractor):
    __doc__ = "\n    An extractor for MangaSushi.net\n\n    For any URL, get the base page (../manga/NAME) to retrieve the tag data.\n    For a series URL, search the page to find chapter URLS\n    For a chapter URL, search the page to find 'var chapter_preload_images'\n    to get the image URLs.\n    "

    def __init__(self):
        super().__init__()
        self.name = 'MangaSushi'
        self.url = 'https://www.mangasushi.net'
        self._PAGE_PATTERN = 'https?://(?:www\\.)?mangasushi\\.net.*'
        self._GALLERY_PATTERN = 'https?://(?:www\\.)?mangasushi\\.net/manga/[\\w\\-]*(?:/[\\w\\-]*)*/?'
        self._CHAPTER_PATTERN = 'https?://(?:www\\.)?mangasushi\\.net/manga/[\\w\\-]*/chapter-\\d+(/p/\\d+)?/?'
        self._all_chapters = {}

    def get_tests(self):
        tests = (
         {'url':'https://mangasushi.net/manga/saikyou-no-shuzoku-ga-ningen-datta-ken/chapter-23/', 
          'img_urls':[
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/000.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/001.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/002.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/003.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/004.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/005.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/006.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/007.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/008.jpg',
           'https://mangasushi.net/wp-content/uploads/WP-manga/data/manga_5c704f54cc350/541da92670a9b90135ef3808062ec846/009.jpg'], 
          'size':19, 
          'tags':{'Title':'Saikyou no Shuzoku ga Ningen datta Ken', 
           'URL':'https://mangasushi.net/manga/saikyou-no-shuzoku-ga-ningen-datta-ken/chapter-23/', 
           'Artists':'YANO Mitsuki', 
           'Authors':'KANKITSU Yusura', 
           'Genres':[
            'Action', 'Adult', 'Adventure',
            'Comedy', 'Ecchi', 'Fantasy', 'Harem',
            'Seinen'], 
           'Chapters':'0023', 
           'Languages':'English'}},)
        return tests

    def _is_chapter(self, url):
        """Check if the URL passed is a chapter-type page"""
        return bool(re.match(self._CHAPTER_PATTERN, url))

    def reset(self):
        """Reset the all_chapters variable"""
        self._all_chapters = {}

    def get_size(self, url, soup, args):
        if self._is_chapter(url):
            return self._get_chapter_size(soup)
        return self._get_series_size(soup)

    @staticmethod
    def _get_chapter_size(soup):
        """Return the size of a chapter

        The size is found based on the number of <option> tags within a
        specific <select> tag.
        """
        select_tag = soup.find('select', {'id':'single-pager',  'class':'selectpicker'})
        return sum((1 for option in select_tag.findAll('option')))

    def _get_series_size(self, soup):
        """Return the size of the series

        Finds the size by summing the size of all chapters in the series.
        """
        all_chapters = self._all_chapters or self._get_all_chapters(soup)
        return sum((self._get_chapter_size(soup) for _, soup in all_chapters.values()))

    def _get_all_chapters(self, soup):
        """Return a dictionary of chapter numbers mapped to URL and soup

        Ex. {"0001": ("http://mangasushi.net/manga/series/chapter-1", soup-1)}
        Also sets the attribute '_all_chapters'
        """
        chapter_tags = soup.findAll('li', {'class': 'wp-manga-chapter'})
        for tag in chapter_tags:
            url = tag.a['href']
            chapter = url[(-1)].zfill(4)
            self._all_chapters[chapter] = (url, self._get_soup(url))

        return self._all_chapters

    def get_gallery_urls(self, url, soup, args):
        if self._is_chapter(url):
            return self._get_chapter_urls(soup)
        return self._get_series_urls(soup)

    @staticmethod
    def _get_chapter_urls(soup):
        """Returns the image URLs and filenames for the chapter

        Finds the image URLs from the 'chapter_preload_images' variable
        from the chapter page
        """
        div_tag = soup.find('div', {'class': 'reading-content'})
        js_tag = div_tag.script
        img_vars = re.findall('http[^,]*\\.jpg', js_tag.text)
        img_urls = (url.replace('\\', '') for url in img_vars)
        return [[url.split('/')[(-1)], url] for url in img_urls]

    def _get_series_urls(self, soup):
        """Returns the image URLs and filenames for the series

        Combines the image URLs and filenames from each chapter of the series.
        For each chapter, appends the chapter number as a folder to the
        filename.
        """
        urls = []
        all_chapters = self._all_chapters or self._get_all_chapters(soup)
        for chapter_num, (_, ch_soup) in all_chapters.items():
            chapter_imgs = self._get_chapter_urls(ch_soup)
            for filename, img_url in chapter_imgs:
                filename = f"Chapter {chapter_num}/{filename}"
                urls.append([filename, img_url])

        return urls

    def get_tags(self, url, soup, args):
        """The tags are retrieved from the series page"""
        series_url = '/'.join(url.split('/')[:5])
        series_soup = self._get_soup(series_url)
        tags = {'Title':self._get_title(series_soup), 
         'URL':url, 
         'Languages':'English', 
         'Artists':self._get_artists(series_soup), 
         'Authors':self._get_authors(series_soup), 
         'Genres':self._get_genres(series_soup)}
        if self._is_chapter(url):
            chapter = re.findall('chapter-(\\d+)', url)[0]
            tags['Chapters'] = str(chapter).zfill(4)
        else:
            all_chapters = self._all_chapters or self._get_all_chapters(soup)
            chapter_nums = sorted(all_chapters.keys())
            first, last = chapter_nums[0], chapter_nums[(-1)]
            tags['Chapters'] = f"{first}-{last}"
        return tags

    @staticmethod
    def _get_title(soup):
        return soup.title.string.split('–')[0].strip()

    @staticmethod
    def _parse_tags(soup, div_class):
        """A generic parser for tags, used for getting: artists, authors,
        and genres"""
        div_content = soup.find('div', {'class': div_class})
        tags = div_content.findAll('a')
        return [tag.string for tag in tags]

    @staticmethod
    def _get_artists(soup):
        return MangaSushiEX._parse_tags(soup, 'artist-content')

    @staticmethod
    def _get_authors(soup):
        return MangaSushiEX._parse_tags(soup, 'author-content')

    @staticmethod
    def _get_genres(soup):
        return MangaSushiEX._parse_tags(soup, 'genres-content')
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\extractors\mangahub.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 12383 bytes
"""This module contains the MangaHub extractor class"""
import os, re, ast, json
from .extractor import Extractor

class MangaHubEX(Extractor):
    __doc__ = "\n    An extractor for MangaHub.io\n\n    In MangaHub, series URLs and chapter URLs are supported.\n        + Chapter URLs are for a single chapter of a comic.\n        + Series URLs include all chapters of a comic.\n\n    The image URLs are retrieved by making a POST request to MangaHub's API and\n    parsing the JSON. The request is built from a template and information\n    from the URL.\n\n    Tags come from parsing the comic's series page.\n\n    Getting the chapter URLs and size requires extra requests to the server\n    and thus are cached once retrieved.\n    "

    def __init__(self):
        super().__init__()
        self.name = 'MangaHub'
        self.url = 'https://www.mangahub.io'
        self._PAGE_PATTERN = 'https?://(?:www\\.)?mangahub\\.io.*'
        self._GALLERY_PATTERN = 'https?://(?:www\\.)?mangahub\\.io/chapter/[a-z0-9-]+/?'
        self._SERIES_PATTERN = 'https?://(?:www\\.)?mangahub\\.io/manga/[a-z-]+/?'
        self._IMG_DOMAIN = 'https://cdn.mangahub.io/file/imghub/'
        self._POST_API = 'https://api2.mangahub.io/graphql'
        self._chapter_urls = None
        self._size = None

    def get_tests(self):
        tests = (
         {'url':'https://mangahub.io/manga/madoromi-barmaid', 
          'img_urls':[
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/1.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/2.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/3.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/4.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/5.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/6.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/7.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/8.jpg',
           'https://cdn.mangahub.io/file/imghub/madoromi-barmaid/1/9.jpg'], 
          'size':123, 
          'series':True, 
          'tags':{'Title':'Madoromi Barmaid', 
           'Category':[
            'Comedy', 'Seinen', 'Slice of Life'], 
           'Authors':'HAYAKAWA Pao', 
           'Artists':'HAYAKAWA Pao'}},
         {'url':'https://mangahub.io/chapter/very-pure/chapter-154/', 
          'img_urls':[
           'https://cdn.mangahub.io/file/imghub/very-pure/154/1.jpg',
           'https://cdn.mangahub.io/file/imghub/very-pure/154/2.jpg',
           'https://cdn.mangahub.io/file/imghub/very-pure/154/3.jpg',
           'https://cdn.mangahub.io/file/imghub/very-pure/154/4.jpg',
           'https://cdn.mangahub.io/file/imghub/very-pure/154/5.jpg',
           'https://cdn.mangahub.io/file/imghub/very-pure/154/6.jpg',
           'https://cdn.mangahub.io/file/imghub/very-pure/154/7.jpg',
           'https://cdn.mangahub.io/file/imghub/very-pure/154/8.jpg'], 
          'size':8, 
          'tags':{'Title':'Very Pure', 
           'Category':[
            'Comedy', 'Ecchi', 'Harem',
            'Romance', 'School Life'], 
           'Authors':'You Lu Wen Hua', 
           'Artists':'You Lu Wen Hua'}})
        return tests

    def is_gallery(self, url):
        return self._is_chapter(url) or self._is_series(url)

    def _is_chapter(self, url):
        return re.match(self._GALLERY_PATTERN, url)

    def _is_series(self, url):
        return re.match(self._SERIES_PATTERN, url)

    def reset(self):
        self._chapter_urls = None
        self._size = None

    @staticmethod
    def _get_title(soup):
        """Get title of manga from main page"""
        rough = soup.title.string.split(' ')[1:-4]
        return ' '.join(rough)

    @staticmethod
    def _get_categories(soup):
        category_tags = soup.find_all('a', {'class': 'label genre-label'})
        return [item.string for item in category_tags]

    @staticmethod
    def _get_status(soup):
        return soup.find('span', {'class': '_3SlhO'}, string='Status').next_sibling.string

    @staticmethod
    def _get_artists(soup):
        return soup.find('span', {'class': '_3SlhO'}, string='Artist').next_sibling.string

    @staticmethod
    def _get_authors(soup):
        return soup.find('span', {'class': '_3SlhO'}, string='Author').next_sibling.string

    def _get_chapter_urls(self, soup):
        """Returns URLs for each chapter of a series

        The URLs are also saved in an attribute for quick retrieval later.
        """
        if self._chapter_urls is None:
            latest_tag = soup.find('span', {'class': '_3SlhO'}, string='Latest').next_sibling
            latest_url = latest_tag.a.get('href')
            latest_num = latest_url.split('-')[(-1)]
            base_url = '-'.join(latest_url.split('-')[:-1])
            self._chapter_urls = (f"{base_url}-{num}" for num in range(1, int(latest_num) + 1))
        return self._chapter_urls

    @staticmethod
    def _gallery_slug(gallery_url):
        """Return the gallery's slug and number for POST requests"""
        if gallery_url[(-1)] == '/':
            gallery_url = gallery_url[:-1]
        series = gallery_url.split('/')[(-2)]
        id_ = re.search('[0-9]+/?$', gallery_url)
        return (series, id_.group(0))

    def _get_chapters(self, url, soup):
        """Return a string to summarize chapters scraped from URL"""
        if self._is_series(url):
            tag = soup.find('span', {'class': '_3SlhO'}, string='Latest').next_sibling
            number = tag.a.get('href').split('-')[(-1)]
            return f"0001-{number.zfill(4)}"
        number = url.split('-')[(-1)]
        return number.zfill(4)

    def _pages_dict(self, url):
        """Return a dictionary of pages for a chapter URL

        Data specific to the chapter is retrieved and used for a POST operation
        to the site's API. The JSON response is then parsed and returned.

        Returns a dict mapping image # to image URL
        """
        slug, number = self._gallery_slug(url)
        query = f'{{chapter(x:m01,slug:"{slug}",number:{number}){{pages}}}}'
        data = {'query': query}
        response = self._session.post((self._POST_API), data=data)
        json_data = json.loads(response.content.decode('utf-8'))
        literal_dict = json_data['data']['chapter']['pages']
        return ast.literal_eval(literal_dict)

    def get_size(self, url, soup, args):
        """Get total # of images in the gallery to download

        The size is also saved in an attribute for quick retrieval later.
        """
        if self._size is None:
            if self._is_series(url):
                chapter_urls = self._get_chapter_urls(soup)
                self._size = self._series_size(chapter_urls)
            else:
                self._size = self._chapter_size(url)
        return self._size

    def _series_size(self, chapter_urls):
        """Get total # of images in the series (the sum of all chapters)"""
        return sum((self._chapter_size(chapter) for chapter in chapter_urls))

    def _chapter_size(self, url):
        """Get total # of images of a chapter"""
        pages_dict = self._pages_dict(url)
        size_str = list(pages_dict.keys())[(-1)]
        return int(size_str)

    def get_gallery_urls(self, url, soup, args):
        """Return all image paths and image URLs"""
        if self._is_series(url):
            return self._get_series_images(soup)
        return self._get_chapter_images(url, soup)

    def _get_series_images(self, soup):
        """Return all images and image URLs for a series URL

        Combines the URLs for all chapters in the series.
        """
        series_urls = []
        chapter_urls = self._get_chapter_urls(soup)
        for chapter in chapter_urls:
            chapter_num = chapter.split('-')[(-1)]
            ch_path = 'Chapter ' + chapter_num.zfill(4)
            series_urls += self._get_chapter_images(chapter, soup, ch_path=ch_path)

        return series_urls

    def _get_chapter_images(self, url, soup, ch_path=None):
        """Return all images and image URLs for a chapter URL"""
        url_list = []
        size = self.get_size(url, soup, None)
        size_len = len(str(size))
        pages_dict = self._pages_dict(url)
        for img_num, sub_url in pages_dict.items():
            img_ext = sub_url.split('.')[(-1)]
            img_name = f"{img_num.zfill(size_len)}.{img_ext}"
            filename = img_name if ch_path is None else os.path.join(ch_path, img_name)
            img_url = f"{self._IMG_DOMAIN}{sub_url}"
            url_list.append([filename, img_url])

        return url_list

    def _main_soup(self, url):
        """Returns the soup of the manga series page"""
        if url[(-1)] == '/':
            url = url[:-1]
        sub_url, _ = os.path.split(url)
        main_url = re.sub('chapter', 'manga', sub_url)
        return self._get_soup(main_url)

    def get_tags(self, url, soup, args):
        """Returns a dictionary of data regarding the series

        A majority of the series data is taken from the series page.
        Thus if a chapter URL is given, the series page needs to be scraped
        too (the 'main_soup').
        """
        main_soup = soup if self._is_series(url) else self._main_soup(url)
        tags = {'Languages':'English', 
         'URL':url}
        tags['Title'] = self._get_title(main_soup)
        tags['Category'] = self._get_categories(main_soup)
        tags['Status'] = self._get_status(main_soup)
        tags['Artists'] = self._get_artists(main_soup)
        tags['Authors'] = self._get_authors(main_soup)
        tags['Chapters'] = self._get_chapters(url, soup)
        return tags
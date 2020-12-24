# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\extractors\nhentai.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 10105 bytes
"""This module contains the NHentai extractor class"""
import os, re
from komidl.exceptions import ExtractorFailed
from .extractor import Extractor

class NHentaiEX(Extractor):
    __doc__ = '\n    An extractor for NHentai.net\n    '

    def __init__(self):
        super().__init__()
        self.name = 'NHentai'
        self.url = 'https://www.nhentai.net'
        self._PAGE_PATTERN = 'https?://(?:t\\.)?(?:www\\.)?nhentai\\.net.*'
        self._GALLERY_PATTERN = 'https?://(?:www\\.)?nhentai\\.net/g/[0-9]+/?'
        self._IMG_DOMAIN = 'https://i.nhentai.net/galleries/'

    def get_tests(self):
        tests = (
         {'url':'https://nhentai.net/g/252295/', 
          'img_urls':[
           'https://i.nhentai.net/galleries/1311486/1.jpg',
           'https://i.nhentai.net/galleries/1311486/2.jpg',
           'https://i.nhentai.net/galleries/1311486/3.jpg',
           'https://i.nhentai.net/galleries/1311486/4.jpg',
           'https://i.nhentai.net/galleries/1311486/5.jpg',
           'https://i.nhentai.net/galleries/1311486/6.jpg',
           'https://i.nhentai.net/galleries/1311486/7.jpg',
           'https://i.nhentai.net/galleries/1311486/8.jpg',
           'https://i.nhentai.net/galleries/1311486/9.jpg'], 
          'size':22, 
          'tags':{'Title':'Ning Hai Nee-chan no Migawari Nikki', 
           'URL':'https://nhentai.net/g/252295/', 
           'Parodies':'Azur Lane', 
           'Characters':[
            'Teitoku', 'Ning Hai'], 
           'Tags':[
            'Blowjob', 'Paizuri', 'Swimsuit',
            'Bikini', 'Lingerie', 'Blackmail'], 
           'Artists':'Chiune', 
           'Groups':'Chiukorone', 
           'Languages':'English', 
           'Categories':'Doujinshi'}},
         {'url':'https://nhentai.net/g/278089/', 
          'img_urls':[
           'https://i.nhentai.net/galleries/1445283/1.jpg',
           'https://i.nhentai.net/galleries/1445283/2.jpg',
           'https://i.nhentai.net/galleries/1445283/3.jpg',
           'https://i.nhentai.net/galleries/1445283/4.jpg',
           'https://i.nhentai.net/galleries/1445283/5.jpg',
           'https://i.nhentai.net/galleries/1445283/6.jpg',
           'https://i.nhentai.net/galleries/1445283/7.jpg',
           'https://i.nhentai.net/galleries/1445283/8.jpg',
           'https://i.nhentai.net/galleries/1445283/9.jpg'], 
          'size':17, 
          'tags':{'Title':'Kissin Cuzins', 
           'URL':'https://nhentai.net/g/278089/', 
           'Parodies':'Sword Art Online', 
           'Characters':[
            'Kazuto Kirigaya', 'Suguha Kirigaya'], 
           'Artists':'Kawase Seiki', 
           'Languages':'English', 
           'Categories':'Doujinshi', 
           'Groups':'Primal Gym', 
           'Tags':[
            'Big Breasts', 'Sole Female', 'Sole Male',
            'Incest', 'Paizuri', 'X-Ray', 'Impregnation',
            'Sleeping']}})
        return tests

    @staticmethod
    def _get_title(soup):
        """Return the title of the gallery

        Title taken from the <h1> tag and may require adjustments.
        """
        raw_title = soup.find('h1').string
        square_br = re.sub('\\[[^\\]]*\\]', '', raw_title)
        round_br = re.sub('\\([^\\)]*\\)', '', square_br)
        curly_br = re.sub('\\{[^\\}]*\\}', '', round_br)
        bar_strip = re.sub('\\|.*', '', curly_br)
        title = bar_strip.strip()
        return title

    @staticmethod
    def _get_gallery_id(soup):
        """Return ID of the gallery

        Used to build gallery URLs (ID appended to IMG_DOMAIN)
        """
        url = soup.find(property='og:image')['content']
        return url.split('/')[4]

    @staticmethod
    def _get_img_type(soup):
        """Return the file format for the images"""
        url = soup.find(property='og:image')['content']
        return url.split('.')[(-1)]

    def get_size(self, url, soup, args):
        """Return total # of images in gallery"""
        tags = soup.time.parent.previous_siblings
        for tag in tags:
            if self._is_size_str(tag.string):
                return int(tag.string.split(' ')[0])

        raise ExtractorFailed(f"Could not find size for URL: {url}")

    def get_gallery_urls(self, url, soup, args):
        url_list = []
        size = self.get_size(url, soup, args)
        size_len = len(str(abs(size)))
        id_ = self._get_gallery_id(soup)
        img_type = self._get_img_type(soup)
        for img_num in range(1, size + 1):
            img_url = self._build_img_url(id_, img_num, img_type)
            basename = str(img_num).zfill(size_len)
            filename = f"{basename}.{img_type}"
            url_list.append([filename, img_url])

        return url_list

    def get_tags(self, url, soup, args):
        soup_tags = {'Title':self._get_title(soup), 
         'URL':url}
        tags = soup.find('section', {'id': 'tags'})
        tag_divs = tags.find_all('div')
        for div in tag_divs:
            tag_name = re.sub('\\s+', '', div.contents[0])[:-1]
            tag_content = re.sub('^\\s+', '', div.get_text().split(':')[1])
            content_elements = div.span.find_all('a')
            tag_content = [element.contents[0] for element in content_elements]
            if tag_content:
                clean_tags = self._clean_tags(tag_name, tag_content)
                soup_tags[tag_name] = clean_tags

        return soup_tags

    def _build_img_url(self, id_, img_num, img_type):
        """Construct the URL of an image"""
        return f"{self._IMG_DOMAIN}{id_}/{img_num}.{img_type}"

    @staticmethod
    def _is_size_str(string):
        """Determine if the string in the HTML tag contains the gallery size"""
        return re.match('^[0-9]+ pages$', string)

    @staticmethod
    def _clean_tags(key, contents):
        """Formats the list of contents for usage as values to a key

        Split by a ' (123,123)' format and capitalize all words.
        Also removes any unnecessary values or keys.
        """
        tag_list = [content.strip().title() for content in contents]
        if key == 'Languages':
            if 'Translated' in tag_list:
                tag_list.remove('Translated')
            if 'Rewrite' in tag_list:
                tag_list.remove('Rewrite')
        return tag_list
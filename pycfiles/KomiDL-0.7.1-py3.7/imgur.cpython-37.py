# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\komidl\extractors\imgur.py
# Compiled at: 2019-10-12 01:12:13
# Size of source mod 2**32: 5787 bytes
"""This module contains the Imgur extractor class"""
from .extractor import Extractor

class ImgurEX(Extractor):
    __doc__ = "\n    An extractor for Imgur.com\n\n    When downloading galleries, Imgur supports various img/file formats.\n    For a file '<ID>.gifv', '<ID>.jpg' also exists as a preview screenshot.\n    Thus, it is unreliable to set all URLs as '.jpg' and rely on receiving an\n    HTTP 404 error and letting Scraper's _retry_download_image() get the actual\n    file. The workaround used is to use '<ID>.gifv' to request the HTML page\n    for the image, and extract the true URL from there. The drawback is that\n    the number of requests made for an album is doubled.\n\n    Tags are non-existant for Imgur so the assumption is that the language is\n    English.\n    "

    def __init__(self):
        super().__init__()
        self.name = 'Imgur'
        self.url = 'https://www.imgur.com'
        self._PAGE_PATTERN = 'https?://(?:www\\.)?imgur\\.com.*'
        self._GALLERY_PATTERN = 'https?://(?:www\\.)?imgur\\.com/(?:a|gallery)/\\w{5,7}/?'
        self._IMG_DOMAIN = 'https://i.imgur.com/'

    def get_tests(self):
        tests = (
         {'url':'https://imgur.com/a/ZbNwy', 
          'img_urls':[
           'https://i.imgur.com/OtQ8qWE.png',
           'https://i.imgur.com/HQx4kIf.png',
           'https://i.imgur.com/HVjsGfg.png',
           'https://i.imgur.com/RSH9anK.jpg'], 
          'size':20, 
          'tags':{'Title':'My Pixel art wallpapers', 
           'URL':'https://imgur.com/a/ZbNwy', 
           'Languages':'English'}},
         {'url':'https://imgur.com/a/TnUGfAs', 
          'img_urls':[
           'https://i.imgur.com/biEef76.jpg',
           'https://i.imgur.com/MXY2976.jpg'], 
          'size':2, 
          'tags':{'Title':'Imgur-TnUGfAs', 
           'URL':'https://imgur.com/a/TnUGfAs', 
           'Languages':'English'}})
        return tests

    @staticmethod
    def _get_title(url, soup):
        raw_title = soup.title.string.strip()
        title = '-'.join(raw_title.split('-')[:-1]).strip()
        if not (title == 'Imgur: The magic of the Internet' or title):
            album_id = url.split('/')[(-1)] if url[(-1)] != '/' else url.split('/')[(-2)]
            title = f"Imgur-{album_id}"
        return title

    def get_size(self, url, soup, args):
        image_tags = soup.findAll('div', {'class': 'post-image-container'})
        return len(image_tags)

    def _image_url(self, img_tag):
        """For an image tag, return the image's true URL with extension

        Using '.gifv', we can obtain an HTML page that hosts the
        image/video. Videos use the <source> tag and images use the
        <img> tag. Note that there will always be at least one <img> tag
        due to the favicon.
        """
        img_id = img_tag.get('id')
        site_url = f"{self._IMG_DOMAIN}{img_id}.gifv"
        image_soup = self._get_soup(site_url)
        img_url = image_soup.find('img')['src']
        video_tag = image_soup.find('source')
        if video_tag:
            img_url = video_tag['src']
        return f"https:{img_url}"

    def get_gallery_urls(self, url, soup, args):
        url_list = []
        size = self.get_size(url, soup, args)
        size_len = len(str(size))
        img_tags = soup.findAll('div', {'class': 'post-image-container'})
        img_urls = (self._image_url(tag) for tag in img_tags)
        for img_num, img_url in enumerate(img_urls):
            base_name = str(img_num).zfill(size_len)
            extension = img_url.split('.')[(-1)]
            filename = f"{base_name}.{extension}"
            url_list.append([filename, img_url])

        return url_list

    def get_tags(self, url, soup, args):
        soup_tags = {'Title':self._get_title(url, soup), 
         'Languages':'English', 
         'URL':url}
        return soup_tags
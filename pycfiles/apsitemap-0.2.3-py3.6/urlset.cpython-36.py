# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\apsitemap\urlset.py
# Compiled at: 2017-10-12 21:51:46
# Size of source mod 2**32: 4569 bytes
from xml.dom.minidom import Document
from urllib import parse
import os
from .utility import standardize_url, sitemap_log

class UrlSet(object):
    __doc__ = 'A set of urls.\n\n    the container of urls that have the same domain.\n\n    Attribute:\n        entry: the entry of website.\n    '

    def __init__(self, entry: str, scheme='http://', changefreq=None, lastmod=None):
        self._UrlSet__entry = standardize_url(entry)
        entry_parse = parse.urlparse(self._UrlSet__entry)
        self._UrlSet__netloc = entry_parse.netloc
        self._UrlSet__scheme = entry_parse.scheme if entry_parse.scheme != '' else scheme
        self._UrlSet__urls = []
        self._UrlSet__changefreq = changefreq
        self._UrlSet__lastmod = lastmod
        sitemap_log.debug('Initialize urls container...')

    def can_have(self, url: str) -> bool:
        """can url join the set?"""
        return parse.urlparse(standardize_url(url)).netloc == self._UrlSet__netloc

    def add(self, urls: list):
        urls = self.fix_urls(urls)
        for url in urls:
            if url not in self._UrlSet__urls:
                self._UrlSet__urls.append(url)

        self._UrlSet__urls.sort()

    def fix_urls(self, urls: list) -> list:
        results = []
        for url in urls:
            if isinstance(url, str):
                if url.startswith('/'):
                    results.append('{}://{}{}'.format(self._UrlSet__scheme, self._UrlSet__netloc, url))
                else:
                    if url.startswith('https://') or url.startswith('http://'):
                        if self.can_have(url):
                            results.append(url)
                    elif not url.startswith('#'):
                        if not url.startswith('javascript'):
                            results.append(standardize_url(url))

        return list(map(lambda url_: parse.urldefrag(parse.unquote(url_)).url, results))

    def save_xml(self, file='sitemap.xml'):
        doc = Document()
        urlset = doc.createElement('urlset')
        urlset.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.setAttribute('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
        for url_item in self:
            url = doc.createElement('url')
            urlset.appendChild(url)
            loc = doc.createElement('loc')
            loc_text = doc.createTextNode(url_item)
            loc.appendChild(loc_text)
            url.appendChild(loc)
            if bool(self._UrlSet__changefreq):
                changefreq = doc.createElement('changefreq')
                changefreq_text = doc.createTextNode(self._UrlSet__changefreq)
                changefreq.appendChild(changefreq_text)
                url.appendChild(changefreq)
            if bool(self._UrlSet__lastmod):
                lastmod = doc.createElement('lastmod')
                lastmod_text = doc.createTextNode(self._UrlSet__lastmod)
                lastmod.appendChild(lastmod_text)
                url.appendChild(lastmod)

        doc.appendChild(urlset)
        with open(file, 'w', encoding='utf-8') as (f):
            f.write(doc.toprettyxml())
        sitemap_log.info('Urlset was saved as xml file, %s', file)

    def save_txt(self, file='sitemap.txt'):
        with open(file, 'w', encoding='utf-8') as (f):
            f.write(os.linesep.join([url for url in self._UrlSet__urls]))
        sitemap_log.info('Urlset was saved as txt file, %s', file)

    def __contains__(self, url: str):
        return url in self._UrlSet__urls

    def __iter__(self):
        yield from self._UrlSet__urls
        if False:
            yield None

    def __getitem__(self, index):
        return self._UrlSet__urls[index]

    def __len__(self):
        return len(self._UrlSet__urls)


if __name__ == '__main__':
    url_lists = ['http://www.qiama.com:8888/article/index.html?page=2#html',
     'http://www.qiama.com:8888/article/index.html?page=2#perfect',
     'http://www.qiama.com:8888/article/index.html?page=3#perfect',
     'http://www.qiama.com:8888/你说呢',
     '/pages/2',
     '#main',
     'javascript',
     'http://baidu.com/article/我说我不知道']
    urlset = UrlSet(entry='www.qiama.com:8888')
    urlset.add(url_lists)
    urlset.save_xml()
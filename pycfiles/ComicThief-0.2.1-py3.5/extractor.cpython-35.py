# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComicThief/extractor.py
# Compiled at: 2017-02-06 14:07:46
# Size of source mod 2**32: 651 bytes
from lxml import html
from .config import WithConfig

class Extractor(WithConfig):

    def extract_comic_links(self, page, service='default'):
        tree = html.fromstring(page.content)
        return tree.xpath(self.config['COMICS_LIST_XPATH'].get(service))

    def extract_issues_list(self, page, service='default'):
        tree = html.fromstring(page.content)
        return tree.xpath(self.config['COMICS_SUBPAGE_XPATH'].get(service))

    def extract_images_list(self, page, service='default'):
        tree = html.fromstring(page.content)
        return tree.xpath(self.config['COMICS_IMAGES_XPATH'].get(service))
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bulrush/image_extractor.py
# Compiled at: 2019-06-14 12:05:42
# Size of source mod 2**32: 702 bytes
from html.parser import HTMLParser

class ImageExtractor(HTMLParser):
    """ImageExtractor"""

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self._extract_source_attr(attrs)

    def _extract_source_attr(self, attrs):
        self.images.append(next((val for attr, val in attrs if attr == 'src')))


def extract_images(article_content):
    """Extract the sources of all images in the article."""
    extractor = ImageExtractor()
    extractor.feed(article_content)
    return extractor.images
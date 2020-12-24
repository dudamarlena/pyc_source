# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/models/index.py
# Compiled at: 2019-09-10 15:18:29
from pip._vendor.six.moves.urllib import parse as urllib_parse

class Index(object):

    def __init__(self, url):
        self.url = url
        self.netloc = urllib_parse.urlsplit(url).netloc
        self.simple_url = self.url_to_path('simple')
        self.pypi_url = self.url_to_path('pypi')

    def url_to_path(self, path):
        return urllib_parse.urljoin(self.url, path)


PyPI = Index('https://pypi.org/')
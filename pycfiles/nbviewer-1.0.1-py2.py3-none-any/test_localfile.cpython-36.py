# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/local/tests/test_localfile.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 1720 bytes
import requests, sys
from nbviewer.utils import url_path_join
from ....tests.base import NBViewerTestCase, FormatHTMLMixin

class LocalFileDefaultTestCase(NBViewerTestCase):

    @classmethod
    def get_server_args(cls):
        return [
         '--localfiles=.']

    def test_url(self):
        url = self.url('localfile/nbviewer/tests/notebook.ipynb')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)


class FormatHTMLLocalFileDefaultTestCase(LocalFileDefaultTestCase, FormatHTMLMixin):
    pass


class LocalFileRelativePathTestCase(NBViewerTestCase):

    @classmethod
    def get_server_args(cls):
        return [
         '--localfiles=nbviewer']

    def test_url(self):
        url = self.url('localfile/tests/notebook.ipynb')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)

    def test_404(self):
        url = self.url('localfile/doesntexist')
        r = requests.get(url)
        self.assertEqual(r.status_code, 404)


class FormatHTMLLocalFileRelativePathTestCase(LocalFileRelativePathTestCase, FormatHTMLMixin):
    pass
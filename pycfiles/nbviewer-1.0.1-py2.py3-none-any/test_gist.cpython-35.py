# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/gist/tests/test_gist.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 2189 bytes
import requests
from ....tests.base import NBViewerTestCase, FormatHTMLMixin

class GistTestCase(NBViewerTestCase):

    def test_gist(self):
        url = self.url('2352771')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)

    def test_gist_not_nb(self):
        url = self.url('6689377')
        r = requests.get(url)
        self.assertEqual(r.status_code, 400)

    def test_gist_no_such_file(self):
        url = self.url('6689377/no/file.ipynb')
        r = requests.get(url)
        self.assertEqual(r.status_code, 404)

    def test_gist_list(self):
        url = self.url('7518294')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('<th>Name</th>', html)

    def test_multifile_gist(self):
        url = self.url('7518294', 'Untitled0.ipynb')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('Download Notebook', html)

    def test_anonymous_gist(self):
        url = self.url('gist/4465051')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('Download Notebook', html)

    def test_gist_unicode(self):
        url = self.url('gist/amueller/3974344')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('<th>Name</th>', html)

    def test_gist_unicode_content(self):
        url = self.url('gist/ocefpaf/cf023a8db7097bd9fe92')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertNotIn('param&#195;&#169;trica', html)
        self.assertIn('param&#233;trica', html)


class FormatHTMLGistTestCase(GistTestCase, FormatHTMLMixin):
    pass
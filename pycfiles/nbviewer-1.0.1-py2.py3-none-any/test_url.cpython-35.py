# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/url/tests/test_url.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 754 bytes
import requests
from ....tests.base import NBViewerTestCase, FormatHTMLMixin

class URLTestCase(NBViewerTestCase):

    def test_url(self):
        url = self.url('url/jdj.mit.edu/~stevenj/IJulia Preview.ipynb')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIn('Download Notebook', r.text)


class FormatHTMLURLTestCase(URLTestCase, FormatHTMLMixin):
    pass
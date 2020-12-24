# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/url/tests/test_content.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 453 bytes
from ....tests.async_base import AsyncNbviewerTestCase

class ForceUTF8TestCase(AsyncNbviewerTestCase):

    def test_utf8(self):
        """ #507, bitbucket returns no content headers, but _is_ serving utf-8
        """
        response = self.fetch('/urls/bitbucket.org/sandiego206/asdasd/raw/master/Untitled.ipynb')
        self.assertEqual(response.code, 200)
        self.assertIn('ñ', response.body)
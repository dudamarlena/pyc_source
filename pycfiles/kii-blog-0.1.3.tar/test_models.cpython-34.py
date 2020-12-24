# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/tests/test_models.py
# Compiled at: 2014-12-16 08:44:42
# Size of source mod 2**32: 321 bytes
from kii.stream.tests import base
from .. import models
from django import db

class BlogModelTestCase(base.StreamTestCase):

    def test_slug_is_set_from_title(self):
        m = models.BlogEntry(root=self.streams[0], title='First blog entry')
        m.save()
        self.assertEqual(m.slug, 'first-blog-entry')
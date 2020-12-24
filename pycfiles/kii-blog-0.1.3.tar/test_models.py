# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii-blog/kii_blog/tests/test_models.py
# Compiled at: 2014-11-24 05:36:44
from kii.stream.tests import base
from .. import models
from django import db

class BlogModelTestCase(base.StreamTestCase):

    def test_slug_is_set_from_title(self):
        m = self.G(models.BlogEntry, title='First blog entry')
        self.assertEqual(m.slug, 'first-blog-entry')
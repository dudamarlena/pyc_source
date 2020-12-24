# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/tests/models/test_category.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 470 bytes
from survey.models.category import Category
from survey.tests import BaseTest

class TestCategory(BaseTest):

    def test_unicode(self):
        """ Unicode is not None and do not raise error. """
        cat = Category.objects.all()[0]
        self.assertIsNotNone(cat)

    def test_slugify(self):
        """ Slugify is not None and do not raise error. """
        cat = Category.objects.all()[0]
        self.assertIsNotNone(cat.slugify())
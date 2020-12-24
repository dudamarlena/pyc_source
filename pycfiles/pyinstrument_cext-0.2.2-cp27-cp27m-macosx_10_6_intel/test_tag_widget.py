# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyinstruments\curvestore\test_tag_widget.py
# Compiled at: 2013-11-18 07:55:23
from django.test import TestCase
from pyinstruments.curvestore.models import Tag, top_level_tag

class TestTagModel(TestCase):

    def test_top_level_tag(self):
        """
        
        """
        self.tag = Tag(name='tag1')
        self.tag.save()
        self.tag2 = Tag(name='tag2')
        self.tag2.save()
        self.assertTrue(top_level_tag()[1].name == 'tag2')
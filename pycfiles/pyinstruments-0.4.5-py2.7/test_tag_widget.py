# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
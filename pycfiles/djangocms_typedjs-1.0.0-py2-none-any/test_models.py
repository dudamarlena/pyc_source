# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/life-website-env/life-website/website/djangocms_typedjs/tests/test_models.py
# Compiled at: 2016-07-18 07:33:35
from __future__ import unicode_literals
from django.core.files import File
from cms.test_utils.testcases import CMSTestCase
from ..models import TypedJS

class TypedJSTest(CMSTestCase):

    def test_creating_new_slider(self):
        t = TypedJS.objects.create(name=b'test')
        all_typedjs = TypedJS.objects.all()
        self.assertEqual(all_typedjs.count(), 1)
        self.assertEqual(all_typedjs[0], t)
        self.assertEqual(t.__str__(), t.name)
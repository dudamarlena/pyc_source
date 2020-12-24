# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/test_utils.py
# Compiled at: 2017-05-03 05:57:29
from django.template.defaultfilters import slugify
from django.test import TestCase
from jmbo.models import ModelBase

class UtilsTestCase(TestCase):
    fixtures = [
     'sites.json']

    def test_generate_slug(self):
        obj = ModelBase(title='utils test case title')
        obj.save()
        self.failIf(obj.slug == '')
        obj = ModelBase(title='utils test case title 1')
        obj.save()
        self.failUnless(obj.slug == slugify(obj.title))
        obj = ModelBase(title='utils test case title 1')
        obj.save()
        obj.title = 'updated title'
        obj.save()
        self.failIf(obj.slug == slugify(obj.title))
        orig_slug = obj.slug
        obj.save()
        self.failUnless(obj.slug == orig_slug)
        obj = ModelBase.objects.get(id=obj.id)
        self.failIf(obj.slug == '')
        obj = ModelBase()
        obj.save()
        obj = ModelBase()
        obj.save()
        obj = ModelBase()
        obj.save()
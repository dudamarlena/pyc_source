# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/test_template_tags.py
# Compiled at: 2017-05-03 05:57:29
from django import template
from django.contrib.sites.models import Site
from django.test import TestCase
from jmbo.models import ModelBase, Relation

class TemplateTagsTestCase(TestCase):
    fixtures = [
     'sites.json']

    def test_get_related_list(self):
        obj1 = ModelBase.objects.create(title='obj1')
        obj1.sites = Site.objects.all()
        obj1.publish()
        obj2 = ModelBase.objects.create(title='obj2')
        obj2.sites = Site.objects.all()
        obj2.publish()
        obj3 = ModelBase.objects.create(title='obj3')
        Relation.objects.create(source=obj1, target=obj2, name='obj-objs')
        Relation.objects.create(source=obj1, target=obj3, name='obj-objs')
        self.context = template.Context({'object': obj1})
        t = template.Template('{% load jmbo_template_tags %}        {% get_related_items "obj-objs" for object as "related_items" %}\n        {% for obj in related_items %}{{ obj.title }}{% endfor %}')
        result = t.render(self.context)
        self.failUnless('obj2' in result)
        self.failIf('obj3' in result)
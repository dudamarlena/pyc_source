# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/tests/test_layers.py
# Compiled at: 2017-04-24 04:30:52
# Size of source mod 2**32: 2288 bytes
from django import template
from django.test import TestCase
from django.test.client import RequestFactory
from mote import models
from mote.utils import get_object_by_dotted_name

class LayersTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(LayersTestCase, cls).setUpTestData()
        cls.factory = RequestFactory()

    def test_render_button(self):
        """We override button element and data"""
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myprojectchild.website.atoms.button" %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, 'Button child')

    def test_render_anchor(self):
        """We override anchor element but not data"""
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myprojectchild.website.atoms.anchor" %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, 'Anchor child')

    def test_render_panel(self):
        """We inherit panel fully"""
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myprojectchild.website.atoms.panel" %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, 'Panel')

    def test_metadata_button(self):
        """We override button element and data"""
        obj = get_object_by_dotted_name('myprojectchild.website.atoms.button')
        self.assertEqual(obj.metadata['title'], 'MyProjectChild Button')

    def test_metadata_anchor(self):
        """We override anchor element but not data"""
        obj = get_object_by_dotted_name('myprojectchild.website.atoms.anchor')
        self.assertEqual(obj.metadata['title'], 'Anchor')

    def test_metadata_panel(self):
        """We inherit panel fully"""
        obj = get_object_by_dotted_name('myprojectchild.website.atoms.panel')
        self.assertEqual(obj.metadata['title'], 'Panel')
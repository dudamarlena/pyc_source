# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/tests/test_tags.py
# Compiled at: 2017-04-24 04:30:52
from django import template
from django.test import TestCase
from django.test.client import RequestFactory
from mote import models
from mote.utils import get_object_by_dotted_name

class TagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TagsTestCase, cls).setUpTestData()
        cls.factory = RequestFactory()

    def test_render_element_by_identifier(self):
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myproject.website.atoms.button" %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Lorem ipsum</i>\n            </button>')

    def test_render_element_by_self(self):
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "self.website.atoms.button" %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Lorem ipsum</i>\n            </button>')

    def test_render_element_with_kwargs_variable(self):
        request = self.factory.get('/')
        button = {'Italic': {'text': 'Foo'}}
        t = template.Template('{% load mote_tags %}\n            {% render_element "myproject.website.atoms.button" data=button %}')
        result = t.render(template.Context({'request': request, 
           'button': button}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Foo</i>\n            </button>')

    def test_render_element_with_kwargs_dict(self):
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myproject.website.atoms.button" data=\'{"Italic": {"text": "Foo"}}\' %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Foo</i>\n            </button>')

    def test_render_element_with_kwargs_variables(self):
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myproject.website.atoms.button" data=\'{"Italic": {"text": "{{ foo }}"}}\' number=number %}')
        result = t.render(template.Context({'request': request, 
           'foo': 'Foo', 
           'number': 1}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Foo</i>\n            </button>')

    def test_render_other_element(self):
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myproject.website.atoms.button" %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Lorem ipsum</i>\n            </button>')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myproject.website.atoms.button" data=\'{"OtherElement": {"element": "myproject.website.atoms.panel"}}\' %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Lorem ipsum</i>\n            </button>\n            Panel')
        t = template.Template('{% load mote_tags %}\n            {% render_element "myproject.website.atoms.button" data=\'{"OtherElement": {"element": "{{ element.pattern.panel.dotted_name }}" }}\' %}')
        result = t.render(template.Context({'request': request}))
        self.assertHTMLEqual(result, '<button class="Button Button--solid Button--yellowButtercup">\n            <i>Lorem ipsum</i>\n            </button>\n            Panel')

    def test_get_element_data(self):
        request = self.factory.get('/')
        t = template.Template('{% load mote_tags %}\n            {% get_element_data "tests/fleet.xml" as fleet %}\n            <fleet>\n            {% for car in fleet.cars %}\n                <car>\n                    <brand>{{ car.brand }}</brand>\n                    <model>{{ car.model }}</model>\n                </car>\n            {% endfor %}\n            <value>{{ fleet.value }}</value>\n            </fleet>')
        result = t.render(template.Context({'request': request, 
           'cars': [{'brand': 'Opel', 'model': 'Astra'}, {'brand': 'Ford', 'model': 'Ikon'}]}))
        expected = '<fleet>\n            <car>\n                <brand>Opel</brand>\n                <model>Astra</model>\n            </car>\n            <car>\n                <brand>Ford</brand>\n                <model>Ikon</model>\n            </car>\n            <value>100</value>\n        </fleet>'
        self.assertHTMLEqual(result, expected)
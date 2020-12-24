# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/tests/test_templatetags.py
# Compiled at: 2017-10-20 11:35:08
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from composer.models import Slot, Row, Column, Tile
from composer.tests.models import DummyModel1, DummyModel2
HOME_REGEX = '^' + reverse('home') + '$'

class TemplateTagsATestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsATestCase, cls).setUpTestData()
        cls.slot = Slot.objects.create(slot_name='content', url=HOME_REGEX)
        cls.slot.sites = Site.objects.all()
        cls.slot.save()

    def test_default_slot(self):
        response = self.client.get(reverse('home'))
        self.assertHTMLEqual('\n        <div id="header">\n            Header slot\n        </div>\n        <div id="content">\n            This is the default content\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>', response.content)


class TemplateTagsBTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsBTestCase, cls).setUpTestData()
        cls.dm_one = DummyModel1.objects.create(title='One')
        cls.slot = Slot.objects.create(slot_name='content', url=HOME_REGEX)
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(column=Column.objects.create(row=Row.objects.create(slot=cls.slot)))
        cls.tile.target = cls.dm_one
        cls.tile.save()

    def test_target(self):
        response = self.client.get(reverse('home'))
        self.assertHTMLEqual('\n        <div id="header">\n            Header slot\n        </div>\n        <div id="content">\n            <div class="composer-row None">\n                <div class="composer-column composer-column-8 None">\n                    <div class="composer-tile None" data-oid="%s">\n                        I am DummyModel1 One\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>' % self.tile.id, response.content)


class TemplateTagsCTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsCTestCase, cls).setUpTestData()
        cls.dm_one = DummyModel2.objects.create(title='One')
        cls.slot = Slot.objects.create(slot_name='content', url=HOME_REGEX)
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(column=Column.objects.create(row=Row.objects.create(slot=cls.slot)))
        cls.tile.target = cls.dm_one
        cls.tile.save()

    def test_target(self):
        response = self.client.get(reverse('home'))
        self.assertHTMLEqual('\n        <div id="header">\n            Header slot\n        </div>\n        <div id="content">\n            <div class="composer-row None">\n                <div class="composer-column composer-column-8 None">\n                    <div class="composer-tile None" data-oid="%s">\n                        I am a tile for DummyModel2 One\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>' % self.tile.id, response.content)


class TemplateTagsDTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsDTestCase, cls).setUpTestData()
        cls.slot = Slot.objects.create(slot_name='header', url='^' + reverse('aaa'))
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(column=Column.objects.create(row=Row.objects.create(slot=cls.slot)))
        cls.tile.view_name = 'header'
        cls.tile.save()

    def test_header(self):
        response = self.client.get(reverse('aaa'))
        self.assertHTMLEqual('\n        <div id="header">\n        \t<div class="composer-row None">\n            \t<div class="composer-column composer-column-8 None">\n                \t<div class="composer-tile None" data-oid="%s">\n                    \tI am the header\n                    </div>\n                </div>\n\t        </div>\n        </div>\n        <div id="content">\n            I am aaa. I live at /aaa/.\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>' % self.tile.id, response.content)
        response = self.client.get(reverse('bbb'))
        self.assertHTMLEqual('\n        <div id="header">\n        \t<div class="composer-row None">\n            \t<div class="composer-column composer-column-8 None">\n                \t<div class="composer-tile None" data-oid="%s">\n                    \tI am the header\n                    </div>\n                </div>\n\t        </div>\n        </div>\n        <div id="content">\n            I am bbb. I live at /aaa/bbb/.\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>' % self.tile.id, response.content)


class TemplateTagsETestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsETestCase, cls).setUpTestData()
        cls.slot = Slot.objects.create(slot_name='header', url=HOME_REGEX)
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(column=Column.objects.create(row=Row.objects.create(slot=cls.slot)), markdown='***I am bold markdown***')
        cls.tile.save()

    def test_tile_markdown(self):
        response = self.client.get(reverse('home'))
        self.assertHTMLEqual('\n        <div id="header">\n        \t<div class="composer-row None">\n            \t<div class="composer-column composer-column-8 None">\n                \t<div class="composer-tile None" data-oid="%s">\n                        <p><strong><em>I am bold markdown</em></strong></p>\n                    </div>\n                </div>\n\t        </div>\n        </div>\n        <div id="content">\n            Content slot\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>' % self.tile.id, response.content)


class TemplateTagsContextTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsContextTestCase, cls).setUpTestData()
        cls.slot = Slot.objects.create(slot_name='default_slot_context', url='^' + reverse('slot_context'), title='test_title_for_base_slot')
        cls.slot.sites = Site.objects.all()
        cls.slot.save()

    def test_default_slot(self):
        response = self.client.get(reverse('slot_context'))
        self.assertEqual(response.context['object'], self.slot)
        self.assertHTMLEqual('\n        <div id="header">\n            Header slot\n        </div>\n        <div id="content">\n            Has a slot that passes default context. This is the default slot context title: test_title_for_base_slot\n        </div>\n        <div id="footer">\n            Footer slot\n        </div>', response.content)
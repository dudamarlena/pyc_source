# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/tests/test_breadcrumbs.py
# Compiled at: 2017-07-06 08:35:55
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from navbuilder import models
from navbuilder.tests.test_base import load_fixtures, load_crumb_fixtures
from django.template import Context, Template
crumb_template_1 = Template("{% load navbuilder_tags %}{% navbuilder_breadcrumbs 'menu-1' %}")
crumb_template_2 = Template("{% load navbuilder_tags %}{% navbuilder_breadcrumbs 'menu-2' %}")
crumb_template_3 = Template("{% load navbuilder_tags %}{% navbuilder_breadcrumbs 'menu-3' %}")

class BreadcrumbsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        load_fixtures(self)
        load_crumb_fixtures(self)
        self.menuitem.link = None
        self.sub_menuitem_2.link = self.link
        return

    def test_single_level(self):
        out = crumb_template_2.render(Context({'object': self.link}))
        self.assertHTMLEqual(out, '\n                <a class="Crumb" href="/link/1/" title="Link 1"\n                target="" data-slug="link-1">\n                    Link 1\n                </a>\n                ')

    def test_multilevel(self):
        out = crumb_template_1.render(Context({'object': self.link}))
        self.assertHTMLEqual(out, '\n                <a class="Crumb" href="/link/1/"\n                title="Link 1" target="" data-slug="link-1">\n                    Link 1\n                </a>\n                >\n                <a class="Crumb" data-slug="link-1" href="/link/1/"\n                target="blank" title="Link 1">\n                    Link 1\n                </a>\n                ')

    def test_menu_slug_not_found(self):
        out = crumb_template_3.render(Context({'object': self.link}))
        self.assertIn('Link 1', out)

    def test_no_matching_menuitem(self):
        self.menuitem_2.link = None
        out = crumb_template_3.render(Context({'object': self.link_2}))
        self.assertHTMLEqual('', out)
        return

    def tearDown(self):
        pass
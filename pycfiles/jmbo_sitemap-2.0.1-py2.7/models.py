# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_sitemap/models.py
# Compiled at: 2015-07-13 06:41:00
from django.db import models
from django.template.loader import get_template_from_string
from django.template import Context
try:
    from django.utils.module_loading import import_string as importer
except ImportError:
    from django.utils.module_loading import import_by_path as importer

from django.conf import settings
from preferences.models import Preferences
from ckeditor.fields import RichTextField
from south.modelsinspector import add_introspection_rules
from foundry.models import Menu, Navbar, Page
try:
    generator = importer(settings.JMBO_SITEMAP['generator'])
except (AttributeError, KeyError):
    generator = None

DRAFT_TEMPLATE = '\n{% load i18n %}\n<html>\n<body>\n\n{% if navbars %}\n    {% trans "Navbars" %}:\n    <ul>\n    {% for navbar in navbars %}\n        <li>{{ navbar.title }}</li>\n        <li>\n            <ul>\n                {% for link in navbar.links %}\n                    <li><a href="{{ link.get_absolute_url }}">{{ link.title }}</a></li>\n                {% endfor %}\n            </ul>\n        </li>\n    {% endfor %}\n    </ul>\n{% endif %}\n\n{% if menus %}\n    {% trans "Menus" %}:\n    <ul>\n    {% for menu in menus %}\n        <li>{{ menu.title }}</li>\n        <li>\n            <ul>\n                {% for link in menu.links %}\n                    <li><a href="{{ link.get_absolute_url }}">{{ link.title }}</a></li>\n                {% endfor %}\n            </ul>\n        </li>\n    {% endfor %}\n    </ul>\n{% endif %}\n\n{% if pages %}\n    {% trans "Pages" %}:\n    <ul>\n    {% for page in pages %}\n        <li><a href="{{ page.get_absolute_url }}">{{ page.title }}</a></li>\n    {% endfor %}\n    </ul>\n{% endif %}\n\n</body>\n<html>\n'

class HTMLSitemap(Preferences):
    content = RichTextField(null=True, blank=True)
    draft = RichTextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'HTML Sitemap'

    def generate_draft(self):
        if generator is not None:
            html = generator()
        else:
            navbars = []
            for navbar in Navbar.objects.filter(sites__in=self.sites.all()).order_by('title'):
                navbar.links = []
                for o in navbar.navbarlinkposition_set.select_related().all().order_by('position'):
                    navbar.links.append(o.link)

                navbars.append(navbar)

            menus = []
            for menu in Menu.objects.filter(sites__in=self.sites.all()).order_by('title'):
                menu.links = []
                for o in menu.menulinkposition_set.select_related().all().order_by('position'):
                    menu.links.append(o.link)

                menus.append(menu)

            pages = Page.objects.filter(sites__in=self.sites.all()).order_by('title')
            template = get_template_from_string(DRAFT_TEMPLATE)
            c = dict(navbars=navbars, menus=menus, pages=pages)
            html = template.render(Context(c))
        self.draft = html
        self.save()
        return

    def make_draft_live(self):
        self.content = self.draft
        self.draft = ''
        self.save()


add_introspection_rules([], ['^ckeditor\\.fields\\.RichTextField'])
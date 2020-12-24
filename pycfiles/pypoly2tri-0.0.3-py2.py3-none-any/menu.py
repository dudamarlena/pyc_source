# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/webpage/menu.py
# Compiled at: 2011-11-05 10:43:07
import os, types, sys, pypoly
from pypoly.content.url import URL
from pypoly.content.webpage import Content, ContentType

class MenuObject(list, Content):

    def __init__(self, *args, **options):
        self.title = ''
        Content.__init__(self, *args, **options)


class Menu(MenuObject):
    xml = None
    type = ContentType('menu')
    submenus = []

    def __init__(self, *args, **options):
        MenuObject.__init__(self, *args, **options)
        self.submenus = []

    def append(self, item):
        if isinstance(item, Menu):
            if len(item) > 0 or len(item.submenus) > 0:
                self.submenus.append(item)
        elif isinstance(item.url, URL) and item.url.is_accessible():
            MenuObject.append(self, item)

    def generate(self, *template_file):
        menu = pypoly.template.load_web(*template_file)
        xml = menu.generate(menu=self)
        return xml

    def __call__(self, *template_file):
        return self.generate(*template_file)


class MenuItem(MenuObject):
    type = ContentType('menu.item')

    def __init__(self, *args, **options):
        self.title = ''
        self.url = None
        self.description = ''
        MenuObject.__init__(self, *args, **options)
        return
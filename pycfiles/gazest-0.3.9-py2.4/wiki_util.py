# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/wiki_util.py
# Compiled at: 2007-10-20 15:07:41
""" Utility function for the Wiki.  This module is mostly there to
prevent circular include between markup.py and wiki_macros.py ."""
import urllib
extra_macros = {}

def get_namespace(page_slug):
    levels = page_slug.strip('/').split('/')
    if levels:
        return ('/').join(levels[:-1])
    else:
        return ''


def get_page(page_slug):
    levels = page_slug.strip('/').split('/')
    return levels[(-1)]


def normalize_page(page):
    return page.strip().capitalize()


def normalize_slug(slug):
    return ('/').join(map(normalize_page, slug.strip('/').split('/')))
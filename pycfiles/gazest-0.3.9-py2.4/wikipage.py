# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/wikipage.py
# Compiled at: 2007-10-16 05:26:40
from gazest.lib import wiki_util
from markdown import markdown

class WikiPage:
    __module__ = __name__

    def __init__(self, slug):
        self.slug = slug
        self.title = wiki_util.get_page(slug)
        self.html_renderer = markdown
        self.html_post_render_processors = []
        self.html_post_expand_processors = []
        self.sidebars = []
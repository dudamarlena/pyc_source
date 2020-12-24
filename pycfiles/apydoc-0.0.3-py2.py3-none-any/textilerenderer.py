# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/renderers/textilerenderer.py
# Compiled at: 2007-10-26 14:28:44
from apydia.renderers.base import HTMLRenderer
from textile import textile

class TextileRenderer(HTMLRenderer):
    __module__ = __name__
    name = 'textile'

    def _render(self, source):
        return textile(source)

    def render_description(self, desc):
        """ render full description (without title) """
        return self._render(desc.docstring)

    def render_short_desc(self, desc):
        """ render first paragraph (without title) """
        return self._render(desc.docstring)

    def render_title(self, desc):
        """ render title only """
        return self._render(desc.docstring[0:1])
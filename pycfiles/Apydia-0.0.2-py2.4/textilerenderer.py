# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
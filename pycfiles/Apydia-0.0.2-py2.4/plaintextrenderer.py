# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/renderers/plaintextrenderer.py
# Compiled at: 2007-10-26 14:28:44
from apydia.renderers.base import Renderer

class PlainTextRenderer(Renderer):
    __module__ = __name__
    name = ['plain', 'plaintext', 'text']

    def _render(self, source):
        return '<pre>%s</pre>' % source
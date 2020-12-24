# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linediff/macro.py
# Compiled at: 2006-06-29 10:43:23
from trac.core import *
from trac.wiki.api import IWikiMacroProvider
from trac.mimeview.patch import PatchRenderer
import inspect, difflib, time

class LineDiffMacro(Component):
    """Diff (and render) two lines of text."""
    __module__ = __name__
    implements(IWikiMacroProvider)

    def get_macros(self):
        """Yield the name of the macro based on the class name."""
        name = self.__class__.__name__
        if name.endswith('Macro'):
            name = name[:-5]
        yield name

    def get_macro_description(self, name):
        """Return the subclass's docstring."""
        return inspect.getdoc(self.__class__)

    def render_macro(self, req, name, content):
        lines = content.splitlines(1)
        pr = PatchRenderer(self.env)
        udiff = ('').join(difflib.unified_diff([lines[0]], [lines[1]], 'Line_1', 'Line_2', time.ctime(), time.ctime()))
        if not udiff:
            return ''
        self.log.debug("'%s'" % udiff)
        return pr.render(req, None, udiff)
        return
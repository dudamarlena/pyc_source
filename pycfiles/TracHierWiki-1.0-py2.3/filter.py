# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hierwiki/filter.py
# Compiled at: 2006-11-13 05:22:24
from trac.core import *
from trac.web.api import IRequestFilter
from trac.wiki.api import IWikiPageManipulator
from trac.wiki.model import WikiPage
from trac.wiki.web_ui import WikiModule
__all__ = ['EnforceHierarchyModule']

class EnforceHierarchyModule(Component):
    """This check that all subpaths under a wiki page exist.
    This enforces a hierarchy, and prevents accidental misspellings."""
    __module__ = __name__
    implements(IWikiPageManipulator)

    def prepare_wiki_page(self, *args):
        pass

    def validate_wiki_page(self, req, page):
        comps = page.name.split('/')
        del comps[-1]
        check = []
        for comp in comps:
            check.append(comp)
            check_page = WikiPage(self.env, ('/').join(check))
            if not check_page.exists:
                yield (
                 'name', 'Hierarchy component "%s" does not exist' % check_page.name)
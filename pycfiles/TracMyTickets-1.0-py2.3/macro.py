# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/mytickets/macro.py
# Compiled at: 2007-07-29 19:42:20
from trac.core import *
from trac.wiki.api import IWikiMacroProvider
from trac.ticket.query import TicketQueryMacro

class MyTicketsMacro(TicketQueryMacro):
    """A simple macro to show your tickets."""
    __module__ = __name__
    implements(IWikiMacroProvider)

    def render_macro(self, req, name, content):
        content = (content or '').split(',')
        content[0] = (content[0] + '&owner=%s' % req.authname).lstrip('&')
        content = (',').join(content)
        return super(MyTicketsMacro, self).render_macro(req, name, content)
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tickettree/web_ui.py
# Compiled at: 2011-05-27 11:27:00
from genshi.builder import tag
from trac.core import *
from trac.mimeview import Context
from trac.web.chrome import ITemplateProvider, INavigationContributor

class TicketTreeTemplateProvider(Component):
    """Provides templates and static resources for the TicketTree plugin."""
    implements(ITemplateProvider)

    def get_htdocs_dirs(self):
        """Return the absolute path of a directory containing additional
        static resources (such as images, style sheets, etc).
        """
        from pkg_resources import resource_filename
        return [
         (
          'tickettree', resource_filename('tickettree', 'htdocs'))]

    def get_templates_dirs(self):
        """
        Return the absolute path of the directory containing the provided
        Genshi templates.
        """
        return []


class TicketTreeSystem(Component):
    """Implements the Ticket Tree tab."""
    implements(INavigationContributor)

    def get_active_navigation_item(self, req):
        if 'TICKET_VIEW' in req.perm:
            return 'tickettree'

    def get_navigation_items(self, req):
        if 'TICKET_VIEW' in req.perm:
            yield (
             'mainnav', 'tickettree',
             tag.a('Ticket Tree', href=req.href.wiki() + '/TicketTree', accesskey='T'))
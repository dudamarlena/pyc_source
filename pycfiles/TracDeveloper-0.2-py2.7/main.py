# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tracdeveloper/main.py
# Compiled at: 2011-09-06 06:16:46
import re
from genshi.builder import tag
from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor, ITemplateProvider
from trac.prefs.api import IPreferencePanelProvider
__all__ = [
 'DeveloperPlugin']

class DeveloperPlugin(Component):
    implements(INavigationContributor, IRequestHandler, ITemplateProvider, IPreferencePanelProvider)

    def get_active_navigation_item(self, req):
        return 'developer'

    def get_navigation_items(self, req):
        yield (
         'metanav', 'developer',
         tag.a('Developer Tools', href=req.href.developer()))

    def match_request(self, req):
        return re.match('/developer/?$', req.path_info)

    def process_request(self, req):
        return (
         'developer/index.html', {}, None)

    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [
         resource_filename(__name__, 'templates')]

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [
         (
          'developer', resource_filename(__name__, 'htdocs'))]

    def get_preference_panels(self, req):
        yield ('developer', 'Developer Options')

    def render_preference_panel(self, req, panel):
        if req.method == 'POST':
            req.session['developer.js.enable_debug'] = req.args.get('enable_debug', '0')
        return (
         'developer/prefs_developer.html', {})
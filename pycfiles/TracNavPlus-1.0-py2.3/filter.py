# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/navplus/filter.py
# Compiled at: 2007-08-28 18:03:59
from trac.core import *
from trac.web.api import IRequestFilter
from trac.web.chrome import INavigationContributor
from trac.util.html import html as tag

class NavPlusModule(Component):
    """The filter to add/remove/migrate navigation items."""
    __module__ = __name__
    implements(INavigationContributor)

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, content_type):
        return (
         template, content_type)

    def get_active_navigation_item(self, req):
        return ''

    def get_navigation_items(self, req):
        for (key, value) in self.config.options('navplus'):
            if value == 'mainnav' or value == 'metanav':
                title = self.config.get('navplus', key + '.title') or ''
                url = self.config.get('navplus', key + '.url') or ''
                if not url.startswith('/') and ':' not in url:
                    url = req.href(url)
                yield (
                 value, key, tag.a(title, href=url))
# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/navplus/admin.py
# Compiled at: 2007-08-29 03:01:05
from pkg_resources import resource_filename
from trac.core import *
from trac.web.chrome import ITemplateProvider, add_stylesheet
from trac.perm import IPermissionRequestor
from webadmin.web_ui import IAdminPageProvider

class NavPlusAdminModule(Component):
    """An admin panel for the NavPlus plugin."""
    __module__ = __name__
    implements(IAdminPageProvider, ITemplateProvider, IPermissionRequestor)

    def get_admin_pages(self, req):
        if req.perm.has_permission('NAV_ADMIN'):
            yield (
             'nav', 'Navigation', 'add', 'Add')

    def process_admin_request(self, req, cat, page, path_info):
        if page == 'add':
            return self._process_add_request(req, cat, page, path_info)

    def get_htdocs_dirs(self):
        return [
         (
          'navplus', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return [
         resource_filename(__name__, 'templates')]

    def get_permission_actions(self):
        yield 'NAV_ADMIN'

    def _process_add_request(self, req, cat, page, path_info):
        if req.method == 'POST':
            if 'add' in req.args:
                title = req.args['title']
                url = req.args['url']
                bar = req.args['bar']
                if not title or not url or not bar:
                    raise TracError('All fields are required')
                if bar not in ('mainnav', 'metanav'):
                    raise TracError('Invalid bar')
                name = title.lower().replace(' ', '_')
                self.config.set('navplus', name, bar)
                self.config.set('navplus', name + '.title', title)
                self.config.set('navplus', name + '.url', url)
                self.config.save()
            elif 'remove' in req.args:
                for name in req.args.getlist('sel'):
                    self.config.remove('navplus', name)
                    self.config.remove('navplus', name + '.title')
                    self.config.remove('navplus', name + '.url')
                    self.config.save()

            req.redirect(req.href.admin(cat, page))
        items = {'mainnav': [], 'metanav': []}
        for (key, value) in self.config.options('navplus'):
            if value == 'mainnav' or value == 'metanav':
                title = self.config.get('navplus', key + '.title') or ''
                url = self.config.get('navplus', key + '.url') or ''
                items[value].append({'name': key, 'title': title, 'url': url})

        req.hdf['navplus.items'] = items
        add_stylesheet(req, 'navplus/admin.css')
        return ('admin_navplus_add.cs', None)
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tracext/piwik/admin.py
# Compiled at: 2012-05-02 14:27:07
import pkg_resources
from trac.admin import IAdminPanelProvider
from trac.config import Option, _TRUE_VALUES
from trac.core import Component, implements
from trac.web.chrome import add_stylesheet, add_script
from trac.util.translation import domain_functions
(_, tag_, N_, add_domain) = domain_functions('piwik4trac', ('_', 'tag_', 'N_', 'add_domain'))

class PiwikAdmin(Component):
    config = env = log = None
    options = {}
    implements(IAdminPanelProvider)

    def __init__(self):
        locale_dir = pkg_resources.resource_filename(__name__, 'locale')
        add_domain(self.env.path, locale_dir)

    def get_admin_panels(self, req):
        if req.perm.has_permission('TRAC_ADMIN'):
            yield (
             'piwik', 'Piwik', 'analytics', _('Title analytics'))

    def render_admin_panel(self, req, cat, page, path_info):
        if req.locale is not None:
            add_script(req, 'piwik/%s.js' % req.locale)
        add_stylesheet(req, 'piwik/piwik.css')
        if req.method.lower() == 'post':
            self.config.set('piwik', 'tracking_site', req.args.get('tracking_site'))
            self.config.set('piwik', 'tracking_server', req.args.get('tracking_server'))
            self.config.save()
        self.update_config()
        return ('piwik_admin.html', {'piwik': self.options})

    def update_config(self):
        for option in [ option for option in Option.registry.values() if option.section == 'piwik'
                      ]:
            if option.name in ('admin_logging', 'authenticated_logging', 'outbound_link_tracking'):
                value = self.config.getbool('piwik', option.name, option.default)
                option.value = value
            else:
                value = self.config.get('piwik', option.name, option.default)
                option.value = value
            self.options[option.name] = option
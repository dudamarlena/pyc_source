# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tracext/google/ads/admin.py
# Compiled at: 2008-09-03 14:03:45
from trac.core import Component, implements
from trac.admin import IAdminPanelProvider
from trac.config import Option, _TRUE_VALUES
from trac.util.text import unicode_unquote
from trac.web.chrome import add_stylesheet

class GoogleAdsAdmin(Component):
    config = env = log = None
    implements(IAdminPanelProvider)
    options = {}

    def get_admin_panels(self, req):
        if req.perm.has_permission('TRAC_ADMIN'):
            yield ('google', 'Google', 'ads', 'Ads')

    def render_admin_panel(self, req, cat, page, path_info):
        add_stylesheet(req, 'googlesads/googleads.css')
        self.log.debug('Saving Google Ads Options')
        if req.method == 'POST':
            self.config.set('google.ads', 'hide_for_authenticated', req.args.get('hide_for_authenticated') in _TRUE_VALUES)
            self.config.save()
            code = req.args.get('ads_html')
            db = self.env.get_db_cnx()
            cursor = db.cursor()
            cursor.execute('SELECT value FROM system WHERE name=%s', ('google.ads_html', ))
            if cursor.fetchone():
                self.log.debug('Updating Ads HTML Code')
                cursor.execute('UPDATE system SET value=%s WHERE name=%s', (
                 code, 'google.ads_html'))
            else:
                self.log.debug('Inserting Ads HTML Code')
                cursor.execute('INSERT INTO system (name,value) VALUES (%s,%s)', (
                 'google.ads_html', code))
            db.commit()
            req.redirect(req.href.admin(cat, page))
        self._update_config()
        return ('google_ads_admin.html', {'ads_options': self.options})

    def _update_config(self):
        for option in [ option for option in Option.registry.values() if option.section == 'google.ads'
                      ]:
            if option.name == 'hide_for_authenticated':
                option.value = self.config.getbool('google.ads', option.name, True)
            elif option.name == 'ads_html':
                db = self.env.get_db_cnx()
                cursor = db.cursor()
                cursor.execute('SELECT value FROM system WHERE name=%s', ('google.ads_html', ))
                code = cursor.fetchone()
                if code:
                    code = unicode_unquote(code[0])
                option.value = code or ''
            else:
                option.value = self.config.get('google.ads', option.name, option.default)
            self.options[option.name] = option
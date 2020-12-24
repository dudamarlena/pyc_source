# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\plugins\themes.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 3417 bytes
from __future__ import print_function
import httplib2
from django.template import loader
import django.core.cache as cache
from django.utils import six
import django.utils.translation as _
from xadmin.sites import site
from xadmin.models import UserSettings
from xadmin.views import BaseAdminPlugin, BaseAdminView
from xadmin.util import static, json
import six
if six.PY2:
    import urllib
else:
    import urllib.parse
THEME_CACHE_KEY = 'xadmin_themes'

class ThemePlugin(BaseAdminPlugin):
    enable_themes = False
    user_themes = None
    use_bootswatch = False
    default_theme = static('xadmin/css/themes/bootstrap-xadmin.css')
    bootstrap2_theme = static('xadmin/css/themes/bootstrap-theme.css')

    def init_request(self, *args, **kwargs):
        return self.enable_themes

    def _get_theme(self):
        if self.user:
            try:
                return UserSettings.objects.get(user=(self.user), key='site-theme').value
            except Exception:
                pass

        if '_theme' in self.request.COOKIES:
            if six.PY2:
                func = urllib.unquote
            else:
                func = urllib.parse.unquote
            return func(self.request.COOKIES['_theme'])
        return self.default_theme

    def get_context(self, context):
        context['site_theme'] = self._get_theme()
        return context

    def get_media(self, media):
        return media + self.vendor('jquery-ui-effect.js', 'xadmin.plugin.themes.js')

    def block_top_navmenu(self, context, nodes):
        themes = [
         {'name':_('Default'), 
          'description':_('Default bootstrap theme'),  'css':self.default_theme},
         {'name':_('Bootstrap2'), 
          'description':_('Bootstrap 2.x theme'),  'css':self.bootstrap2_theme}]
        select_css = context.get('site_theme', self.default_theme)
        if self.user_themes:
            themes.extend(self.user_themes)
        elif self.use_bootswatch:
            ex_themes = cache.get(THEME_CACHE_KEY)
            if ex_themes:
                themes.extend(json.loads(ex_themes))
            else:
                ex_themes = []
                try:
                    h = httplib2.Http()
                    resp, content = h.request('https://bootswatch.com/api/3.json', 'GET', '', headers={'Accept':'application/json', 
                     'User-Agent':self.request.META['HTTP_USER_AGENT']})
                    if six.PY3:
                        content = content.decode()
                    watch_themes = json.loads(content)['themes']
                    ex_themes.extend([{'name':t['name'],  'description':t['description'],  'css':t['cssMin'],  'thumbnail':t['thumbnail']} for t in watch_themes])
                except Exception as e:
                    try:
                        print(e)
                    finally:
                        e = None
                        del e

                cache.set(THEME_CACHE_KEY, json.dumps(ex_themes), 86400)
                themes.extend(ex_themes)
        nodes.append(loader.render_to_string('xadmin/blocks/comm.top.theme.html', {'themes':themes,  'select_css':select_css}))


site.register_plugin(ThemePlugin, BaseAdminView)
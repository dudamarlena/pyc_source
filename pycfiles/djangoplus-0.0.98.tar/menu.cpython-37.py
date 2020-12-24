# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/ui/components/navigation/menu.py
# Compiled at: 2019-04-02 21:54:36
# Size of source mod 2**32: 2852 bytes
from django.conf import settings
from djangoplus.cache import CACHE
from djangoplus.utils import permissions
from djangoplus.ui.components import Component

class Menu(Component):

    def __init__(self, request, app_settings=None):
        super(Menu, self).__init__('menu', request)
        self.subitems = dict()
        self.settings = app_settings
        self._load()

    def _add(self, description, url, icon=None, style='ajax'):
        url = '/breadcrumbs/reset{}'.format(url)
        levels = description.split('::')
        for i, level in enumerate(levels):
            levels[i] = level.strip()

        if levels[0] not in self.subitems:
            self.subitems[levels[0]] = dict(urls=[], subitems=(dict()), icon=None)
        if not self.subitems[levels[0]]['icon']:
            self.subitems[levels[0]]['icon'] = icon
        if len(levels) == 1:
            self.subitems[levels[0]]['urls'].append((url, style))
        else:
            subitems = self.subitems[levels[0]]['subitems']
            if levels[1] not in subitems:
                item = dict(urls=[], subitems=(dict()))
                subitems[levels[1]] = item
            if len(levels) == 2:
                subitems[levels[1]]['urls'].append((url, style))
            else:
                subitems = subitems[levels[1]]['subitems']
                if levels[2] not in subitems:
                    item = dict(urls=[], subitems=(dict()))
                    subitems[levels[2]] = item
                if len(levels) == 3:
                    subitems[levels[2]]['urls'].append((url, style))
                else:
                    subitems = subitems[levels[2]]['subitems']
                    if levels[3] not in subitems:
                        subitems[levels[3]] = dict(urls=[])
                    subitems[levels[3]]['urls'].append((url, style))

    def _load(self):
        if settings.DEBUG or 'side_menu' not in self.request.session:
            for item in CACHE['VIEWS']:
                if item['menu']:
                    can_view = permissions.check_group_or_permission(self.request, item['can_view'])
                    if can_view:
                        if 'groups' in item:
                            can_view = permissions.check_group_or_permission(self.request, item['groups'])
                    if can_view:
                        self._add(item['menu'], item['url'], item['icon'], item.get('style', 'ajax'))

            self.request.session['side_menu'] = super(Menu, self).__str__()
            self.request.session['side_menu_size'] = len(list(self.subitems.keys()))
            self.request.session.save()

    def __str__(self):
        return self.request.session['side_menu']
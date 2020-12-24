# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/pytigon/pytigon/prj/_schwiki/schwiki/__init__.py
# Compiled at: 2020-03-15 04:16:13
# Size of source mod 2**32: 2198 bytes
import django.utils.translation as _
ModuleTitle = _('main tools')
Title = _('Wiki')
Perms = True
Index = 'None'
Urls = (
 (
  'table/Page/-/form/list/?schtml=desktop', _('Wiki'), 'wiki.change_page', 'wx.ART_HELP_SIDE_PANEL'),
 (
  'table/PageObjectsConf/-/form/list/?schtml=desktop', _('Page objects conf.'), None, 'client://actions/document-properties.png'),
 (
  'table/WikiConf/-/form/list/?schtml=desktop', _('Publish options'), None, 'png://categories/applications-system.png'))
UserParam = {}
import django.utils.translation as _

def AdditionalUrls(app_pack, lang):
    from .models import Page
    ret = []
    ret_buf = []
    for object in Page.objects.filter(published=True):
        if object.menu:
            elements = object.menu.split(',')
            menu_path = elements[0].split('/')
            app_pack_name = menu_path[0]
            if app_pack:
                if app_pack_name:
                    if app_pack != app_pack_name:
                        continue
            module_title = ''
            app_name = ''
            if len(menu_path) > 1:
                module_title = menu_path[1]
            else:
                if len(menu_path) > 2:
                    app_name = menu_path[2]
                elif len(elements) > 1:
                    if elements[1]:
                        icon = elements[1]
                    else:
                        icon = 'client://apps/utilities-terminal.png'
                else:
                    icon = 'client://apps/utilities-terminal.png'
                if len(elements) > 2:
                    lp = elements[2]
                else:
                    lp = '00'
            if len(elements) > 3:
                if elements[3]:
                    if lang != elements[3]:
                        continue
            ret_buf.append((lp, ('schwiki/' + object.subject + '/' + object.name + '/view/?schtml=1', object.description, object.rights_group, icon, module_title, _(module_title), app_name, _(app_name))))

    if ret_buf:
        buf = sorted(ret_buf, key=(lambda pos: pos[0]))
        for pos in buf:
            ret.append(pos[1])

        return ret
    return []
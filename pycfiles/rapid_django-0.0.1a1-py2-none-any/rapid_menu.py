# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/templatetags/rapid_menu.py
# Compiled at: 2015-09-18 17:41:33
__author__ = 'marcos.medeiros'
import locale
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from rapid.views import registry, ModelData
from django.utils.translation import to_locale, get_language
register = template.Library()
try:
    locale.setlocale(locale.LC_ALL, str(to_locale(get_language())))
except:
    locale.setlocale(locale.LC_ALL, str('C'))

def _app_menu(app, request):
    models = list(app.models)
    models.sort(key=lambda m: ModelData(m).model_name(), cmp=locale.strcoll)
    sub = '<li class="menu-group"><div>%s</div><ul class="submenu">\n' % escape(app.menu_name.capitalize())
    has_model = False
    for m in models:
        st = registry.model_entry(m).get('list')
        if st:
            read = st.permission.model(request)
            if read:
                has_model = True
                cd = ModelData(st.model)
                sub += '<li><a href="%s">%s</a></li>\n' % (
                 registry.get_url_of_action(m, 'list'),
                 escape(cd.model_name_plural().title()))

    sub += '</ul></li>\n'
    if has_model:
        return sub
    return ''


@register.simple_tag
def menu(request):
    ret = '\n    <nav id="menu">\n    <style scoped>\n        nav li.menu-group{\n            cursor: pointer;\n        }\n        nav li.menu-group.collapsed > ul{\n            display: none;\n        }\n    </style>\n    '
    ret += '<ul class="menu">\n'
    mm = registry.modules()
    mm.sort(key=lambda a: a.menu_name, cmp=locale.strcoll)
    for m in mm:
        ret += _app_menu(m, request)

    ret += '\n    </ul>\n    <script>\n        $(document).ready(function(){\n            $("nav li.menu-group").addClass("collapsed");\n            $("nav li.menu-group > div").click(function(){$(this).parent().toggleClass("collapsed")});\n        });\n    </script>\n    </nav>\n    '
    return mark_safe(ret)
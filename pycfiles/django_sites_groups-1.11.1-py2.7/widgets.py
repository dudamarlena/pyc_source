# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sites_groups/widgets.py
# Compiled at: 2017-05-06 10:44:18
from django.forms.widgets import SelectMultiple
from django.template import Context
from django.utils.translation import ugettext as _
from django.utils.html import mark_safe
from sites_groups.models import SitesGroup
TEMPLATE = '\n{% if groups %}\n{% load i18n %}\n<script type="text/javascript">\nfunction on{{ name }}SitesGroupClick(sender){\n    var select = document.getElementById(\'id_{{ name }}\');\n    var ids = sender.getAttribute(\'site_ids\').split(\',\');\n    for (var i=0; i < select.options.length; i++)\n    {\n        var value = select[i].value;\n        if (ids.indexOf(value) != -1)\n            select[i].selected = true;\n        else\n            select[i].selected = false;\n    }\n}\n</script>\n{% trans "Click an item to select" %}\n<ul style="margin: 0 0 0 8px; padding: 0;">\n    {% for group in groups %}\n        <li>\n            <a href="#" onclick="on{{ name }}SitesGroupClick(this);return false;" site_ids="{{ group.site_ids|join:"," }}">\n                {{ group.title }}\n            </a>\n        </li>\n    {% endfor %}\n</ul>\n{% endif %}'

class SitesGroupsWidget(SelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        try:
            from django.template import engines
        except ImportError:
            from django.template.loader import get_template_from_string as func
        else:
            func = engines['django'].from_string

        template = func(TEMPLATE)
        di = dict(name=name, groups=SitesGroup.objects.all())
        html = template.render(di)
        try:
            select = super(SitesGroupsWidget, self).render(name, value, attrs=attrs, choices=choices)
        except TypeError:
            select = super(SitesGroupsWidget, self).render(name, value, attrs=attrs)

        return mark_safe('<table style="border: 0;"><tr><td>' + select + '</td><td>' + html + '</td></tr></table>')
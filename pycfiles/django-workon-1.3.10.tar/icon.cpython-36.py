# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/forms/icon.py
# Compiled at: 2018-08-30 07:18:16
# Size of source mod 2**32: 3946 bytes
import re, os, logging, locale, json, datetime, time
from django import forms
from django.conf import settings
from django.db.models import CharField
from django.core.exceptions import ValidationError
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
import workon.utils
__all__ = [
 'IconField', 'IconInput']

class IconField(forms.CharField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = IconInput(attrs={'placeholder': '#xxxxxx'})
        (super().__init__)(*args, **kwargs)


class IconInput(forms.widgets.TextInput):

    class Media:
        js = [
         'contrib/forms/icon.js']
        css = {'all': ()}

    def __init__(self, *args, **kwargs):
        self.styles = kwargs.pop('styles')
        (super(IconInput, self).__init__)(*args, **kwargs)

    def render(self, name, value, attrs={}, **kwargs):
        root = workon.utils.get_project_root()
        id = str(time.time()).replace('.', '')
        html = '<style>\n\n            .contrib-icon-widget {\n                color:rgb(102, 71, 30); margin:5px; text-decoration: none; cursor: pointer;   display: inline-block;\n                font-size: 21px;\n                transition: all 0.4s ease-out;\n            }\n            .contrib-icon-widget:hover {\n                text-decoration: none; color:rgb(30, 31, 102);   display: inline-block;\n                transition: all 0.4s ease-out;\n            }\n            .contrib-icon-widget.active,\n            .contrib-icon-widget.active i,\n            .contrib-icon-widget.active a,\n            .contrib-icon-widget.active span {\n                color:green; font-size: 25px; font-weight: bold;\n            }\n\n        </style>\n        <div id="icons-%s">\n            <div style="" class="contrib-icon-widget-tabs">' % id
        for title, local_path, path, classname, prefix in self.styles:
            html += '<link href="%s" rel="stylesheet">' % path

        tabs = '<ul>'
        contents = ''
        i = 1
        for title, local_path, path, classname, prefix in self.styles:
            filec = open(os.path.join(root, local_path), 'rb').read()
            filec = filec.replace('\\s', '')
            tabs += '<li><a class="contrib-icon-widget-tabs-control" href="#tab-%s-%s">%s</a></li>' % (id, i, title)
            contents += '<div class="contrib-icon-widget-tabs-content" id="tab-%s-%s" style="display:none;">' % (id, i)
            for item in re.finditer('\\.(%s[\\w\\-\\.]+)\\:before' % classname, filec):
                classname = item.group(1)
                classname = prefix + ' ' + classname
                contents += '<a class="contrib-icon-widget %s" data-value="%s" data-input="#%s"><i class="%s"></i></a>' % (
                 'active' if value == classname else '',
                 classname,
                 attrs.get('id', ''),
                 classname)

            contents += '</div>'
            i += 1

        tabs += '</ul>'
        html += tabs + contents
        html += '</div>\n                %(inherit)s\n            </div>\n        ' % {'inherit':super(IconInput, self).render(name, value, attrs=attrs, **kwargs), 
         'id':id}
        return mark_safe(html)
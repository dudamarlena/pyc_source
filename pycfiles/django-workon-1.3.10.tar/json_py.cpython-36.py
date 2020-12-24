# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/forms/json_py.py
# Compiled at: 2018-08-30 07:17:09
# Size of source mod 2**32: 1763 bytes
import re, os, logging, locale, json, datetime, time
from django import forms
from django.conf import settings
from django.db.models import CharField
from django.core.exceptions import ValidationError
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
logger = logging.getLogger(__name__)

class JSONField(forms.CharField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = JSONReadOnlyInput(expanded=(kwargs.pop('expanded', False)))
        (super(JSONField, self).__init__)(*args, **kwargs)


class JSONReadOnlyInput(forms.widgets.TextInput):

    class Media:
        css = {'all': (settings.STATIC_URL + 'contrib/vendors/pretty-json/pretty-json.css',)}
        js = (
         settings.STATIC_URL + 'contrib/packages/json.js',)

    def __init__(self, *args, **kwargs):
        self.expanded = kwargs.pop('expanded', False)
        (super(JSONReadOnlyInput, self).__init__)(*args, **kwargs)

    def render(self, name, value, attrs={}, **kwargs):
        if 'id' not in attrs:
            attrs['id'] = 'id_%s' % name
        obj = json.dumps(value, ensure_ascii=False)
        return '<div id="%(id)s" ></div><script type="text/javascript">\n\n                    var node = new PrettyJSON.view.Node({\n                        el: $(\'#%(id)s\'),\n                        data: JSON.parse(%(obj)s),\n                    });\n                    %(expandAll)s\n                </script>\n                ' % {'id':attrs['id'], 
         'obj':obj, 
         'expandAll':'node.expandAll();' if self.expanded else ''}
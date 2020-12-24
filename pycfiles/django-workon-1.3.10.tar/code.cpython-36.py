# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/forms/code.py
# Compiled at: 2018-08-30 07:18:53
# Size of source mod 2**32: 2254 bytes
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets as admin_widgets
from django.forms.utils import flatatt
from django.utils.html import strip_tags
from django.utils.html import escape
from django.template import Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext as _
import json
try:
    from django.utils.encoding import smart_text as smart_unicode
except ImportError:
    try:
        from django.utils.encoding import smart_unicode
    except ImportError:
        from django.forms.util import smart_unicode

__all__ = [
 'CodeField', 'CodeInput']

class CodeField(forms.CharField):

    def __init__(self, *args, **kwargs):
        (super(CodeField, self).__init__)(*args, **kwargs)


class CodeInput(forms.Textarea):

    def __init__(self, *args, **kwargs):
        self.mode = kwargs.get('attrs', {}).get('mode', 'python')
        (super().__init__)(*args, **kwargs)

    def render_script(self, id):
        return '\n                <div id="%(id)s_ace_editor"></div>\n                <script type="text/javascript">\n                    var %(id)s_ed = ace.edit("%(id)s_ace_editor");\n                    %(id)s_ed.setTheme("ace/theme/monokai");\n                    %(id)s_ed.getSession().setMode("ace/mode/%(mode)s");\n                    //%(id)s_ed.setPrintMarginColumn(150)\n                    %(id)s_ed.setOptions({\n                        maxLines: Infinity\n                    });\n                    %(id)s_ed.on("change", function(e) {\n                        $(\'#%(id)s\').val(%(id)s_ed.getValue());\n                    });\n                    %(id)s_ed.setValue($(\'#%(id)s\').val());\n                    %(id)s_ed.resize();\n\n                </script>\n                ' % {'id':id.replace('-', '_'),  'mode':self.mode}

    def render(self, name, value, attrs={}, **kwargs):
        if 'id' not in attrs:
            attrs['id'] = 'id_%s' % name
        attrs['style'] = 'display:none;'
        render = (super().render)(name, value, attrs, **kwargs)
        return mark_safe('%s%s' % (render, self.render_script(attrs['id'])))
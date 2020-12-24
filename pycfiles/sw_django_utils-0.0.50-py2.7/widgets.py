# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djutils/widgets.py
# Compiled at: 2017-06-22 08:38:26
from django import forms
from django.utils.safestring import mark_safe

class NameInput(forms.TextInput):
    media = forms.Media(js=['djutils/js/capitalize.js'])

    def render(self, name, *args, **kwargs):
        return super(NameInput, self).render(name, *args, **kwargs) + mark_safe(('\n                <script type="text/javascript">\n                    capitalize(\'input[type=text][name={}]\');\n                </script>\n            ').format(name))
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tube/widgets.py
# Compiled at: 2011-01-07 06:45:25
from django import forms
from django.utils.safestring import mark_safe

class RadioFieldImageRenderer(forms.widgets.RadioFieldRenderer):

    def render(self):
        """
        Outputs a <ul> for this set of radio fields.
        """
        output = []
        output.append('<table style="border: 0 solid black"><tr>')
        for choice in self.choices:
            output.append('\n<th style="border: 0 solid black">\n<center>\n<input type="radio" name="%s" value="%s" id="%s" >\n%s\n</center>\n<br />\n<img src="%s" height="130"/></th>' % (self.name, choice['file_path'], self.attrs['id'], choice['label'], choice['media_path']))

        output.append('</tr></table>')
        return mark_safe(('').join(output))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nijel/weblate/weblate/weblate/fonts/forms.py
# Compiled at: 2020-03-12 04:44:12
# Size of source mod 2**32: 1405 bytes
from django import forms
from weblate.fonts.models import Font, FontGroup, FontOverride

class FontForm(forms.ModelForm):

    class Meta:
        model = Font
        fields = ('font', )


class FontGroupForm(forms.ModelForm):

    class Meta:
        model = FontGroup
        fields = ('name', 'font')

    def __init__(self, data=None, project=None, **kwargs):
        (super().__init__)(data, **kwargs)
        self.fields['font'].queryset = self.fields['font'].queryset.filter(project=project)


class FontOverrideForm(forms.ModelForm):

    class Meta:
        model = FontOverride
        fields = ('language', 'font')
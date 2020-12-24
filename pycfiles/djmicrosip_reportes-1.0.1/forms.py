# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reportes\djmicrosip_reportes\forms.py
# Compiled at: 2016-06-24 19:09:18
from django import forms
import os
from .models import *
import autocomplete_light

class lineaForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=LineaArticulos.objects.all(), widget=autocomplete_light.ChoiceWidget('LineaArticulosAutocomplete'), required=False)

    def __init__(self, *args, **kwargs):
        super(lineaForm, self).__init__(*args, **kwargs)
        self.fields['linea'].widget.attrs['class'] = 'form-control'
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_exportaimportaprecios\djmicrosip_exportaimportaprecios\forms.py
# Compiled at: 2016-07-25 12:02:48
from django import forms
from .models import *
import os

class ArticulosSearchForm(forms.Form):
    linea = forms.ModelChoiceField(queryset=LineaArticulos.objects.all().order_by('nombre'), required=False)


IMPORT_FILE_TYPES = [
 '.xls']

class ImportarPreciosForm(forms.Form):
    archivo = forms.FileField()
    linea = forms.ModelChoiceField(queryset=LineaArticulos.objects.all().order_by('nombre'), required=False)
    moneda = forms.ModelChoiceField(queryset=Moneda.objects.all(), required=False)

    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        extension = os.path.splitext(archivo.name)[1]
        if extension not in IMPORT_FILE_TYPES:
            raise forms.ValidationError('%s is not a valid excel file. Please make sure your input file is an excel file' % extension)
        else:
            return archivo
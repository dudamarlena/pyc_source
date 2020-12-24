# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_comparadb\djmicrosip_comparadb\forms.py
# Compiled at: 2016-08-26 13:36:38
from django import forms
from .models import *
from django.conf import settings

class MultipleConexionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        bases_de_datos = settings.MICROSIP_DATABASES.keys()
        empresas = []
        for database_conexion in bases_de_datos:
            try:
                database_conexion = '%s' % database_conexion
            except UnicodeDecodeError:
                pass
            else:
                conexion_split = database_conexion.split('-')
                conexion_id = conexion_split[0]
                empresa = ('-').join(conexion_split[1:])
                conexion = ConexionDB.objects.get(pk=int(conexion_id))
                database_conexion_name = '%02d-%s' % (conexion.id, empresa)
                empresa_option = [database_conexion, database_conexion_name]
                empresas.append(empresa_option)

        super(MultipleConexionForm, self).__init__(*args, **kwargs)
        self.fields['empresas'] = forms.MultipleChoiceField(choices=empresas, widget=forms.CheckboxSelectMultiple)


class SingleConexionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        bases_de_datos = settings.MICROSIP_DATABASES.keys()
        empresas = []
        for database_conexion in bases_de_datos:
            try:
                database_conexion = '%s' % database_conexion
            except UnicodeDecodeError:
                pass
            else:
                conexion_split = database_conexion.split('-')
                conexion_id = conexion_split[0]
                empresa = ('-').join(conexion_split[1:])
                conexion = ConexionDB.objects.get(pk=int(conexion_id))
                database_conexion_name = '%02d-%s' % (conexion.id, empresa)
                empresa_option = [database_conexion, database_conexion_name]
                empresas.append(empresa_option)

        super(SingleConexionForm, self).__init__(*args, **kwargs)
        self.fields['empresas'] = forms.ChoiceField(choices=empresas)


class LineaForm(forms.Form):
    linea = forms.ModelChoiceField(LineaArticulos.objects.all().order_by('nombre'), required=False)
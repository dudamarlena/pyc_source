# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\django-microsip-api\microsip_api\apps\config\forms.py
# Compiled at: 2020-04-07 19:51:08
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import fdb, os
from .models import *
from microsip_api.comun.sic_db import first_or_none
from microsip_api.models_base.models import ConexionDB
from django.conf import settings
RUTA_API = os.path.dirname(os.path.realpath(__file__)).strip('config').strip('apps\\')

class ConexionManageForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = ConexionDB


class CustomAuthenticationForm(forms.Form):
    conexion_db = forms.ModelChoiceField(ConexionDB.objects.all(), required=False)
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario de microsip'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    conexion_db.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = self.cleaned_data
        conexion_db = cleaned_data.get('conexion_db')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if conexion_db == None and username != 'SYSDBA':
            raise forms.ValidationError('Por favor selecciona una conexion')
        else:
            try:
                if settings.MICROSIP_VERSION >= 2019:
                    db = fdb.connect(host='localhost', user=username, password=str(password), database='%s\\data\\LOGIN.FDB' % RUTA_API)
                else:
                    db = fdb.connect(host='localhost', user=username, password=str(password), database='%s\\data\\LOGIN25.FDB' % RUTA_API)
            except fdb.DatabaseError:
                raise forms.ValidationError('nombre de usuario o password invalidos')

            if conexion_db:
                try:
                    db = fdb.connect(host=conexion_db.servidor, user=conexion_db.usuario, password=conexion_db.password, database='%s\\System\\CONFIG.FDB' % conexion_db.carpeta_datos)
                except fdb.DatabaseError:
                    raise forms.ValidationError('Error en la conexion selecionada')

            try:
                usuario = User.objects.get(username__exact=username)
            except ObjectDoesNotExist:
                usuario = User.objects.create_user(username=username, password=str(password))
                if username == 'SYSDBA':
                    User.objects.filter(username='SYSDBA').update(is_superuser=True, is_staff=True)
            else:
                usuario.set_password(str(password))
                usuario.save()

        return cleaned_data


class SelectDBForm(forms.Form):

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')
        conexion_activa = kwargs.pop('conexion_activa')
        empresas = []
        if conexion_activa != '':
            conexion_activa = ConexionDB.objects.get(pk=conexion_activa)
        else:
            conexion_activa = None
        if conexion_activa:
            acceso_empresas = ''
            try:
                acceso_empresas = Usuario.objects.get(nombre__exact=usuario.username).acceso_empresas
            except ObjectDoesNotExist:
                if usuario.username == 'SYSDBA':
                    acceso_empresas = 'T'

            consulta = ''
            if acceso_empresas == 'T':
                consulta = 'SELECT EMPRESAS.nombre_corto FROM EMPRESAS order by nombre_corto'
            else:
                if acceso_empresas == 'L':
                    consulta = "SELECT EMPRESAS.nombre_corto FROM EMPRESAS_USUARIOS, EMPRESAS, USUARIOS WHERE USUARIOS.usuario_id = empresas_usuarios.usuario_id AND EMPRESAS.empresa_id = empresas_usuarios.empresa_id AND usuarios.nombre = '%s' order by nombre_corto" % usuario
                db = fdb.connect(host=conexion_activa.servidor, user=conexion_activa.usuario, password=conexion_activa.password, database='%s\\System\\CONFIG.FDB' % conexion_activa.carpeta_datos)
                cur = db.cursor()
                cur.execute(consulta)
                empresas_rows = cur.fetchall()
                for empresa in empresas_rows:
                    try:
                        empresa = '%s' % empresa[0]
                    except UnicodeDecodeError:
                        pass
                    else:
                        empresa_option = [
                         empresa, empresa]
                        empresas.append(empresa_option)

        super(SelectDBForm, self).__init__(*args, **kwargs)
        self.fields['conexion'] = forms.ChoiceField(choices=empresas)
        return
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Developer.pe\proyectos\base_django\aplicaciones\usuarios\admin.py
# Compiled at: 2019-07-11 02:06:27
# Size of source mod 2**32: 3381 bytes
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Usuario

class FormularioCreacionUsuario(forms.ModelForm):
    __doc__ = 'A form for creating new users. Includes all the required\n    fields, plus a repeated password.'
    password1 = forms.CharField(label='Contraseña', widget=(forms.PasswordInput))
    password2 = forms.CharField(label='Contraseña de Confirmación', widget=(forms.PasswordInput))

    class Meta:
        model = Usuario
        fields = ('email', 'nombres', 'apellidos')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1:
            if password2:
                if password1 != password2:
                    raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class FormularioEdicionUsuario(forms.ModelForm):
    __doc__ = "A form for updating users. Includes all the fields on\n    the user, but replaces the password field with admin's\n    password hash display field.\n    "
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'nombres', 'apellidos', 'usuario_activo', 'usuario_administrador')

    def clean_password(self):
        return self.initial['password']


class UsuarioAdmin(BaseUserAdmin):
    form = FormularioEdicionUsuario
    add_form = FormularioCreacionUsuario
    list_display = ('username', 'email', 'nombres', 'apellidos', 'usuario_activo',
                    'usuario_administrador')
    list_filter = ('usuario_administrador', )
    fieldsets = (
     (
      None, {'fields': ('email', 'password')}),
     (
      'Información Personal', {'fields': ('nombres', 'apellidos')}),
     (
      'Permisos', {'fields': ('usuario_administrador', 'usuario_activo')}))
    add_fieldsets = (
     (
      None,
      {'classes':('wide', ), 
       'fields':('email', 'nombres', 'apellidos', 'password1', 'password2')}),)
    search_fields = ('email', )
    ordering = ('email', )
    filter_horizontal = ()


admin.site.register(Usuario, UsuarioAdmin)
admin.site.unregister(Group)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_mail\djmicrosip_mail\modulos\saldos_clientes\forms.py
# Compiled at: 2019-12-02 13:48:11
from django import forms
from .models import *
from django.core.validators import RegexValidator
import autocomplete_light
from django.conf import settings

class SelectMultipleClients(forms.Form):
    clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.all(), widget=autocomplete_light.MultipleChoiceWidget('ClienteManyAutocomplete'))
    mensaje = forms.CharField(max_length=160, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje aqui (160 Caracteres)...', 'cols': 35, 'rows': 5, 'maxlength': 160}))


if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
    from djmicrosip_tareas.models import ProgrammedTask

    class ProgrammedTaskForm(forms.ModelForm):
        period_start_datetime = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha inicio periodo...'}))
        period_end_datetime = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}), required=False)
        period_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unidades...'}))
        next_execution = forms.CharField(widget=forms.HiddenInput(), required=False)

        class Meta:
            model = ProgrammedTask
            exclude = ('description', 'command_type', 'command', 'status', 'last_execution')
            widgets = {'period_unit': forms.Select(attrs={'class': 'form-control'})}
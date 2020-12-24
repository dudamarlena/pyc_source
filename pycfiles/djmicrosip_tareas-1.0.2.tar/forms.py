# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\djmicrosip_apps\djmicrosip_tareas\djmicrosip_tareas\forms.py
# Compiled at: 2020-01-17 20:06:16
from django import forms
from .models import ProgrammedTask

class ProgrammedTaskForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion de la tarea...'}))
    command = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comando a ejecutar...'}))
    period_start_datetime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha inicio periodo...'}))
    period_end_datetime = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha fin periodo...'}), required=False)
    period_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unidades...'}))
    next_execution = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ProgrammedTask
        exclude = ('status', 'last_execution')
        widgets = {'command_type': forms.Select(attrs={'class': 'form-control'}), 
           'period_unit': forms.Select(attrs={'class': 'form-control'})}
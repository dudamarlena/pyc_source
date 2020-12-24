# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_reorden\djmicrosip_reorden\forms.py
# Compiled at: 2015-10-19 16:12:47
from django import forms
from .models import *
from django.conf import settings
if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
    from djmicrosip_tareas.models import ProgrammedTask

    class ProgrammedTaskForm(forms.ModelForm):
        period_start_datetime = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha inicio periodo...'}))
        period_end_datetime = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}), required=False)
        period_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unidades...'}))
        ESTATUS_ARTICULOS = (('P', 'POR PEDIR'), ('C', 'CRITICO'))
        estatus = forms.ChoiceField(widget=forms.Select, choices=ESTATUS_ARTICULOS)
        almacenes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Almacen.objects.all())
        NIVEL_RESURTIR = (('M', 'MAXIMO'), ('R', 'REORDEN'))
        nivel = forms.ChoiceField(widget=forms.Select, choices=NIVEL_RESURTIR)
        next_execution = forms.CharField(widget=forms.HiddenInput(), required=False)

        class Meta:
            model = ProgrammedTask
            exclude = ('description', 'command_type', 'command', 'status', 'last_execution')
            widgets = {'period_unit': forms.Select(attrs={'class': 'form-control'})}

        def save(self, *args, **kwargs):
            nivel = self.cleaned_data['nivel']
            nivel_obj = Registry.objects.get(nombre='SIC_REORDEN_nivel')
            nivel_obj.valor = nivel
            nivel_obj.save()
            almacenes = self.cleaned_data['almacenes']
            almacenes_ids = almacenes.values_list('ALMACEN_ID', flat=True)
            almacenes_obj = Registry.objects.get(nombre='SIC_REORDEN_almacenes_id')
            almacenes_obj.valor = (',').join(map(str, almacenes_ids))
            almacenes_obj.save()
            estatus = self.cleaned_data['estatus']
            estatus_obj = Registry.objects.get(nombre='SIC_REORDEN_estatus')
            estatus_obj.valor = estatus
            estatus_obj.save()
            return super(ProgrammedTaskForm, self).save(*args, **kwargs)


class GeneraOrdenForm(forms.Form):
    almacen = forms.ModelChoiceField(widget=forms.Select, queryset=Almacen.objects.all(), required=True)
    ESTATUS_ARTICULOS = (('P', 'POR PEDIR'), ('C', 'CRITICO'))
    estatus = forms.ChoiceField(widget=forms.Select, choices=ESTATUS_ARTICULOS)
    NIVEL_RESURTIR = (('M', 'MAXIMO'), ('R', 'REORDEN'))
    nivel = forms.ChoiceField(widget=forms.Select, choices=NIVEL_RESURTIR)


class ProgrammedTaskInForm(forms.ModelForm):
    period_start_datetime = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha inicio periodo...'}))
    period_end_datetime = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}), required=False)
    period_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unidades...'}))
    next_execution = forms.CharField(widget=forms.HiddenInput(), required=False)

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

        super(ProgrammedTaskInForm, self).__init__(*args, **kwargs)
        self.fields['empresas'] = forms.ChoiceField(choices=empresas)

    def save(self, *args, **kwargs):
        empresa = self.cleaned_data['empresas']
        empresa_obj = Registry.objects.get(nombre='SIC_REORDEN_empresa')
        empresa_obj.valor = empresa
        empresa_obj.save()
        return super(ProgrammedTaskInForm, self).save(*args, **kwargs)

    class Meta:
        model = ProgrammedTask
        exclude = ('description', 'command_type', 'command', 'status', 'last_execution')
        widgets = {'period_unit': forms.Select(attrs={'class': 'form-control'})}


class ProgrammedTaskOutForm(forms.ModelForm):
    period_start_datetime = forms.CharField(label='Inicio', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fecha inicio periodo...'}))
    period_end_datetime = forms.CharField(label='Fin', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '...'}), required=False)
    period_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'unidades...'}))
    next_execution = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ProgrammedTask
        exclude = ('description', 'command_type', 'command', 'status', 'last_execution')
        widgets = {'period_unit': forms.Select(attrs={'class': 'form-control'})}
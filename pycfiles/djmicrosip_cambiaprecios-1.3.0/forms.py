# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_cambiaprecios\djmicrosip_cambiaprecios\modulos\herramientas\forms.py
# Compiled at: 2017-05-03 15:46:28
from django import forms
from .models import *

def UpdateRegistry(registry_name, value):
    registry = Registry.objects.get(nombre=registry_name)
    registry.valor = value
    registry.save()


class PreferenciasManageForm(forms.Form):
    actualizar_costos = forms.BooleanField(required=False)

    def save(self, *args, **kwargs):
        actualizar_costos_value = 0
        if self.cleaned_data['actualizar_costos']:
            actualizar_costos_value = 1
        UpdateRegistry('SIC_CambiaPrecio_ActualizarCostos', actualizar_costos_value)
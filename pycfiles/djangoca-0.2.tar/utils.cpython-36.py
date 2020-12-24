# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Developer.pe\proyectos\base_django\aplicaciones\base\utils.py
# Compiled at: 2019-07-29 02:27:40
# Size of source mod 2**32: 776 bytes
from django.apps import apps
from aplicaciones.usuarios.models import Usuario

def obtener_consulta(modelo):
    return modelo.objects.all().values()


def obtener_nombres_atributos_modelos(modelo):
    nombres_campos_modelos = [nombre for nombre, _ in models.fields_for_model(modelo).items()]
    return nombres_campos_modelos


def obtener_modelo(_app_name, _model_name):
    return apps.get_model(app_label=_app_name, model_name=_model_name)


def obtener_valor_de_atributos_de_modelo(modelo):
    usuarios = modelo.objects.all().values()
    return [valor for valor in usuarios]


def convertir_booleanos(data):
    for dat in data:
        if data[dat] == 'true':
            data[dat] = True
        if data[dat] == 'false':
            data[dat] = False

    return data
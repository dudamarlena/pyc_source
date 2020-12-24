# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/aplicaciones/base/utils.py
# Compiled at: 2019-08-01 02:10:13
# Size of source mod 2**32: 1669 bytes
import django.apps as apps
from aplicaciones.usuarios.models import Usuario

def obtener_consulta(modelo):
    """ OBTENER CONSULTA DE UN MODELO.

    Retorna todos los objetos junto con todos sus valores del modelo
    enviado como parámetro.

    """
    return modelo.objects.all().values()


def obtener_nombres_atributos_modelos(modelo):
    """ OBTENER ATRIBUTOS DE UN MODELO.

    Retorna todos los atributos de un modelo enviado por parámetro.

    """
    nombres_campos_modelos = [nombre for nombre, _ in models.fields_for_model(modelo).items()]
    return nombres_campos_modelos


def obtener_modelo(_app_name, _model_name):
    """ OBTENER MODEL.

    Retorna el modelo en cuestión que pertenece a las etiquetas enviadas por parámetros.

    Parámetros:
    -- _app_name                : Nombre de aplicación donde se encuentra el modelo.
    -- _model_name              : Cadena de texto con el nombre de modelo a buscar.

    """
    return apps.get_model(app_label=_app_name, model_name=_model_name)


def obtener_valor_de_atributos_de_modelo(modelo):
    """ OBTENER VALORES PERTENECIENTES A ATRIBUTOS DE UN MODELO.

    Retorna todos los valores que le pertenecen a un modelo en cuestión.

    """
    usuarios = modelo.objects.all().values()
    return [valor for valor in usuarios]


def convertir_booleanos(data):
    """ VALIDACIÓN DE CAMPOS BOOLEANOS ENVIADOS VÍA AJAX.

    Retorna todos los valores enviados vía AJAX convirtiendo a Booleanos los que correspondan.

    """
    for dat in data:
        if data[dat] == 'true':
            data[dat] = True
        if data[dat] == 'false':
            data[dat] = False

    return data
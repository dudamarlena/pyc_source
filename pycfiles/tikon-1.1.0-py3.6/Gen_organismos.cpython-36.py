# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\RAE\Gen_organismos.py
# Compiled at: 2017-03-28 15:33:12
# Size of source mod 2**32: 1419 bytes
import os.path
from tikon import RAE

def generar_org(archivo):
    """
    Esta función devuelve una instancia de Organismo, con la subclase apropiada para la extensión del archivo
    especificado.
    Notar que NO podrá encontrar subclases de Organismo que no se importan en el código __init__ de RAE.

    :param archivo: El archivo fuente.
    :type archivo: str

    :return: La instancia apropiada.
    :rtype: RAE.Organismo.Organismo
    """

    def sacar_subclases(cls):
        return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in sacar_subclases(s)]

    proyecto, nombre_con_ext = os.path.split(archivo)
    nombre, ext = os.path.splitext(nombre_con_ext)
    for sub in sacar_subclases(RAE.Organismo.Organismo):
        if sub.ext == ext:
            obj_org = sub(nombre=nombre, proyecto=proyecto)
            obj_org.cargar(fuente=archivo)

    raise ValueError('No se encontró subclase de Organismo con extensión %s.' % ext)
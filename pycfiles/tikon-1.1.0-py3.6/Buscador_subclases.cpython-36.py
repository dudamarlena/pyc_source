# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Buscador_subclases.py
# Compiled at: 2017-01-05 16:18:40
# Size of source mod 2**32: 878 bytes
from tikon.Coso import Coso

def encontrar_subclase_coso(ext):
    """
    Esta función devuelve la clase de objeto asociada con la extensión especificada.

    :param ext: La extensión de interés.
    :type ext: str

    :return: El objeto de la subclase de Coso asociado con la extensión.
    :rtype: Coso
    """

    def sacar_subclases(cls):
        return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in sacar_subclases(s)]

    for sub in sacar_subclases(Coso):
        if sub.ext == ext:
            return sub

    raise ValueError('No se encontró subclase de Coso con extensión %s.' % ext)
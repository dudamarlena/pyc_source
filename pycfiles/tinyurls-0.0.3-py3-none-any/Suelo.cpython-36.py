# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Cultivo\Suelo.py
# Compiled at: 2017-01-26 11:00:46
# Size of source mod 2**32: 990 bytes
from tikon.Coso import Coso
from tikon.Matemáticas import Ecuaciones as Ec

class Suelo(Coso):
    ext = '.suel'
    dic_ecs = Ec.ecs_suelo

    def __init__(símismo, nombre, proyecto=None):
        super().__init__(nombre=nombre, proyecto=proyecto)
        símismo.receta['coefs'] = Ec.gen_ec_inic(Ec.ecs_suelo)
        Textura_suelo = ''
        Color = ''

    def _sacar_líms_coefs_interno(símismo):
        """
        Ver la documentación de Coso.

        :rtype: list

        """
        return [símismo.dic_ecs[x]['límites'] for x in símismo.receta['coefs']]

    def _sacar_coefs_interno(símismo):
        """
        Ver la documentación de Coso.

        :rtype: list

        """
        return list(símismo.receta['coefs'].values())
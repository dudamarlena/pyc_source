# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\RAE\Enfermedad.py
# Compiled at: 2017-08-25 13:07:47
# Size of source mod 2**32: 2832 bytes
from tikon.RAE.Organismo import Organismo

class Enfermedad(Organismo):
    ext = '.enf'

    def __init__(símismo, nombre, proyecto=None):
        """

        :param nombre:
        :type nombre: str

        :param proyecto:
        :type proyecto: str
        """
        super().__init__(nombre=nombre, proyecto=proyecto)

    def infecta(símismo, etp_símismo, etp_huésped, huésped):
        """

        :param etp_símismo:
        :type etp_símismo: list | str

        :param etp_huésped:
        :type etp_huésped: list | str

        :param huésped:
        :type huésped: Organismo

        """
        símismo.victimiza(huésped, etps_símismo=etp_símismo, etps_víctima=etp_huésped, método='huésped')


class EnfermedadHoja(Enfermedad):

    def __init__(símismo, nombre, proyecto, huéspedes):
        super().__init__(nombre=nombre, proyecto=proyecto)
        ecs_esp = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
          Muertes={'Ecuación': 'Nada'},
          Edad={'Ecuación': 'Nada'},
          Transiciones={'Prob':'Nada', 
         'Mult':'Nada'},
          Reproducción={'Prob': 'Nada'},
          Movimiento={})
        ecs_inf = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
          Muertes={'Ecuación': 'Nada'},
          Edad={'Ecuación': 'Nada'},
          Transiciones={'Prob':'Nada', 
         'Mult':'Nada'},
          Reproducción={'Prob': 'Nada'},
          Movimiento={})
        for huésped in huéspedes:
            planta = huésped.nombre
            símismo.añadir_etapa(nombre=('%s_espórulo' % planta), posición=(len(símismo.etapas)), ecuaciones=ecs_esp)
            símismo.añadir_etapa(nombre=('%s_infección' % planta), posición=(len(símismo.etapas)), ecuaciones=ecs_inf)
            símismo.infecta(etp_símismo=('%s_infección' % planta), etp_huésped='hoja', huésped=huésped)


class DosHuéspedes(EnfermedadHoja):

    def __init__(símismo, nombre, huésped_1, huésped_2, proyecto):
        super().__init__(nombre=nombre, proyecto=proyecto, huéspedes=[huésped_1, huésped_2])
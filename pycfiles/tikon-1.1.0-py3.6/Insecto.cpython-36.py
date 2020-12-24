# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\RAE\Insecto.py
# Compiled at: 2017-08-25 13:07:47
# Size of source mod 2**32: 17618 bytes
from tikon.RAE.Organismo import Organismo

class Insecto(Organismo):
    __doc__ = '\n    Esta clase representa insectos. En general no se llama directamente, sino a través de una de sus subclasses (ver\n    abajo).\n    '
    ext = '.ins'

    def __init__(símismo, nombre, proyecto, huevo=False, njuvenil=0, pupa=False, adulto=True, tipo_ecuaciones=None):
        """
        La funciôn de inicializaciôn crea un objeto Organismo y después crea las etapas apropiadas.

        :param nombre: El nombre del insecto
        :type nombre: str
        
        :param proyecto: El proyecto al cual pertenece este Insecto.
        :type proyecto: str

        :param huevo: Si incluimos la etapa del huevo en el modelo o no.
        :type huevo: bool

        :param njuvenil: Cuantas fases juveniles incluimos en el modelo (puede ser 0).
        :type njuvenil: int

        :param pupa: Si incluimos la etapa de la pupa en el modelo o no.
        :type pupa: bool

        :param adulto: Si incluimos la etapa del adulto en el modelo o no.
        :type adulto: bool

        :param tipo_ecuaciones: Un diccionario con los tipos de ecuaciones para cada etapa. (Siempre se puede cambiar
          más tarde con la función usar_ecuación()).
          Tiene el formato: {Etapa_1: {Categoría_1: {subcategoría_1: tipo_de_ecuacion, ...}, Categoría_2: {...} },
           Etapa_2: {Categoría_1: {subcategoría...}, ...}, ...}
        :type tipo_ecuaciones: dict

        """
        super().__init__(nombre=nombre, proyecto=proyecto)
        pos = 0
        if huevo:
            símismo.añadir_etapa('huevo', posición=pos, ecuaciones=(tipo_ecuaciones['huevo']))
            pos += 1
        if njuvenil < 0:
            raise ValueError('El número de juveniles no puede ser inferior a 0.')
        for i in range(0, njuvenil):
            if njuvenil == 1:
                nombre = 'juvenil'
            else:
                nombre = 'juvenil_%i' % (i + 1)
            símismo.añadir_etapa(nombre, posición=pos, ecuaciones=(tipo_ecuaciones['juvenil']))
            pos += 1

        if pupa:
            símismo.añadir_etapa('pupa', posición=pos, ecuaciones=(tipo_ecuaciones['pupa']))
            pos += 1
        if adulto:
            símismo.añadir_etapa('adulto', posición=pos, ecuaciones=(tipo_ecuaciones['adulto']))

    def secome(símismo, presa, etps_presa=None, etps_depred=None):
        """
        Estabelce relaciones de depredador y presa.

        :param presa:
        :type presa: tikon.RAE.Organismo.Organismo

        :param etps_presa:
        :type etps_presa: str 1 list

        :param etps_depred:
        :type etps_depred: str | list

        """
        símismo.victimiza(víctima=presa, etps_símismo=etps_depred, etps_víctima=etps_presa, método='presa')

    def nosecome(símismo, presa, etps_presa=None, etps_depred=None):
        """
        Para quitar una relación de depredador y presa.

        :param presa:
        :type presa: tikon.RAE.Organismo.Organismo

        :param etps_presa:
        :type etps_presa:

        :param etps_depred:
        :type etps_depred:

        """
        símismo.novictimiza(víctima=presa, etps_símismo=etps_depred, etps_víctima=etps_presa, método='presa')


class Sencillo(Insecto):
    __doc__ = '\n    Esta clase representa insectos con ciclos de vida sencillos (para cuales sólo se incluye la etapa adulta en el\n    modelo).\n    '

    def __init__(símismo, nombre, proyecto):
        tipo_ec = dict(Crecimiento={'Modif':'Ninguna',  'Ecuación':'Logístico Presa'}, Depredación={'Ecuación': 'Kovai'},
          Muertes={'Ecuación': 'Nada'},
          Edad={'Ecuación': 'Nada'},
          Transiciones={'Prob':'Nada', 
         'Mult':'Nada'},
          Reproducción={'Prob': 'Nada'},
          Movimiento={})
        super().__init__(nombre=nombre, huevo=False, njuvenil=0, pupa=False, adulto=True, tipo_ecuaciones=dict(adulto=tipo_ec),
          proyecto=proyecto)


class MetamCompleta(Insecto):
    __doc__ = '\n    Esta clase representa insectos que tienen una metamórfosis completa. No necesita extensión propia, visto que\n    no tiene métodos o atributos distintos a los de Insecto.\n    '

    def __init__(símismo, nombre, proyecto, huevo=True, njuvenil=1, adulto=True):
        """
        Inicializamos el Insecto de metamórfosis completa con las ecuaciones apropiadas.

        :param nombre: El nombre del insecto
        :type nombre: str

        :param huevo: Si incluimos la etapa del huevo en el modelo o no.
        :type huevo: bool

        :param njuvenil: Cuantas fases juveniles incluimos en el modelo.
        :type njuvenil: int

        :param adulto: Si incluimos la etapa del adulto en el modelo o no.
        :type adulto: bool

        """
        tipo_ec = {}
        if huevo:
            tipo_ec['huevo'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Nada'},
              Muertes={'Ecuación': 'Constante'},
              Edad={'Ecuación': 'Días'},
              Transiciones={'Prob':'Normal', 
             'Mult':'Nada'},
              Reproducción={'Prob': 'Nada'},
              Movimiento={})
        else:
            tipo_ec['juvenil'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
              Muertes={'Ecuación': 'Constante'},
              Edad={'Ecuación': 'Días'},
              Transiciones={'Prob':'Normal', 
             'Mult':'Nada'},
              Reproducción={'Prob': 'Nada'},
              Movimiento={})
            tipo_ec['pupa'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Nada'},
              Muertes={'Ecuación': 'Constante'},
              Edad={'Ecuación': 'Días'},
              Transiciones={'Prob':'Normal', 
             'Mult':'Nada'},
              Reproducción={'Prob': 'Nada'},
              Movimiento={})
            if adulto:
                tipo_ec['adulto'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
                  Muertes={'Ecuación': 'Nada'},
                  Edad={'Ecuación': 'Días'},
                  Transiciones={'Prob':'Normal', 
                 'Mult':'Nada'},
                  Reproducción={'Prob': 'Normal'},
                  Movimiento={})
            else:
                tipo_ec['pupa']['Reproducción']['Prob'] = 'Constante'
        super().__init__(nombre=nombre, huevo=huevo, njuvenil=njuvenil, pupa=True, adulto=adulto, tipo_ecuaciones=tipo_ec,
          proyecto=proyecto)


class MetamIncompleta(Insecto):
    __doc__ = '\n    Esta clase representa insectos que tienen una metamórfosis incompleta. No necesita extensión propia, visto que\n    no tiene métodos o atributos distintos a los de Insecto.\n    '

    def __init__(símismo, nombre, proyecto, huevo=True, njuvenil=1, adulto=True):
        """
        Inicializamos el Insecto de metamórfosis incompleta con las ecuaciones apropiadas.

        :param nombre: El nombre del insecto
        :type nombre: str

        :param proyecto: El proyecto al cual pertenece este Insecto.
        :type proyecto: str
        
        :param huevo: Si incluimos la etapa del huevo en el modelo o no.
        :type huevo: bool

        :param njuvenil: Cuantas etapas juveniles incluimos en el modelo.
        :type njuvenil: int

        :param adulto: Si incluimos la etapa del adulto en el modelo o no.
        :type adulto: bool

        """
        tipo_ec = {}
        if huevo:
            tipo_ec['huevo'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Nada'},
              Muertes={'Ecuación': 'Constante'},
              Edad={'Ecuación': 'Días'},
              Transiciones={'Prob':'Normal', 
             'Mult':'Nada'},
              Reproducción={'Prob': 'Nada'},
              Movimiento={})
        else:
            tipo_ec['juvenil'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
              Muertes={'Ecuación': 'Constante'},
              Edad={'Ecuación': 'Días'},
              Transiciones={'Prob':'Normal', 
             'Mult':'Nada'},
              Reproducción={'Prob': 'Nada'},
              Movimiento={})
            if adulto:
                tipo_ec['adulto'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
                  Muertes={'Ecuación': 'Nada'},
                  Edad={'Ecuación': 'Días'},
                  Transiciones={'Prob':'Normal', 
                 'Mult':'Nada'},
                  Reproducción={'Prob': 'Normal'},
                  Movimiento={})
            else:
                tipo_ec['juvenil']['Reproducción']['Prob'] = 'Constante'
        super().__init__(nombre=nombre, huevo=huevo, njuvenil=njuvenil, pupa=False, adulto=adulto, tipo_ecuaciones=tipo_ec,
          proyecto=proyecto)


class Parasitoide(Insecto):
    __doc__ = '\n    Parasitoides son una clase muy especial de insecto, porque sus larvas crecen adentro de los cuerpos de otros\n    organismos. Después de mucho dolor de cabeza, decidimos (decidí) implementarlos así.\n    '
    ext = '.prs'

    def __init__(símismo, nombre, proyecto, pupa=False):
        """

        :param nombre: El nombre del Parasitoide
        :type nombre: str
        
        :param proyecto: El proyecto al cual pertenece este Insecto.
        :type proyecto: str

        :param pupa: Si hay que modelizar la etapa de pupa del Parasitoide
        :type pupa: bool

        """
        tipo_ec = {}
        if pupa:
            tipo_ec['pupa'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Nada'},
              Muertes={'Ecuación': 'Constante'},
              Edad={'Ecuación': 'Días'},
              Transiciones={'Prob':'Normal', 
             'Mult':'Nada'},
              Reproducción={'Prob': 'Nada'},
              Movimiento={})
        tipo_ec['juvenil'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Nada'},
          Muertes={'Ecuación': 'Nada'},
          Edad={'Ecuación': 'Días'},
          Transiciones={'Prob':'Normal', 
         'Mult':'Linear'},
          Reproducción={'Prob': 'Nada'},
          Movimiento={})
        tipo_ec['adulto'] = dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
          Muertes={'Ecuación': 'Nada'},
          Edad={'Ecuación': 'Días'},
          Transiciones={'Prob':'Normal', 
         'Mult':'Nada'},
          Reproducción={'Prob': 'Nada'},
          Movimiento={})
        super().__init__(nombre=nombre, proyecto=proyecto, huevo=False, njuvenil=1, pupa=pupa, adulto=True, tipo_ecuaciones=tipo_ec)

    def parasita(símismo, víctima, etps_infec, etp_sale):
        """

        :param víctima: El objeto del otro insecto que este parasitoide puede parasitar.
        :type víctima: tikon.RAE.Insecto.Insecto

        :param etps_infec:  Las etapas del otro insecto que este parasitoide puede infectar.
        :type etps_infec: list | str

        :param etp_sale:  La etapa de la víctima de la cual el parásito adulto (o pupa) saldrá.
        :type etp_sale: str

        """
        símismo.victimiza(víctima=víctima, etps_símismo='adulto', etps_víctima=etps_infec, etp_sale=etp_sale, método='huésped')

    def noparasita(símismo, víctima, etps_infec=None):
        """
        Esta función borra la relación de parasitoide-huésped entre dos insectos.

        :param víctima: El objeto representando el otro insecto que ahora ya no hay que parasitar.
        :type víctima: tikon.RAE.Insecto.Insecto

        :param etps_infec: La lista de etapas de la víctima que no se pueden infectar por este parasitoide. Un valor
          de 'None' borrará la relación de parasitismo con todas las etapas víctimas del huésped.
        :type etps_infec: list | str

        """
        símismo.novictimiza(víctima=víctima, etps_símismo='adulto', etps_víctima=etps_infec, método='huésped')


class Esfécido(Insecto):
    __doc__ = '\n    Los esfécidos son una familia de avispas que ponen sus huevos en los cuerpos (vivos) de sus presas. Al contrario\n    de parasitoides típicos, estos paralizan y quitan su presa de la planta. Por lo mismo, se debe considerar\n    su papel ecológico de manera distinta. (Se considera como depredación con reproducción basada en el éxito\n    de la depredación).\n    '
    ext = '.esf'

    def __init__(símismo, nombre, proyecto):
        tipo_ec = {'adulto':dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
           Muertes={'Ecuación': 'Nada'},
           Edad={'Ecuación': 'Días'},
           Transiciones={'Prob':'Normal', 
          'Mult':'Nada'},
           Reproducción={'Prob': 'Depredación'},
           Movimiento={}), 
         'juvenil':dict(Crecimiento={'Modif':'Nada',  'Ecuación':'Nada'}, Depredación={'Ecuación': 'Kovai'},
           Muertes={'Ecuación': 'Nada'},
           Edad={'Ecuación': 'Días'},
           Transiciones={'Prob':'Normal', 
          'Mult':'Nada'},
           Reproducción={'Prob': 'Nsda'},
           Movimiento={})}
        super().__init__(nombre=nombre, proyecto=proyecto, huevo=False, njuvenil=1, pupa=False, adulto=True, tipo_ecuaciones=tipo_ec)

    def captura(símismo, víctima, etps_víc):
        """

        :param víctima: El objeto del otro insecto que este parasitoide puede parasitar.
        :type víctima: tikon.RAE.Insecto.Insecto

        :param etps_víc: Las etapas de la víctima en las cuales el esfécido oviposita.
        :type etps_víc: list | str

        """
        símismo.victimiza(víctima=víctima, etps_símismo='adulto', etps_víctima=etps_víc, método='presa')

    def nocaptura(símismo, víctima, etps_víc=None):
        """

        :param víctima: El objeto del otro insecto que este parasitoide ya no puede parasitar.
        :type víctima: tikon.RAE.Insecto.Insecto

        :param etps_víc: Las etapas de la víctima en las cuales el esfécido ya no oviposita.
        :type etps_víc: list | str
        """
        símismo.novictimiza(víctima=víctima, etps_símismo='adulto', etps_víctima=etps_víc, método='presa')
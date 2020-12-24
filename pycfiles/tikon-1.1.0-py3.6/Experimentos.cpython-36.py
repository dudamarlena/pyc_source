# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Experimentos.py
# Compiled at: 2017-01-05 16:18:44
# Size of source mod 2**32: 12534 bytes
import csv, datetime as ft, os, numpy as np
from tikon.Controles import directorio_base

class Experimento(object):

    def __init__(símismo, nombre, proyecto=None):
        """

        :param nombre:
        :type nombre: str

        :param proyecto:
        :type proyecto: str
        """
        símismo.nombre = nombre
        símismo.fecha_ref = None
        símismo.datos = {'Organismos':{'tiempo':None, 
          'obs':{},  'parcelas':[]}, 
         'Cultivos':{'tiempo': None}, 
         'Aplicaciones':{'tiempo': None}, 
         'Parcelas':{}}
        símismo.proyecto = proyecto

    def agregar_orgs(símismo, archivo, col_tiempo, factor=1, col_parcela=None, fecha_ref=None):
        """
        Esta función establece la base de datos para las observaciones de organismos en el campo.

        :param archivo: La ubicación del archivo para leer
        :type archivo: str

        :param col_tiempo: El nombre de la columna que especifica el tiempo de las observaciones.
        :type col_tiempo: str

        :param factor: El factor con el cual multiplicar las observaciones de poblaciones (útil para compatibilidad
          de unidades).
        :type factor: float

        :param col_parcela: Una columna, si existe, que referencia la parcela.
        :type col_parcela: str

        :param fecha_ref: Un parámetro opcional para especificar la fecha de referencia (la fecha para cual tiempo = 0
          en la columna 'col_tiempo').
        :type fecha_ref: ft.date

        """
        símismo.datos['Organismos']['tiempo'] = None
        símismo.datos['Organismos']['obs'].clear()
        símismo.datos['Organismos']['parcelas'].clear()
        archivo = símismo.prep_archivo(archivo)
        dic_datos = símismo.leer_datos(archivo)
        if col_tiempo not in dic_datos:
            raise ValueError('No se encontró la columna de tiempo en la base de datos.')
        fecha_inic_datos, vec_tiempos, vec_tiempos_únic = símismo.leer_fechas(dic_datos[col_tiempo])
        símismo.datos['Organismos']['tiempo'] = vec_tiempos_únic
        if fecha_ref is not None:
            fecha_inic_datos = fecha_ref
        if fecha_inic_datos is not None:
            if símismo.fecha_ref is None:
                símismo.fecha_ref = fecha_inic_datos
            else:
                dif = (fecha_inic_datos - símismo.fecha_ref).days
                if dif < 0:
                    símismo.fecha_ref = fecha_inic_datos
                    símismo.mover_fechas(dif=dif, no_cambiar='Organismos')
                else:
                    símismo.datos['Organismos']['tiempo'] += dif
        for col in dic_datos:
            if col != col_tiempo and col != col_parcela:
                if col_parcela is None:
                    matr = símismo.texto_a_datos(dic_datos[col])[np.newaxis, :]
                    símismo.datos['Organismos']['parcelas'] = ['1']
                else:
                    parcelas = list(set(dic_datos[col_parcela]))
                    parcelas.sort()
                    símismo.datos['Organismos']['parcelas'] = parcelas
                    vec_parc = dic_datos[col_parcela]
                    matr = np.empty((len(parcelas), len(vec_tiempos_únic)))
                    matr.fill(np.nan)
                    for n, p in enumerate(parcelas):
                        vec_datos = dic_datos[col][np.where(vec_parc == p)]
                        tiempos_parc = dic_datos[col][np.where(vec_parc == p)]
                        matr[(n, tiempos_parc)] = vec_datos

                np.multiply(matr, factor, out=matr)
                símismo.datos['Organismos']['obs'][col] = matr.round()

    def agregar_cultivos(símismo, archivo):
        pass

    def agregar_aplicaciones(símismo, archivo):
        pass

    def agregar_parcelas(símismo, archivo):
        pass

    def mover_fechas(símismo, dif, no_cambiar):
        for bd in símismo.datos:
            if bd != no_cambiar:
                símismo.datos[bd]['tiempo'] += dif

    def prep_archivo(símismo, archivo):
        if os.path.splitdrive(archivo)[0] == '':
            archivo = os.path.join(directorio_base, 'Proyectos', símismo.proyecto, archivo)
        return archivo

    @staticmethod
    def leer_datos(archivo):
        """
        Esta función lee una base de datos y devuelve un diccionario con el formato:
          {nombre_columna1: [lista de datos],
           nombre_columna2: [lista de datos],
           ...
           }

           Los datos de presentan todos en formato texto.

        :param archivo: La dirección del archivo para leer.
        :type archivo: str

        :return: Un diccionario de los datos.
        :rtype: dict

        """
        datos = {}
        tipo = os.path.splitext(archivo)[1]
        if tipo == '.csv':
            with open(archivo, newline='') as (d):
                l = csv.reader(d)
                valores = []
                cols = next(l)
                for f in l:
                    valores.append(f)

            for n, col in enumerate(cols):
                datos[col] = [x[n] for x in valores]

        else:
            raise NotImplementedError("No puedes cargar archivos de tipo '%s' todavía." % tipo)
        return datos

    @staticmethod
    def texto_a_datos(datos):
        """
        Esta función toma una lista de datos en formato de texto y la convierte en matriz numpy. Valores vacíos ("") se
          convertirán a np.nan.

        :param datos: La lista de datos en formato de texto.
        :type datos: list

        :return: La matriz numpy de los datos. Datos que faltan se representan con np.nan
        :rtype: np.ndarray

        """
        matr = np.array(datos)
        matr[matr == ''] = np.nan
        return matr.astype(np.float)

    @staticmethod
    def leer_fechas(lista_fechas):
        """
        Esta función toma una lista de datos de fecha en formato de texto y detecta 1) la primera fecha de la lista,
          y 2) la posición relativa de cada fecha a esta.

        :param lista_fechas: Una lista con las fechas en formato de texto
        :type lista_fechas: list

        :return: Un tuple de la primera fecha, del vector numpy de la posición de cada fecha relativa a la primera,
          y del vector numpy de las fechas (numéricas) únicas.
        :rtype: (ft.date, np.ndarray, np.ndarray)

        """
        separadores = [
         '-', '/', ' ', '.']
        f = [
         '%d{0}%m{0}%y', '%m{0}%d{0}%y', '%d{0}%m{0}%Y', '%m{0}%d{0}%Y',
         '%d{0}%b{0}%y', '%m{0}%b{0}%y', '%d{0}%b{0}%Y', '%b{0}%d{0}%Y',
         '%d{0}%B{0}%y', '%m{0}%B{0}%y', '%d{0}%B{0}%Y', '%m{0}%B{0}%Y',
         '%y{0}%m{0}%d', '%y{0}%d{0}%m', '%Y{0}%m{0}%d', '%Y{0}%d{0}%m',
         '%y{0}%b{0}%d', '%y{0}%d{0}%b', '%Y{0}%b{0}%d', '%Y{0}%d{0}%b',
         '%y{0}%B{0}%d', '%y{0}%d{0}%B', '%Y{0}%B{0}%d', '%Y{0}%d{0}%B']
        formatos_posibles = [x.format(s) for s in separadores for x in f]
        if all([x.isdigit() for x in lista_fechas]):
            fecha_inic_datos = None
            vector_fechas = np.array(lista_fechas, dtype=int)
            list(set(lista_fechas)).sort()
            vector_únicas = np.array(lista_fechas, dtype=int)
        else:
            fechas = None
            for formato in formatos_posibles:
                try:
                    fechas = [ft.datetime.strptime(x, formato).date() for x in lista_fechas]
                    break
                except ValueError:
                    continue

            if fechas is None:
                raise ValueError('No puedo leer los datos de fechas. ¿Mejor le eches un vistazo a tu base de datos?')
            else:
                fecha_inic_datos = min(fechas)
                lista_fechas = [(x - fecha_inic_datos).days for x in fechas]
                vector_fechas = np.array(lista_fechas, dtype=int)
                list(set(lista_fechas)).sort()
                vector_únicas = np.array(lista_fechas, dtype=int)
        return (
         fecha_inic_datos, vector_fechas, vector_únicas)
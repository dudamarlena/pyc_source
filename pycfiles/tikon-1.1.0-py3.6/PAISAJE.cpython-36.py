# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\PAISAJE.py
# Compiled at: 2017-01-05 16:18:46
# Size of source mod 2**32: 9724 bytes
import os
from COSO import Coso
from Cultivo.SUELO import Suelo
from Cultivo.VARIEDAD import Variedad
from Parcela import Parcela
from RAE.REDES import Red
from geopy.distance import vincenty as dist
from tikon.Clima import Diario

class Paisaje(Coso):

    def __init__(símismo, nombre, datos=None, variedades_común=True, suelos_común=True, redes_común=True, fecha_inic='', fecha_fin='', reinic=None):
        dic = {'Directorio':'', 
         'Nombre':'',  'fecha_inic':fecha_inic,  'fecha_fin':fecha_fin,  'variedades_común':variedades_común, 
         'suelos_común':suelos_común,  'redes_común':redes_común,  'Parcelas':dict(Nombre=[], Long=[], Lat=[], Dilim=[]), 
         'RedAE':''}
        if reinic is None:
            reinic = datos is None
        super().__init__(nombre=nombre, ext='pais', dic=dic, directorio='Personales\\Paisajes', reinic=reinic)
        símismo.dic['Directorio'] = símismo.directorio
        símismo.dic['Nombre'] = símismo.nombre
        símismo.datos_crud = {}
        símismo.parcelas = {}
        símismo.suelos = {}
        símismo.meteos = {}
        símismo.variedades = {}
        símismo.resultados = {}
        símismo.distancias = {}
        símismo.red = None
        símismo.inic(datos)

    def inic(símismo, datos):
        if datos:
            datos_crudos = símismo.leer_documento(datos)
            for núm, nombre in enumerate(datos_crudos['Parcela']):
                nueva_parcela = Parcela(nombre=nombre, directorio=(símismo.directorio), suelos_común=(símismo.dic['suelos_común']),
                  variedades_común=(símismo.dic['variedades_común']),
                  redes_común=(símismo.dic['redes_común']))

                def leer_vars(obj):
                    for var in obj:
                        if type(var) is dict:
                            leer_vars(obj[var])
                        if var in datos_crudos:
                            try:
                                valor = float(datos_crudos[var][núm])
                            except ValueError:
                                valor = datos_crudos[var][núm]

                            obj[var] = valor

                leer_vars(nueva_parcela.dic)
                símismo.parcelas[nombre] = nueva_parcela

        else:
            if símismo.dic['redes_común']:
                símismo.red = Red(nombre=(símismo.dic['RedAE']))
            else:
                if os.path.isfile(os.path.join(símismo.directorio, símismo.nombre + '.red')):
                    símismo.red = Red(nombre=(símismo.dic['RedAE']))
                else:
                    dirección = os.path.join('Proyectos', 'Personales', 'Redes', símismo.nombre + '.red')
                    if os.path.isfile(dirección):
                        with open(dirección) as (d):
                            doc = d.readlines()
                        with open(os.path.join(símismo.directorio, símismo.nombre + '.red'), 'w') as (d):
                            d.write(doc)
                    else:
                        print('No se encontró la red agroecológica %s.' % (símismo.nombre + '.red'))
        for itema in símismo.parcelas.items():
            parcela = itema[1]
            if símismo.dic['suelos_común']:
                if parcela.dic['Suelo'] not in símismo.suelos:
                    símismo.suelos[parcela.dic['Suelo']] = Suelo(nombre=(parcela.dic['Suelo']), directorio=(símismo.directorio))
                parcela.suelo = símismo.suelos[parcela.dic['Suelo']]
            if símismo.dic['variedades_común']:
                if parcela.dic['Variedad'] not in símismo.variedades:
                    símismo.variedades[parcela.dic['Variedad']] = Variedad(nombre=(parcela.dic['Variedad']), directorio=(símismo.directorio))
                parcela.variedad = símismo.variedades[parcela.dic['Variedad']]
            meteo_temp = Diario(coord=(parcela.dic['Lat'], parcela.dic['Long']))
            meteo_temp.buscar(símismo.dic['fecha_inic'], símismo.dic['fecha_fin'])
            if meteo_temp.nombre not in símismo.meteos:
                símismo.meteos[meteo_temp.nombre] = Diario(nombre=(parcela.dic['Variedad']))
            parcela.meteo = símismo.meteos[meteo_temp.nombre]
            parcela.red = símismo.red
            for otro_itema in símismo.parcelas.items():
                otra_parcela = otro_itema[1]
                símismo.distancias[itema[0]][otro_itema[1]] = dist((parcela.dic['Lat'], parcela.dic['Long']), (
                 otra_parcela.dic['Lat'], otra_parcela.dic['Long']))

    @staticmethod
    def leer_documento(documento):
        try:
            with open(documento, mode='r') as (d):
                doc = d.readlines()
        except IOError:
            return 'El documento {0:s} no se pudo abrir.'.format(documento)
        else:
            datos_crud = {}
            variables = doc[0].replace(';', ',').split(',')
            for var in variables:
                datos_crud[var] = []

            for num_lín, línea in enumerate(doc[1:]):
                if len(línea):
                    valores = línea.replace(';', ',').split(',')
                    for posición, variable in enumerate(variables):
                        datos_crud[variable].append(valores[posición].replace('\n', ''))

            return datos_crud

    def simul(símismo, fecha_init, tiempo_simul, paso):
        fecha = fecha_init
        for parcela in símismo.parcelas:
            parcela.ejec(fecha_init)

        for tiempo in range(0, tiempo_simul):
            for parcela in símismo.parcelas:
                if parcela.cultivo.poll is not None:
                    pass
                fecha.incr(paso)
                parcela.incr(paso)
                for otra_parcela in símismo.parcelas:
                    if parcela is not otra_parcela:
                        for insecto in parcela.red.insectos:
                            distancia = parcela.dist[otra_parcela]
                            const_migr = parcela.RedAE.insecto.dic['const_migr']
                            migración = parcela.plagas[insecto] * const_migr * (1 / distancia) ** 2
                            parcela.emigración[insecto] += migración
                            otra_parcela.imigración[insecto] += migración

            for parcela in símismo.parcelas:
                for insecto in parcela.red.insectos:
                    parcela.red.insectos[insecto] -= parcela.emigración[insecto]
                    parcela.red.insectos[insecto] += parcela.imigración[insecto]
                    parcela.resultados[insecto]['Emigración'].append(parcela.emigración[insecto])
                    parcela.resultados[insecto]['Imigración'].append(parcela.imigración[insecto])
                    parcela.insectos = parcela.red.insectos

            símismo.resultados['Día'].append(fecha.díaaño)

        for parcela in símismo.parcelas:
            símismo.resultados[parcela] = parcela.resultados
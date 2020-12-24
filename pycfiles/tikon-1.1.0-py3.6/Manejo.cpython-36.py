# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Clima\Manejo.py
# Compiled at: 2016-08-26 12:42:31
# Size of source mod 2**32: 9128 bytes
import datetime as ft, json, os, numpy as np
from geopy.distance import vincenty as dist

def cargar_estación(documento, coord, elev, fecha_inic=None, fecha_fin=None, generar=True):
    """
    Limitaciones: 1) Al momento, solamente se leen documentos .csv de formato INSIVUMEH o con nombres de columnas
    Y UNIDADES iguales a los utilizados aquí: Fecha, [Hora], Precip (mm), Rad_sol (MJ/m2/día), y Temp (C).
    :param documento:
    :param coord:
    :param elev:
    :param fecha_inic:
    :param fecha_fin:
    :param generar:
    :return:
    """
    dic = dict(Elev=elev, Coord=coord, Fecha=[], Datos=dict(Precip=[], Rad_sol=[], Temp_máx=[], Temp_mín=[]))
    faltan = False
    faltan_puntos = dic['Datos'].copy()
    faltan_porciones = dic['Datos'].copy()
    fechatiempos = []
    if '.día' in documento:
        dic = json.load(documento)
        for n, f in enumerate(dic['Fecha']):
            dic['Fecha'][n] = ft.datetime(f[2], f[1], f[0])

    else:
        if '.csv' in documento:
            insivumeh = False
            precip_hora = temp_hora = rad_sol_hora = []
            with open(documento) as (d):
                doc = d.readlines()
            variables = doc[0].split(',')
            conv_var_insivumeh = {'Lluvia':'Precip',  'R.Global':'Rad_sol',  'Temp.Ai':'Temp'}
            for n, var in enumerate(variables):
                if '[w/m2]' in var:
                    insivumeh = True
                for var_INSI in conv_var_insivumeh:
                    if var_INSI in var:
                        variables[n] = conv_var_insivumeh[var_INSI]

            for i in doc[1:]:
                datos = i.split(',')
                f = datos[variables.index('Fecha')].split('/')
                fechatiempos.append(ft.datetime(int(f[2]), int(f[1]), int(f[0])))
                if 'Hora' in variables:
                    h = datos[variables.index('Hora')].split(':')
                    fechatiempos[-1] = fechatiempos[(-1)].replace(hour=(int(h[0])), minute=(int(h[1])), second=(int(h[2])))
                precip = variables.index('Precip')
                rad_sol = variables.index('Rad_sol')
                temp = variables.index('Temp')
                for var in [precip, rad_sol, temp]:
                    if datos[var] == '':
                        datos[var] = float('NaN')

                precip_hora.append(float(precip))
                rad_sol_hora.append(float(rad_sol))
                temp_hora.append(float(temp))

            if insivumeh:
                rad_sol_hora = [i * 0.0036 for i in rad_sol_hora]
            lluvia_cum = precip_hora[0]
            rad_sol_cum = rad_sol_hora[0]
            temp_día = [temp_hora[0]]
            for n, i in enumerate(fechatiempos[1:]):
                if i.date() == fechatiempos[(n - 1)].date():
                    lluvia_cum += precip_hora[n]
                    rad_sol_cum += (rad_sol_hora[n] + rad_sol_hora[(n - 1)]) * (fechatiempos[n].hour - fechatiempos[(n - 1)].hour) / 2
                    temp_día.append(temp_hora[n])
                else:
                    dic['Datos']['Precip'].append(lluvia_cum)
                    lluvia_cum = precip_hora[(n + 1)]
                    dic['Datos']['Rad_sol'].append(rad_sol_cum)
                    rad_sol_cum = rad_sol_hora[(n + 1)]
                    dic['Datos']['Temp_mín'].append(min(temp_día))
                    dic['Datos']['Temp_máx'].append(max(temp_día))
                    temp_día = [temp_hora[(n + 1)]]
                    dic['Datos']['Fecha'].append(fechatiempos[n].date())

        else:
            return False
    if not generar:
        return ordenar(dic)
    else:
        if fecha_inic is None:
            fecha_inic = min(dic['Fecha'])
        if fecha_fin is None:
            fecha_fin = max(dic['Fecha'])
        f = fecha_inic
        while f <= fecha_fin:
            if f not in dic['Fecha']:
                dic['Fecha'].append(f)
                for var in dic['Datos']:
                    dic['Datos'][var].append(float('NaN'))

        dic = ordenar(dic)
        for var in dic['Datos']:
            dic[var] = np.array(dic[var])

        for var in dic['Datos']:
            for n, i in enumerate(dic['Datos'][var]):
                if np.isnan(i):
                    faltan_puntos[var].append(dic['Datos'][var]['Fecha'][n])
                    faltan = True

        while n < len(faltan_puntos[var]):
            consecutivos = 0
            while (faltan_puntos[var][(n + 1)] - faltan_puntos[var][n]).days == 1:
                consecutivos += 1
                n += 1

            if consecutivos >= 9:
                faltan_porciones[var] += (faltan_puntos[var][(n - consecutivos)], faltan_puntos[var][n])

        for i in faltan_porciones[var]:
            faltan_puntos[var].pop(faltan_puntos[var].index(i))

        return (dic, faltan, faltan_puntos, faltan_porciones)


def ordenar(dic):
    a_ordenar = [
     dic['Fecha']]
    variables = sorted(list(dic['Datos'].keys()))
    for var in variables:
        a_ordenar.append(dic['Datos'][var])

    ordenados = [x for x in sorted((zip(a_ordenar)), key=(lambda dato: dato[0]))]
    ordenados = list(zip(*ordenados))
    for n, var in a_ordenar[1:]:
        dic['Datos'][var] = ordenados[n]

    dic['Fecha'] = ordenados[0]
    return dic


def buscar_cercanas(n, coord, estaciones):
    nombres_cercanas = distancias = []
    for i in estaciones:
        distancia = dist((estaciones[i]['Lat'], estaciones[i]['Long']), coord).km
        if distancia < max(distancias) or len(nombres_cercanas) < n:
            if len(nombres_cercanas) >= n:
                índice = distancias.index(max(distancias))
                nombres_cercanas.pop(índice)
                distancias.pop(índice)
            distancias.append(distancia)
            nombres_cercanas.append(estaciones[i]['Estación'])

    estaciones_cercanas = []
    for i in nombres_cercanas:
        estaciones_cercanas.append(cargar_estación((os.path.join('Proyectos', 'Clima', i, '.csv')), generar=False)[0])

    return estaciones_cercanas


def verificar_fechas(var, estaciones, fechas):
    """
    var: nombre de la variable
    estaciones: lista de los diccionarios de datos de las estaciones a verificar
    fechas: lista de fechas de datos que faltan
    """
    verificados = []
    for estación in estaciones:
        for fecha in fechas:
            if fecha in estación['Fecha']:
                if not np.isnan(estación[var][estaciones['Fecha'].index(fecha)]):
                    verificados.append(estación)
                    break

    return verificados
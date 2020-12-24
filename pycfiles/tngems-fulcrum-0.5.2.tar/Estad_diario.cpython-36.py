# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Clima\Estad_diario.py
# Compiled at: 2016-08-26 12:42:29
# Size of source mod 2**32: 10115 bytes
import random, numpy as np
from PyKrige.uk import UniversalKriging as krigUniversal
from scipy import stats as estad
__author__ = 'Julien Malard'

def move1(x, y):
    x = np.array(x)
    y = np.array(y)
    r = np.correlate(y, x)
    b_move = np.nanstd(y) / np.nanstd(x)
    if r < 0:
        b_move *= -1
    a_move = np.nanmean(y) - b_move * np.nanmean(x)
    return (
     a_move[0], b_move[0])


def ktrl(x, y):
    x = np.array(x)
    y = np.array(y)
    w = x.size()
    k = []
    for i in range(w - 1, 1, -1):
        for j in range(0, i - 2):
            yk = y[i] - y[j]
            xk = x[i] - x[j]
            k.append(yk / xk)

    k = np.array(k)
    b_ktrl = np.nanmedian(k)
    a_ktrl = np.nanmedian(y) - b_ktrl * np.nanmedian(x)
    return (
     a_ktrl[0], b_ktrl[0])


def ktrl2(x, y):
    x = np.array(x)
    y = np.array(y)
    qx = np.percentile(x, list(range(5, 100, 5)))
    qy = np.percentile(y, list(range(5, 100, 5)))
    k2 = []
    for i in range(18, 1, -1):
        for j in range(0, i - 2):
            yk2 = qy[i] - qy[j]
            xk2 = qx[i] - qx[j]
            k2.append(yk2 / xk2)

    k2 = np.array(k2)
    b_ktrl2 = np.nanmedian(k2)
    a_ktrl2 = np.nanmedian(y) - b_ktrl2 * np.nanmedian(x)
    return (
     a_ktrl2[0], b_ktrl2[0])


def rloc(x, y):
    x = np.array(x)
    y = np.array(y)
    r = np.correlate(y, x)
    qx = np.percentile(x, list(range(5, 100, 5)))
    qy = np.percentile(y, list(range(5, 100, 5)))
    b_rloc = (qy[14] - qy[4]) / (qx[14] - qx[4])
    if r < 0:
        b_rloc *= -1
    a_rloc = np.nanmedian(y) - b_rloc * np.nanmedian(x)
    return (
     a_rloc[0], b_rloc[0])


def reg_lin(x, y):
    x = np.array(x)
    y = np.array(y)
    pendiente, intersección = estad.linregress(x, y)[0:2]
    return (
     intersección, pendiente)


def verificar_atípicos(x, nivel=3.5):
    """
    Código modificado del código de Joe Kingston,
    http://stackoverflow.com/questions/22354094/pythonic-way-of-detecting-outliers-in-one-dimensional-observation-data
    """
    x = np.array(x)
    if len(x.shape) == 1:
        x = x[:, None]
    mediano = np.nanmedian(x, axis=0)
    dif = np.absolute(np.nansum((x - mediano), axis=(-1)))
    med_abs_deviation = np.nanmedian(dif)
    z_modificado = 0.6745 * dif / med_abs_deviation
    return (z_modificado > nivel).sum()


def eval_estaciones(var, lugar, cercanas, tipo):
    a_final = b_final = r2 = datos = None
    atípicos = verificar_atípicos(lugar[var])
    for i in cercanas:
        atípicos = atípicos or verificar_atípicos(cercanas[i][var])

    X = []
    Y = []
    f = min(cercanas['Fecha'], lugar['Fecha'])
    while f <= max(cercanas['Fecha'], lugar['Fecha']):
        if f in cercanas['Fecha']:
            X += cercanas[var][cercanas['Fecha'].index(f)]
            if f in lugar['Fecha']:
                Y += lugar[var][lugar['Fecha'].index(f)]
            else:
                Y += float('NaN')
        else:
            if f in lugar['Fecha']:
                X += float('NaN')
                Y += lugar[var][lugar['Fecha'].index(f)]
            f += 1

    completos = [(x, y) for x, y in zip(X, Y) if not np.isnan(x) if not np.isnan(y)]
    completos = np.array(list(zip(*completos)))
    for otra_estación in cercanas:
        if tipo == 'puntual':
            if atípicos:
                a, b = ktrl(completos[0], completos[1])
            else:
                a, b = reg_lin(completos[0], completos[1])
            estimados = []
            verdaderos = []
            for j in range(100):
                a_quitar = random.sample(range(len(X)), round(len(X) * 0.1))
                conocidos_y = Y.copy()
                conocidos_x = X.copy()
                quitados_y = quitados_x = []
                for i in a_quitar:
                    quitados_x.append = conocidos_x.pop(i)
                    quitados_y.append = conocidos_y.pop(i)

                if atípicos:
                    a_estim, b_estim = ktrl(conocidos_x, conocidos_y)
                else:
                    a_estim, b_estim = reg_lin(conocidos_x, conocidos_y)
                estimados += a_estim + b_estim * quitados_x
                verdaderos += quitados_y

        else:
            if tipo == 'extensa':
                if atípicos:
                    a, b = ktrl2(completos[0], completos[1])
                else:
                    a, b = move1(completos[0], completos[1])
                estimados = []
                verdaderos = []
                for j in range(100):
                    inic = random.randint(0, len(X) - round(len(X) * 0.1))
                    fin = inic + round(len(X) * 0.1)
                    a_quitar = range(inic, fin)
                    conocidos_y = Y.copy()
                    conocidos_x = X.copy()
                    quitados_y = quitados_x = []
                    for i in a_quitar:
                        quitados_x.append = conocidos_x.pop(i)
                        quitados_y.append = conocidos_y.pop(i)

                    if atípicos:
                        a_estim, b_estim = ktrl(conocidos_x, conocidos_y)
                    else:
                        a_estim, b_estim = reg_lin(conocidos_x, conocidos_y)
                    estimados += a_estim + b_estim * quitados_x
                    verdaderos += quitados_y

            else:
                return False
        r2_nuevo = np.corrcoef(estimados, verdaderos) ** 2
        if not r2 or r2 < r2_nuevo:
            r2 = r2_nuevo
            a_final = a
            b_final = b
            datos = otra_estación

    return (a_final, b_final, datos)


def krigear(lugar, cercanas, fecha_inic, fecha_fin):
    x = y = elev = []
    for estación in cercanas:
        x += estación['Coord'][0]
        y += estación['Coord'][1]
        elev += estación['Elev']

    for var in lugar['Datos']:
        f = fecha_inic
        while f <= fecha_fin:
            valor = []
            for estación in cercanas:
                valor += estación['Datos'][var][estación['Fecha'].index(f)]

            krigeaje = krigUniversal(x, y, valor, variogram_model='linear', drift_terms=['specified'], specified_drift=[
             np.array(elev)])
            lugar[var] = krigeaje.execute('points', (lugar['Coord'][0]), (lugar['Coord'][1]), specified_drift_arrays=[
             np.array(lugar['Elev'])])[0][0]
            f += 1

    return lugar
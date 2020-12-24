# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Matemáticas\Arte.py
# Compiled at: 2017-11-13 14:49:06
# Size of source mod 2**32: 10812 bytes
import os, numpy as np, pymc
from matplotlib import pyplot as dib
from scipy import stats as estad
from tikon.Matemáticas.Incert import texto_a_dist

def graficar_línea(datos, título, etiq_y=None, etiq_x='Día', color=None, directorio=None, mostrar=False):
    """

    :param datos:
    :type datos: np.ndarray
    :param título:
    :type título: str
    :param etiq_y:
    :type etiq_y: str
    :param etiq_x:
    :type etiq_x: str
    :param color:
    :type color: str
    :param directorio:
    :type directorio: str

    """
    graficar_pred(matr_predic=datos, título=título, etiq_y=etiq_y, etiq_x=etiq_x, color=color, directorio=directorio, mostrar=mostrar,
      vector_obs=None,
      promedio=True,
      n_líneas=0,
      incert=None)


def graficar_pred(matr_predic, título, vector_obs=None, tiempos_obs=None, etiq_y=None, etiq_x='Día', color=None, promedio=True, incert='componentes', n_líneas=0, mostrar=True, directorio=None):
    """
    Esta función genera un gráfico, dato una matriz de predicciones y un vector de observaciones temporales.

    :param matr_predic: La matriz de predicciones. Eje 0 = incertidumbre estocástico, eje 1 = incertidumbre
    paramétrico, eje 2 = día.
    :type matr_predic: np.ndarray

    :param vector_obs: El vector de las observaciones. Eje 0 = tiempo.
    :type vector_obs: np.ndarray | None

    :param tiempos_obs: El vector de los tiempos de las observaciones.
    :type tiempos_obs: np.ndarray

    :param título: El título del gráfico
    :type título: str

    :param etiq_y: La etiqueta para el eje y del gráfico.
    :type etiq_y: str

    :param etiq_x: La etiqueta para el eje x del gráfico
    :type etiq_x: str

    :param color: El color para el gráfico
    :type color: str

    :param promedio: Si hay que mostrar el promedio de las repeticiones o no.
    :type promedio: bool

    :param incert: El tipo de incertidumbre para mostrar (o no). Puede ser None, 'confianza', o 'descomponer'.
    :type incert: str | None

    :param todas_líneas: Si hay que mostrar todas las líneas de las repeticiones o no.
    :type todas_líneas: bool

    :param n_líneas:
    :type n_líneas: int

    :param mostrar: Si hay que mostrar el gráfico de inmediato, o solo guardarlo.
    :type mostrar: bool

    :param directorio: El archivo donde guardar el gráfico
    :type directorio: str

    Parameters
    ----------
    n_líneas
    n_líneas

    """
    if color is None:
        color = '#99CC00'
    else:
        if etiq_y is None:
            etiq_y = título
        else:
            if mostrar is False:
                if directorio is None:
                    raise ValueError('Hay que especificar un archivo para guardar el gráfico de %s.' % título)
                elif not os.path.isdir(directorio):
                    os.makedirs(directorio)
            x = np.arange(matr_predic.shape[2])
            prom_predic = matr_predic.mean(axis=(0, 1))
            if promedio:
                dib.plot(x, prom_predic, lw=2, color=color)
            if vector_obs is not None:
                if tiempos_obs is None:
                    tiempos_obs = np.arange(len(vector_obs))
                vacíos = np.where(~np.isnan(vector_obs))
                tiempos_obs = tiempos_obs[vacíos]
                vector_obs = vector_obs[vacíos]
                dib.plot(tiempos_obs, vector_obs, 'o', color=color, label='Obs')
                dib.plot(tiempos_obs, vector_obs, lw=1, color='#000000')
        if incert is None:
            pass
        else:
            if incert == 'confianza':
                percentiles = [
                 50, 75, 95, 99, 100]
                percentiles.sort()
                máx_perc_ant = mín_perc_ant = prom_predic
                for n, p in enumerate(percentiles):
                    máx_perc = np.percentile(matr_predic, (50 + p / 2), axis=(0, 1))
                    mín_perc = np.percentile(matr_predic, ((100 - p) / 2), axis=(0,
                                                                                 1))
                    op_máx = 0.5
                    op_mín = 0.01
                    opacidad = (1 - n / (len(percentiles) - 1)) * (op_máx - op_mín) + op_mín
                    dib.fill_between(x, máx_perc_ant, máx_perc, facecolor=color,
                      alpha=opacidad,
                      linewidth=0.5,
                      edgecolor=color)
                    dib.fill_between(x, mín_perc, mín_perc_ant, facecolor=color,
                      alpha=opacidad,
                      linewidth=0.5,
                      edgecolor=color)
                    mín_perc_ant = mín_perc
                    máx_perc_ant = máx_perc

            else:
                if incert == 'componentes':
                    máx_total = matr_predic.max(axis=(0, 1))
                    mín_total = matr_predic.min(axis=(0, 1))
                    rango_total = np.subtract(máx_total, mín_total)
                    des_est_total = np.std(matr_predic, axis=(0, 1))
                    des_est_estóc = np.mean(np.std(matr_predic, axis=0), axis=0)
                    des_est_parám = np.subtract(des_est_total, des_est_estóc)
                    frac_des_est_parám = np.divide(des_est_parám, des_est_total)
                    incert_parám = np.multiply(rango_total, frac_des_est_parám)
                    mitad = np.divide(np.add(máx_total, mín_total), 2)
                    máx_parám = np.add(mitad, np.divide(incert_parám, 2))
                    mín_parám = np.subtract(mitad, np.divide(incert_parám, 2))
                    dib.fill_between(x, máx_parám, mín_parám, facecolor=color, alpha=0.5, label='Incert paramétrico')
                    dib.fill_between(x, máx_total, mín_total, facecolor=color, alpha=0.3, label='Incert estocástico')
                else:
                    raise ValueError('No entiendo el tipo de incertidumbre "%s" que especificaste para el gráfico.' % incert)
            if n_líneas > 0:
                n_rep_estoc = matr_predic.shape[0]
                n_rep_parám = matr_predic.shape[1]
                rep_total = n_rep_estoc * n_rep_parám
                if n_líneas > rep_total:
                    n_líneas = rep_total
                í_líneas = np.random.randint(rep_total, size=n_líneas)
                í_lín_estoc = np.floor_divide(í_líneas, n_rep_estoc)
                í_lín_parám = np.remainder(í_líneas, n_rep_parám)
                for n in range(í_lín_estoc.shape[0]):
                    dib.plot(x, (matr_predic[(í_lín_estoc[n], í_lín_parám[n])]), lw=1, color=color)

            dib.xlabel(etiq_x)
            dib.ylabel(etiq_y)
            dib.title(título)
            dib.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
        if mostrar is True:
            dib.show()
        else:
            if directorio[-4:] != '.png':
                válidos = (' ', '.', '_')
                nombre_arch = ''.join(c for c in título + '.png' if c.isalnum() or c in válidos).rstrip()
                directorio = os.path.join(directorio, nombre_arch)
            dib.savefig(directorio)
            dib.close()


def graficar_dists(dists, n=100000, valores=None, rango=None, título=None, archivo=None):
    """
    Esta función genera un gráfico de una o más distribuciones y valores.

    :param dists: Una lista de las distribuciones para graficar.
    :type dists: list[str, pymc.Deterministic, pymc.Stochastic]

    :param n: El número de puntos para el gráfico.
    :type n: int

    :param valores: Una matriz numpy de valores para hacer un histograma (opcional)
    :type valores: np.ndarray

    :param rango: Un rango de valores para resaltar en el gráfico (opcional).
    :type rango: tuple

    :param título: El título del gráfico, si hay.
    :type título: str

    :param archivo: Dónde hay que guardar el dibujo. Si no se especifica, se presentará el gráfico al usuario en una
      nueva ventana (y el programa esperará que la usadora cierra la ventana antes de seguir con su ejecución).
    :type archivo: str

    """
    if type(dists) is not list:
        dists = [
         dists]
    else:
        dib.close()
        for dist in dists:
            if type(dist) is str:
                dist = texto_a_dist(texto=dist, usar_pymc=False)
            else:
                if isinstance(dist, pymc.Stochastic):
                    puntos = np.array([dist.rand() for _ in range(n)])
                    y, delim = np.histogram(puntos, normed=True, bins=(n // 100))
                    x = 0.5 * (delim[1:] + delim[:-1])
                else:
                    if isinstance(dist, pymc.Deterministic):
                        dist_stoc = min(dist.extended_parents)
                        puntos = np.array([(dist_stoc.rand(), dist.value)[1] for _ in range(n)])
                        y, delim = np.histogram(puntos, normed=True, bins=(n // 100))
                        x = 0.5 * (delim[1:] + delim[:-1])
                    else:
                        if isinstance(dist, estad._distn_infrastructure.rv_frozen):
                            x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), n)
                            y = dist.pdf(x)
                        else:
                            raise TypeError('El tipo de distribución "%s" no se reconoce como distribución aceptada.' % type(dist))
            dib.plot(x, y, 'b-', lw=2, alpha=0.6)
            if rango is not None:
                if rango[1] < rango[0]:
                    rango = (
                     rango[1], rango[0])
                dib.fill_between((x[((rango[0] <= x) & (x <= rango[1]))]), 0, (y[((rango[0] <= x) & (x <= rango[1]))]), color='blue',
                  alpha=0.2)

        if valores is not None:
            dib.hist(valores, normed=True, color='green', histtype='stepfilled', alpha=0.2)
        if título is not None:
            dib.title(título)
        if archivo is None:
            dib.show()
        else:
            inacceptables = [
             ':', ';', '/', '\\']
            for i in inacceptables:
                título = título.replace(i, '_')

            if archivo[-4:] != '.png':
                archivo = os.path.join(archivo, título + '.png')
            dib.savefig(archivo)
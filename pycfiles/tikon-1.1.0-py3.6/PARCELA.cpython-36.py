# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\PARCELA.py
# Compiled at: 2017-01-05 16:18:45
# Size of source mod 2**32: 6601 bytes
import os
from tikon.Cultivo.CULTIVO import Cultivo

class Parcela(object):

    def __init__(símismo, nombre, directorio, suelos_común, variedades_común, redes_común):
        símismo.dic = {'Suelo':'', 
         'Variedad':'',  'Meteo':'',  'RedAE':'',  'Long':(),  'Lat':(),  'Área':(),  'Surcos':(),  'Long_surcos':(),  'Pendiente_orientación':'',  'Piedras':'',  'Fecha_init':'', 
         'Manejo':dict(Fecha_siembra='', Fecha_emergencia='', Población_siembra=[], Población_emerg=[], Método_siembra=[], Distribución_siembra=[], Espacio_surcos=[], Dirección_surcos=[], Profund_siembra=[], Peso_material_sembrado=[], Edad_transplantaciones=[], Temp_transplantación=[], Plantas_por_montículo=[], Eficiencia_irrig=[], Profund_manejo_irrig=[], Hum_empiezo_irrig_auto=[], Hum_fin_irrig_auto=[], Estadio_crec_fin_irrig=[], Método_irrig=[], Cantidad_por_irrig=[], Fecha_abono=[], Material_abono=[], Método_app_abono=[], Profund_abono=[], Abono_N=[], Abono_P=[], Abono_K=[], Abono_Ca=[], Abono_otro_conc=[], Abono_otro_cód=[], Fecha_incorp_resid=[], Material_resid=[], Resid_N=[], Resid_P=[], Resid_K=[], Resid_porcent_incorp=[], Resid_prodund_incorp=[], Fecha_labranza=[], Herramienta_labranza=[], Profund_labranza=[], Fecha_cosecha=[], Estadio_cosecha=[], Componente_cosecha=[], Grupo_tamaño_cosecha=[], Porcent_cosecha=[], Irrig=True, Irrig_auto=True, Cant_irrig_auto=())}
        símismo.suelos_común = suelos_común
        símismo.variedades_común = variedades_común
        símismo.redes_común = redes_común
        símismo.suelo = None
        símismo.variedad = None
        símismo.meteo = None
        símismo.red = None
        if not símismo.variedades_común or not símismo.suelos_común:
            if not os.path.exists(os.path.splitext(símismo.documento)[0]):
                os.makedirs(os.path.splitext(símismo.documento)[0])
        else:
            if símismo.variedades_común:
                carpeta_variedad = 'Parcelas\\Variedades'
            else:
                carpeta_variedad = símismo.carpeta
            if símismo.suelos_común:
                carpeta_suelo = 'Parcelas\\Suelos'
            else:
                carpeta_suelo = símismo.carpeta
            if símismo.redes_común:
                carpeta_redes = 'Parcelas\\Redes'
            else:
                carpeta_redes = símismo.carpeta
        símismo.cultivo = Cultivo(cultivo=(símismo.cultivo), variedad=(símismo.variedad),
          suelo=(símismo.dic['Suelo']),
          meteo=(símismo.dic['Meteo']),
          manejo=(símismo.dic))
        símismo.estado_cultivo = {}
        for var in símismo.cultivo.egresos:
            símismo.estado_cultivo[var] = ()

        símismo.daño_plagas = {}
        símismo.insectos = {}
        for insecto in símismo.red.insectos:
            símismo.insectos[insecto] = ()

        símismo.resultados = dict(Emigración=[], Imigración=[], Día=[0])
        for dato in símismo.cultivo.egresos:
            símismo.resultados[dato] = ()

        for insecto in símismo.insectos:
            símismo.resultados[insecto]['Emigración'] = [
             0]
            símismo.resultados[insecto]['Imigración'] = [0]

    def ejec(símismo):
        carpeta_egr = os.path.join(símismo.carpeta, 'documentos_mod_cul')
        símismo.cultivo.ejec(carpeta=carpeta_egr)
        símismo.red = eval(símismo.dic['RedAE'])
        símismo.resultados['Día'] = [0]

    def incr(símismo, paso):
        if símismo.cultivo.proceso.poll is None:
            símismo.cultivo.incr(paso, símismo.daño_plagas)
            símismo.estado_cultivo = símismo.cultivo.egresos
            símismo.daño_plagas, símismo.insectos = símismo.red.incr(símismo.estado_cultivo, paso)
            for dato in símismo.estado_cultivo:
                if dato not in símismo.resultados:
                    símismo.resultados[dato] = []
                símismo.resultados[dato].append(símismo.estado_cultivo[dato])

            for dato in símismo.daño_plagas:
                if dato not in símismo.resultados:
                    símismo.resultados[dato] = []
                símismo.resultados[dato].append(símismo.daño_plagas[dato])

            for dato in símismo.insectos:
                if dato not in símismo.resultados:
                    símismo.resultados[dato] = []
                símismo.resultados[dato].append(símismo.insectos[dato])

            símismo.resultados['Día'].append = símismo.resultados['Día'][(-1)] + paso
        else:
            return 'Modelo de cultivo terminado.'
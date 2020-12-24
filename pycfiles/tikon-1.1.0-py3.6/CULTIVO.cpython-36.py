# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Cultivo\CULTIVO.py
# Compiled at: 2017-01-24 13:42:13
# Size of source mod 2**32: 5478 bytes
import os, subprocess
from COSO import Simulable
from Cultivo.Controles import dir_DSSAT
from Cultivo.Controles import sacar_modelos_disp
import tikon.Cultivo.ModExtern.DSSAT.DSSAT as DSSAT

class Cultivo(Simulable):

    def __init__(símismo, cultivo, variedad, suelo, meteo, manejo, modelo=''):
        símismo.cultivo = cultivo
        símismo.variedad = variedad
        símismo.suelo = suelo
        símismo.meteo = meteo
        símismo.manejo = manejo
        símismo.modelo = modelo
        símismo.egresos = {'raices':(),  'hojas':(),  'asim':(),  'tallo':(),  'semillas':(),  'frutas':{},  'nubes':(),  'humrel':(),  'lluvia':(),  'tprom':(),  'tmin':(),  'tmax':(),  'radsol':(),  'tsuelo':(),  'humsuelo':()}
        símismo.proceso = None

    def ejec(símismo, carpeta):
        modelos_disp = sacar_modelos_disp(símismo.cultivo)
        if not len(símismo.modelo):
            if símismo.cultivo in modelos_disp:
                símismo.modelo = list(modelos_disp.keys())[0]
            else:
                return 'No existe modelo de cultivo válido para cultivo' + símismo.cultivo + '.'
        programa = modelos_disp[símismo.modelo]['Programa']
        comanda = modelos_disp[símismo.modelo]['Comanda']
        if not os.path.isdir(carpeta):
            os.makedirs(carpeta)
        else:
            if programa == 'DSSAT':
                dssat = DSSAT.Experimento(carpeta, suelo=(símismo.suelo), variedad=(símismo.variedad), meteo=(símismo.meteo), cultivo=(símismo.cultivo),
                  manejo=(símismo.manejo))
                dssat.gen_ingresos()
                comanda = os.path.join(dir_DSSAT, comanda) + ' B ' + carpeta + 'DSSBatch.v46'
            else:
                if programa == 'CropSyst':
                    return 'Falta un módulo para CropSyst.'
                else:
                    return 'Modelo de cultivo no reconocido.'
        símismo.proceso = subprocess.Popen(comanda, shell=True,
          stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE),
          cwd=carpeta)

    def incr(símismo, paso, daño_plagas):
        daño_plagas_texto = ''
        for daño in daño_plagas:
            daño_plagas_texto += daño + ': ' + daño_plagas[daño] + '; '

        daño_plagas_texto.replace('ñ', 'n').replace('í', 'i').replace('é', 'e').replace('á', 'a').replace('ó', 'o')
        daño_plagas_texto.replace('ú', 'u').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O')
        daño_plagas_texto.replace('Ú', 'U')
        for día in paso:
            símismo.proceso.stdin.write(daño_plagas_texto)
            símismo.proceso.stdin.flush()
            línea = símismo.proceso.stdout.readline()
            while 'Empezando' not in línea and len(línea):
                for egreso in símismo.egresos:
                    if egreso in línea:
                        símismo.egresos[egreso] = float(línea.decode()[len(egreso):len(línea)])

                línea = símismo.proceso.stdout.readline()
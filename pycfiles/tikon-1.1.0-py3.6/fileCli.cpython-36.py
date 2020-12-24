# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Cultivo\ModExtern\DSSAT\fileCli.py
# Compiled at: 2017-01-05 16:18:48
# Size of source mod 2**32: 5166 bytes
import os
from tikon.Cultivo.Controles import dir_DSSAT

class FileCli(object):

    def __init__(símismo):
        símismo.dic = {'SITE':[],  'INSI':[],  'LAT':[],  'LONG':[],  'ELEV':[],  'TAV':[],  'AMP':[],  'SPRAY':[],  'TMXY':[],  'TMNY':[],  'RAIY':[],  'START':[],  'DURN':[],  'ANGA':[],  'ANGB':[],  'REFHT':[],  'WNDHT':[],  'SOURCE':[],  'GSST':[],  'GSDU':[],  'MONTH':[],  'SAMN':[],  'XAMN':[],  'NAMN':[],  'RTOT':[],  'RNUM':[],  'SHMN':[],  'AMTH':[],  'BMTH':[],  'MTH':[],  'SDMN':[],  'SDSD':[],  'SWMN':[],  'SWSD':[],  'XDMN':[],  'XDSD':[],  'XWMN':[],  'XWSD':[],  'NASD':[],  'ALPHA':[],  'PDW':[]}
        símismo.prop_vars = {'SITE':50, 
         'INSI':5,  'LAT':8,  'LONG':8,  'ELEV':5,  'TAV':5,  'AMP':5,  'SPRAY':5,  'TMXY':5, 
         'TMNY':5,  'RAIY':5,  'START':5,  'DURN':5,  'ANGA':5,  'ANGB':5,  'REFHT':5, 
         'WNDHT':5,  'SOURCE':20,  'GSST':5,  'GSDU':5,  'MONTH':5,  'SAMN':5,  'XAMN':5,  'NAMN':5, 
         'RTOT':5,  'RNUM':5,  'SHMN':5,  'AMTH':5,  'BMTH':5,  'MTH':5,  'SDMN':5, 
         'SDSD':5,  'SWMN':5,  'SWSD':5,  'XDMN':5,  'XDSD':5,  'XWMN':5,  'XWSD':5, 
         'NASD':5,  'ALPHA':5,  'PDW':5}

    def leer(símismo, cod_clima):
        for i in símismo.dic:
            símismo.dic[i] = []

        encontrado = False
        for doc_clima in os.listdir(os.path.join(dir_DSSAT, 'Weather', 'Climate')):
            if doc_clima.upper().endswith('.CLI') and cod_clima.upper() in doc_clima.upper():
                with open(os.path.join(dir_DSSAT, 'Weather', 'Climate', doc_clima)) as (d):
                    doc = d.readlines()
                    símismo.decodar(doc)
                encontrado = True

        if not encontrado:
            print("Error: El código de clima no se ubica en la base de datos 'Clima' de DSSAT.")
            return False

    def escribir(símismo):
        cod_clim = símismo.dic['INSI'] + 'TKON'
        for i in símismo.dic:
            if not len(símismo.dic[i]):
                símismo.dic[i] = [
                 '-99']

        with open('FILECli.txt', 'r') as (d):
            esquema = d.readlines()
        esquema.append('\n')
        esquema = símismo.encodar(esquema)
        esquema = ''.join(esquema)
        with open(os.path.join(dir_DSSAT, 'Weather', 'Clima', cod_clim, '.CLI'), 'w') as (d):
            d.write(''.join(esquema))

    def decodar(símismo, doc):
        for línea in doc:
            if '*' in línea:
                if 'CLIMATE' in línea:
                    símismo.dic['SITE'] = línea[línea.index(':') + 1:].strip()
                    continue
                if '@' in línea:
                    variables = línea.replace('@', '').split()
                    núm_lin = línea + 1
                    while '@' not in doc[núm_lin] and doc[núm_lin] != '\n':
                        valores = doc[núm_lin].replace('\n', '')
                        for j, var in enumerate(variables):
                            if var in símismo.dic:
                                valor = valores[:símismo.prop_vars[var] + 1].strip()
                                símismo.dic[var].append(valor)
                                valores = valores[símismo.prop_vars[var] + 1:]

                        núm_lin += 1

    def encodar(símismo, doc_clima):
        for n, línea in enumerate(doc_clima):
            l = n
            texto = línea
            if '{' in texto:
                var = texto[texto.index('{') + 2:texto.index(']')]
                for k, a in enumerate(símismo.dic[var]):
                    l += 1
                    nueva_línea = texto.replace('[', '').replace(']', '[' + str(k) + ']')
                    nueva_línea = (nueva_línea.format)(**símismo.dic)
                    doc_clima.insert(l, nueva_línea)

                doc_clima.remove(texto)

        return doc_clima
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Cultivo\ModExtern\DSSAT\fileW.py
# Compiled at: 2017-01-05 16:18:43
# Size of source mod 2**32: 4461 bytes
import os
from tikon.Cultivo.Controles import dir_DSSAT

class FileW(object):

    def __init__(símismo):
        símismo.dic = {'SITE':'', 
         'INSI':'',  'LAT':(),  'LONG':(),  'ELEV':(),  'TAV':(),  'AMP':(),  'REFHT':(),  'WNDHT':(),  'DATE':[],  'SRAD':[],  'TMAX':[],  'TMIN':[],  'RAIN':[],  'DEWP':[],  'WIND':[],  'PAR':[]}
        símismo.prop_vars = {'SITE':100, 
         'INSI':5,  'LAT':8,  'LONG':8,  'ELEV':5,  'TAV':5,  'AMP':5,  'REFHT':5,  'WNDHT':5,  'DATE':5, 
         'SRAD':5,  'TMAX':5,  'TMIN':5,  'RAIN':5,  'DEWP':5,  'WIND':5,  'PAR':5}

    def leer(símismo, cod_clima):
        for i in símismo.dic:
            símismo.dic[i] = []

        encontrado = False
        for doc_clima in os.listdir(os.path.join(dir_DSSAT, 'Weather')):
            if doc_clima.upper().endswith('.WHT') and cod_clima.upper() in doc_clima.upper():
                with open(os.path.join(dir_DSSAT, 'Weather', doc_clima)) as (d):
                    doc = d.readlines()
                    símismo.decodar(doc)
                encontrado = True

        if not encontrado:
            print('Error: El código de estación de clima no se ubica en la base de datos de DSSAT.')
            return False

    def escribir(símismo):
        cod_clim = símismo.dic['INSI'] + 'TKON'
        for i in símismo.dic:
            if not len(símismo.dic[i]):
                símismo.dic[i] = [
                 '-99']

        with open('FILEW.txt', 'r') as (d):
            esquema = d.readlines()
        esquema.append('\n')
        esquema = símismo.encodar(esquema)
        esquema = ''.join(esquema)
        with open(os.path.join(dir_DSSAT, 'Weather', cod_clim, '.WTH'), 'w') as (d):
            d.write(''.join(esquema))

    def decodar(símismo, doc):
        for línea in doc:
            if '*' in línea:
                if 'WEATHER DATA' in línea:
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
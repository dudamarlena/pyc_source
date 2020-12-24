# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Controles.py
# Compiled at: 2017-03-27 11:26:23
# Size of source mod 2**32: 1175 bytes
import os.path, json
from pkg_resources import resource_filename
directorio_base = os.path.dirname(__file__)
dir_proyectos = os.path.join(directorio_base, 'Proyectos')
archivo_ctrls = resource_filename('tikon', 'controles.json')
with open(archivo_ctrls, 'r', encoding='utf8') as (doc):
    dic_ctrls = json.load(doc)
dirs_modelos = dic_ctrls['dirs_mods_cult']

def espec_dir_modelo_cult(modelo, directorio):
    if modelo not in dirs_modelos.keys():
        raise ValueError('Modelo "{}" no reconocido.'.format(modelo))
    else:
        if os.path.exists(directorio):
            dirs_modelos[modelo] = directorio
            with open(archivo_ctrls, 'w', encoding='utf8') as (d):
                json.dump(dic_ctrls, d, ensure_ascii=False, sort_keys=True, indent=2)
        else:
            raise ValueError('El directorio especificado ("{}") no existe.'.format(directorio))
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\__init__.py
# Compiled at: 2017-10-26 14:08:56
# Size of source mod 2**32: 1367 bytes
import json, os.path
from warnings import warn as avisar
from pkg_resources import resource_filename
__author__ = 'Julien Malard'
__email__ = 'julien.malard@mail.mcgill.ca'
with open(resource_filename('tikon', 'versión.txt')) as (archivo_versión):
    versión = archivo_versión.read().strip()
__version__ = versión
archivo_ctrls = resource_filename('tikon', 'controles.json')
with open(archivo_ctrls, 'r', encoding='utf8') as (d):
    dic_ctrls = json.load(d)
dirs_modelos = dic_ctrls['dirs_mods_cult']
dirs_auto = {'DSSAT': 'C:\\DSSAT46'}
mods_faltan = []
ctrls_cambiados = False
for mod in dirs_modelos:
    if not os.path.exists(dirs_modelos[mod]):
        if mod in dirs_auto:
            if os.path.exists(dirs_auto[mod]):
                dirs_modelos[mod] = dirs_auto[mod]
                ctrls_cambiados = True
        mods_faltan.append(mod)

if ctrls_cambiados:
    with open(archivo_ctrls, 'w', encoding='utf8') as (d):
        json.dump(dic_ctrls, d, ensure_ascii=False, sort_keys=True, indent=2)
if len(mods_faltan):
    avisar("Directorios no encontrados para los modelos de cultivo %s. No se pueden usar estos modelos de cultivos en esta sesión de Tiko'n." % ', '.join(mods_faltan))
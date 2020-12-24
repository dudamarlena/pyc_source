# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/factotum/newmap.py
# Compiled at: 2017-01-20 23:06:59
# Size of source mod 2**32: 1273 bytes
"""
This is the newmap module.
Calling this will make a new map in FACTORIOPATH/saves/Headless-YYMMDD-HHMMSS.zip

"""
import os, codecs, json, subprocess, datetime
from .factoriopath import getFactorioPath

def newFactorioMap():
    FACTORIOPATH = getFactorioPath()
    mapFileExamplePath = '%s/data/map-gen-settings.example.json' % FACTORIOPATH
    mapFilePath = '%s/config/mapsettings.json' % FACTORIOPATH
    if not os.path.isfile(mapFilePath):
        with codecs.open(mapFileExamplePath, 'r', encoding='utf-8') as (map_file):
            mapJson = json.load(map_file)
            mapJson['starting_area'] = 'very-high'
            for control in mapJson['autoplace_controls']:
                mapJson['autoplace_controls'][control]['size'] = 'high'
                mapJson['autoplace_controls'][control]['richness'] = 'very-high'
                mapJson['autoplace_controls'][control]['frequency'] = 'low'

        with codecs.open(mapFilePath, 'w', encoding='utf-8') as (map_file):
            json.dump(mapJson, map_file, indent=4)
    print(subprocess.check_output([
     '%s/bin/x64/factorio' % FACTORIOPATH,
     '--create', '%s/saves/%s' % (FACTORIOPATH, 'Headless-{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now())),
     '--map-gen-settings', '%s/config/mapsettings.json' % FACTORIOPATH]).decode('unicode_escape'))
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/geoserver/geoserver_test.py
# Compiled at: 2014-08-04 05:19:09
from pgeo.geoserver.geoserver import Geoserver
from pgeo.config.settings import settings
from pgeo.utils import log
from pgeo.error.custom_exceptions import PGeoException
import sys, random
log = log.logger('pgeo.geoserver.geoserver_test')
g = Geoserver(settings['geoserver'])
randomName = random.random()
name = 'test' + str(randomName).replace('.', '')
layer_to_publish = {'name': name, 
   'title': 'MODIS iuhadiuh', 
   'description': 'MODIS iuhadiuh', 
   'workspace': 'fenix', 
   'path': '/home/vortex/Desktop/LAYERS/MODIS/AB_NDVI_4326.tif'}
try:
    if g.publish_coveragestore(layer_to_publish, True):
        log.info('upload done')
    else:
        log.error('not uploaded')
except PGeoException as e:
    log.error(e)
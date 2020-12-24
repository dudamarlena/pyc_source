# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/gis/gdal_calc_test.py
# Compiled at: 2014-08-06 10:27:53
from pgeo.gis import gdal_calc
files_path = [
 '/home/vortex/Desktop/LAYERS/TRMM/Rainfall_06_2014.tif', '/home/vortex/Desktop/LAYERS/TRMM/Rainfall_05_2014.tif']
outputfile = '/home/vortex/Desktop/result_last_sum2.tif'
print 'Created (%s) layer %s' % (gdal_calc.calc_layers(files_path, outputfile, 'sum'), outputfile)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/godber/.virtualenvs/gdal_pds/lib/python2.7/site-packages/gdal_pds/__init__.py
# Compiled at: 2015-03-05 08:52:09
import numpy as np
try:
    from osgeo import gdal
except ImportError:
    import gdal

from gdal_pds import label

class PDSImage(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.label = label.read(self.filepath)
        self._gdal_img = gdal.Open(filepath)
        self.num_bands = self._gdal_img.RasterCount

    @property
    def image(self):
        """
        Returns the band data as a stacked Numpy Array
        """
        band_data_array = None
        for band in range(1, self.num_bands + 1):
            band_data = self._gdal_img.GetRasterBand(band).ReadAsArray()
            if band == 1:
                band_data_array = band_data
            else:
                band_data_array = np.dstack((band_data_array, band_data))

        return band_data_array
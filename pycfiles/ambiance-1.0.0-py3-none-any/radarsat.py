# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ambhas/radarsat.py
# Compiled at: 2012-11-13 06:12:06
__doc__ = '\nCreated on Sat Oct  9 17:06:59 2010\nby taking help from\nhttp://benjamindeschamps.ca/blog/2009/11/12/processing-radarsat-2-imagery-reading-raw-data-and-saving-rgb-composites/\n@author: sat kumar tomer\n'
import numpy, math
from osgeo import gdal
from xml.dom import minidom
import scipy.signal

class calibrate:
    """
    radar_in_dir = '/home/tomer/radarsat' # directory of the product.xml file
    radar_file = radar.calibrate(radar_in_dir)
    radar_file.speckle_filter('median',7)
    radar_file.speckle_filter('wiener',7)
    
    radar_out_file = '/home/tomer/radarsat/product.tif'
    radar_file.save_tiff(radar_out_file)
    """

    def __init__(self, inpath):
        self.inpath = inpath
        dataset = gdal.Open('RADARSAT_2_CALIB:SIGMA0:' + inpath + 'product.xml')
        self.geotransform = dataset.GetGeoTransform()
        self.gcps = dataset.GetGCPs()
        self.gcpproj = dataset.GetGCPProjection()
        self.RasterXSize = dataset.RasterXSize
        self.RasterYSize = dataset.RasterYSize
        S_HH = dataset.GetRasterBand(1).ReadAsArray()
        S_HV = dataset.GetRasterBand(3).ReadAsArray()
        S_VH = dataset.GetRasterBand(4).ReadAsArray()
        S_VV = dataset.GetRasterBand(2).ReadAsArray()
        S_HH_ABS = numpy.absolute(S_HH)
        S_HV_ABS = numpy.absolute(S_HV)
        S_VH_ABS = numpy.absolute(S_VH)
        S_VV_ABS = numpy.absolute(S_VV)
        self.SigmaHH = 20 * numpy.log10(S_HH_ABS)
        self.SigmaHV = 20 * numpy.log10(S_HV_ABS)
        self.SigmaVH = 20 * numpy.log10(S_VH_ABS)
        self.SigmaVV = 20 * numpy.log10(S_VV_ABS)

    def speckle_filter(self, filter_name, ws):
        if filter_name == 'median':
            self.SigmaHH = scipy.signal.medfilt2d(self.SigmaHH, kernel_size=ws)
            self.SigmaHV = scipy.signal.medfilt2d(self.SigmaHV, kernel_size=ws)
            self.SigmaVH = scipy.signal.medfilt2d(self.SigmaVH, kernel_size=ws)
            self.SigmaVV = scipy.signal.medfilt2d(self.SigmaVV, kernel_size=ws)
        elif filter_name == 'wiener':
            self.SigmaHH = scipy.signal.wiener(self.SigmaHH, mysize=(ws, ws), noise=None)
            self.SigmaHV = scipy.signal.wiener(self.SigmaHV, mysize=(ws, ws), noise=None)
            self.SigmaVH = scipy.signal.wiener(self.SigmaVH, mysize=(ws, ws), noise=None)
            self.SigmaVV = scipy.signal.wiener(self.SigmaVV, mysize=(ws, ws), noise=None)
        else:
            print 'the name of filter not understood'
        return

    def save_tiff(self, outfile_sigma):
        driver = gdal.GetDriverByName('GTiff')
        output_dataset = driver.Create(outfile_sigma, self.RasterXSize, self.RasterYSize, 4, gdal.GDT_Float32)
        output_dataset.SetGeoTransform(self.geotransform)
        output_dataset.SetGCPs(self.gcps, self.gcpproj)
        output_dataset.GetRasterBand(1).WriteArray(self.SigmaHH, 0, 0)
        output_dataset.GetRasterBand(2).WriteArray(self.SigmaHV, 0, 0)
        output_dataset.GetRasterBand(3).WriteArray(self.SigmaVH, 0, 0)
        output_dataset.GetRasterBand(4).WriteArray(self.SigmaVV, 0, 0)
        output_dataset = None
        return

    def incidence_angle(self, outfile_ia):
        xmldoc = minidom.parse(self.inpath + 'lutSigma.xml')
        SigmaGains = xmldoc.getElementsByTagName('gains')
        SigmaGains = SigmaGains[0].toxml()
        SigmaGains = SigmaGains[7:-8]
        SigmaGains = SigmaGains.split(' ')
        xmldoc = minidom.parse(self.inpath + 'lutBeta.xml')
        BetaGains = xmldoc.getElementsByTagName('gains')
        BetaGains = BetaGains[0].toxml()
        BetaGains = BetaGains[7:-8]
        BetaGains = BetaGains.split(' ')
        IncidenceAngle = numpy.zeros([self.RasterYSize, self.RasterXSize])
        for i in range(IncidenceAngle.shape[0]):
            for j in range(IncidenceAngle.shape[1]):
                IncidenceAngle[(i, j)] = math.asin((float(BetaGains[j]) / float(SigmaGains[j])) ** 2)

        driver = gdal.GetDriverByName('GTiff')
        output_IA = driver.Create(outfile_ia, self.RasterXSize, self.RasterYSize, 1, gdal.GDT_Float32)
        output_IA.SetGeoTransform(self.geotransform)
        output_IA.SetGCPs(self.gcps, self.gcpproj)
        output_IA.GetRasterBand(1).WriteArray(IncidenceAngle, 0, 0)
        output_IA = None
        return
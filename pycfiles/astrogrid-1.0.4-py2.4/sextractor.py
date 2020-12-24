# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/examples/sextractor.py
# Compiled at: 2008-03-31 10:25:20
"""
Run SExtractor on an image.

Demonstrates how to remotely run a task and retrieve the results.

"""
__id__ = '$Id$'
import time, urllib
from astrogrid import acr
from astrogrid import Applications, MySpace
print ''
print 'Start Aladin if you want to see the extracted catalogue on top of the image...'
print ''
acr.login()
image = 'http://help.astrogrid.org/raw-attachment/wiki/Help/IntroScripting/AstrogridPython/image.fits'
config = '\n#-------------------------------- Catalog ------------------------------------\n\nCATALOG_NAME\ttest.cat\t# name of the output catalog\nCATALOG_TYPE\tASCII_HEAD\t# "NONE","ASCII_HEAD","ASCII","FITS_1.0"\n\t\t\t\t# "FITS_LDAC" or "ASCII_SKYCAT"\n\nPARAMETERS_NAME\tint-wfs.param\t\n                                # name of the file containing catalog contents\n\n#------------------------------- Extraction ----------------------------------\n\nDETECT_TYPE\tCCD\t\t# "CCD" or "PHOTO" (*)\n#FLAG_IMAGE\tflag    \t# filename for an input FLAG-image\nDETECT_MINAREA\t3\t\t# minimum number of pixels above threshold\nDETECT_THRESH\t5.0\t\t# <sigmas> or <threshold>,<ZP> in mag.arcsec-2\nANALYSIS_THRESH\t5.0\t\t# <sigmas> or <threshold>,<ZP> in mag.arcsec-2\n\nFILTER\t\tY\t\t# apply filter for detection ("Y" or "N")?\nFILTER_NAME\tgauss_4.0_7x7.conv\t\n                                # name of the file containing the filter\n\nDEBLEND_NTHRESH\t32\t\t# Number of deblending sub-thresholds\nDEBLEND_MINCONT\t0.005\t\t# Minimum contrast parameter for deblending\n\nCLEAN\t\tY\t\t# Clean spurious detections? (Y or N)?\nCLEAN_PARAM\t1.0\t\t# Cleaning efficiency\n\nMASK_TYPE\tCORRECT\t\t# type of detection MASKing: can be one of\n\t\t\t\t# "NONE", "BLANK" or "CORRECT"\n\n#------------------------------ Photometry -----------------------------------\n\nPHOT_APERTURES\t3.5, 7.0, 9.9, 14.0, 19.8\t# MAG_APER aperture diameter(s) in pixels\nPHOT_AUTOPARAMS\t2.5, 3.5\t# MAG_AUTO parameters: <Kron_fact>,<min_radius>\n\nSATUR_LEVEL\t50000.0\t\t# level (in ADUs) at which arises saturation\n\nMAG_ZEROPOINT\t0.0\t\t# magnitude zero-point\nMAG_GAMMA\t4.0\t\t# gamma of emulsion (for photographic scans)\nGAIN\t\t1.0\t\t# detector gain in e-/ADU.\nPIXEL_SCALE\t0.333\t\t# size of pixel in arcsec (0=use FITS WCS info).\n\n#------------------------- Star/Galaxy Separation ----------------------------\n\nSEEING_FWHM\t1.2\t\t# stellar FWHM in arcsec\nSTARNNW_NAME\tdefault.nnw\t\n                                # Neural-Network_Weight table filename\n\n#------------------------------ Background -----------------------------------\n\nBACK_SIZE\t64\t\t# Background mesh: <size> or <width>,<height>\nBACK_FILTERSIZE\t3\t\t# Background filter: <size> or <width>,<height>\n\nBACKPHOTO_TYPE\tGLOBAL\t\t# can be "GLOBAL" or "LOCAL" (*)\nBACKPHOTO_THICK\t24\t\t# thickness of the background LOCAL annulus (*)\n\n#------------------------------ Check Image ----------------------------------\n\nCHECKIMAGE_TYPE\tNONE\t\t# can be one of "NONE", "BACKGROUND",\n\t\t\t\t# "MINIBACKGROUND", "-BACKGROUND", "OBJECTS",\n\t\t\t\t# "-OBJECTS", "SEGMENTATION", "APERTURES",\n\t\t\t\t# or "FILTERED" (*)\n#CHECKIMAGE_NAME\tcheck\t# Filename for the check-image (*)\n\n#--------------------- Memory (change with caution!) -------------------------\n\nMEMORY_OBJSTACK\t2000\t\t# number of objects in stack\nMEMORY_PIXSTACK\t100000\t\t# number of pixels in stack\nMEMORY_BUFSIZE\t1024\t\t# number of lines in buffer\n\n#----------------------------- Miscellaneous ---------------------------------\n\nVERBOSE_TYPE\tNORMAL\t\t# can be "QUIET", "NORMAL" or "FULL" (*)\n'
params = 'NUMBER\nX_WORLD\nY_WORLD\nX_IMAGE\nY_IMAGE\nMAG_ISO\nMAGERR_ISO\nMAG_AUTO\nMAGERR_AUTO\nCLASS_STAR\n'
filter = "CONV NORM\n# 3x3 ``all-ground'' convolution mask with FWHM = 2 pixels.\n1 2 1\n2 4 2\n1 2 1\n"
m = MySpace()
m.savefile(image, '#sextractor/image.fits')
id = 'ivo://org.astrogrid/SExtractor'
app = Applications(id)
app.inputs['ANALYSIS_THRESH']['value'] = 1.5
app.inputs['IMAGE_BAND']['value'] = 'R'
app.inputs['MAG_ZEROPOINT']['value'] = 25.0
app.inputs['SEEING_FWHM']['value'] = 1.2
app.inputs['PARAMETERS_NAME']['value'] = params
app.inputs['FILTER_NAME']['value'] = filter
app.inputs['config_file']['value'] = config
app.inputs['DetectionImage']['value'] = '#sextractor/image.fits'
app.inputs['PhotoImage']['value'] = '#sextractor/image.fits'
app.outputs['CATALOG_NAME']['value'] = '#sextractor/image_cat.fits'
task = app.submit()
time.sleep(10)
while task.status() != 'COMPLETED':
    time.sleep(10)
    print 'Status: ', task.status()

print task.status()
print task.results()
print 'Catalogue written to\n%s' % task.results()
acr.startplastic()
acr.plastic.broadcast('#sextractor/image.fits')
acr.plastic.broadcast('#sextractor/image_cat.fits')
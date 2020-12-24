# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\winpython\python-2.7.9.amd64\lib\site-packages\pySAXS\guisaxs\qt\pyFAICalibStart.py
# Compiled at: 2015-04-29 04:16:28
from guidata.dataset.dataitems import FileOpenItem, BoolItem, ButtonItem
from pyFAI.calibration import calib
import fabio, guidata, guidata.dataset.dataitems as di, guidata.dataset.datatypes as dt, os, pyFAI, pyFAI.calibrant, pyFAI.detectors
_app = guidata.qapplication()

class Processing(dt.DataSet):
    """Calib Start program"""
    calibrants = pyFAI.calibrant.ALL_CALIBRANTS.keys()
    list_Calibrants = list(calibrants)
    list_Calibrants.sort()
    detectors = pyFAI.detectors.ALL_DETECTORS.keys()
    list_Detectors = list(detectors)
    list_Detectors.sort()
    waveLength = di.FloatItem('Wavelength (A) : ', '0.709')
    detector = type = di.ChoiceItem('Detectors', list_Detectors)
    calibrant = type = di.ChoiceItem('Calibrants', list_Calibrants)
    fname = FileOpenItem('File :', ('tiff', 'edf', '*'))
    polarization = di.StringItem('Polarization : ', default=None)
    distance = di.StringItem('Distance (mm) : ', default=None)
    fix_distance = BoolItem('fix distance')
    notilt = BoolItem('No Tilt')


param = Processing()
if param.edit():
    cmd = 'pyFAI-calib.py '
    cmd += '-w ' + str(param.waveLength)
    cmd += ' -D ' + param.list_Detectors[param.detector]
    if param.notilt:
        cmd += ' --no-tilt'
    if param.polarization != '':
        cmd += ' -P ' + param.polarization
    if param.distance != '':
        cmd += ' -l ' + param.distance
    if param.fix_distance:
        cmd += ' --fix-dist'
    cmd += ' "' + param.fname + '"'
    print cmd
    os.system(cmd)
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/essai/lib/python2.7/site-packages/kernel/__init__.py
# Compiled at: 2016-03-24 06:20:11
__doc__ = '\nKernel module\n@summary: Contains all the routines necessary to the wavelet analysis<br />\n          of along-track altimetry data, and to compute diagnostics from it.\n@author: Renaud DUSSURGET, LER/PAC IFREMER.\n@change: Create in November 2012 by RD.\n@copyright: Renaud Dussurget 2012.\n@license: GNU Lesser General Public License\n    \n    This file is part of PyAltiWAVES.\n    \n    PyAltiWAVES is free software: you can redistribute it and/or modify it under\n    the terms of the GNU Lesser General Public License as published by the Free\n    Software Foundation, either version 3 of the License, or (at your option)\n    any later version.\n    PyAltiWAVES is distributed in the hope that it will be useful, but WITHOUT\n    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or\n    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License\n    for more details.\n    \n    You should have received a copy of the GNU Lesser General Public License along\n    with PyAltiWAVES.  If not, see <http://www.gnu.org/licenses/>.\n'
from runAnalysis import runAnalysis
from external import wavelet
from detectEddies import detection
from getScales import get_characteristics, eddy_amplitude, cyclone
from spectrum import spectral_analysis, periodogram_analysis
from bins import bin_space, bin_time
from io import save_analysis, save_detection, save_binning
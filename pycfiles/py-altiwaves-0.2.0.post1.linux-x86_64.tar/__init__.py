# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rdussurget/.virtualenvs/essai/lib/python2.7/site-packages/kernel/__init__.py
# Compiled at: 2016-03-24 06:20:11
"""
Kernel module
@summary: Contains all the routines necessary to the wavelet analysis<br />
          of along-track altimetry data, and to compute diagnostics from it.
@author: Renaud DUSSURGET, LER/PAC IFREMER.
@change: Create in November 2012 by RD.
@copyright: Renaud Dussurget 2012.
@license: GNU Lesser General Public License
    
    This file is part of PyAltiWAVES.
    
    PyAltiWAVES is free software: you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.
    PyAltiWAVES is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
    for more details.
    
    You should have received a copy of the GNU Lesser General Public License along
    with PyAltiWAVES.  If not, see <http://www.gnu.org/licenses/>.
"""
from runAnalysis import runAnalysis
from external import wavelet
from detectEddies import detection
from getScales import get_characteristics, eddy_amplitude, cyclone
from spectrum import spectral_analysis, periodogram_analysis
from bins import bin_space, bin_time
from io import save_analysis, save_detection, save_binning
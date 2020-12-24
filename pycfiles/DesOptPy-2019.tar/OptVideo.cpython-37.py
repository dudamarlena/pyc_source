# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/DesOptPy/DesOptPy/OptVideo.py
# Compiled at: 2017-05-04 20:05:59
# Size of source mod 2**32: 1258 bytes
"""
-------------------------------------------------------------------------------
Title:          OptVideo.py
Units:          Unitless
Date:           October 16, 2013
Author:         E.J. Wehrle
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description
-------------------------------------------------------------------------------
Optimization suite for Python...

TODO several videos for system responses
TODO check frames per second
TODO check codec
TODO is mencorder on cluster, master, workstations?
TODO integrate in file OptPostProc?
TODO save pngs in result folder? Yes!
-------------------------------------------------------------------------------
"""
from __future__ import absolute_import, division, print_function
import os

def OptVideo(OptName):
    fps = 4
    os.system("mencoder 'mf://DesVar***.png' -mf type=png:fps=" + str(fps) + ' -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o DesVar.mpg')
    os.system("mencoder 'mf://SysRes***.png' -mf type=png:fps=" + str(fps) + ' -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o SysRes.mpg')
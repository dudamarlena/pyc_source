# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/PythonCodes/gaeio\gaeio\__init__.py
# Compiled at: 2020-04-25 14:16:44
# Size of source mod 2**32: 1368 bytes
from __future__ import absolute_import, division, print_function
__version__ = '1.0'
__all__ = [
 'basic', 'core', 'vis', 'seismic', 'psseismic', 'horizon', 'pointset', 'gui',
 'start']
import os, sys
sys.path.append(os.path.dirname(__file__)[:-6])
import gaeio.src.basic as basic, gaeio.src.core as core, gaeio.src.vis as vis, gaeio.src.seismic as seismic, gaeio.src.psseismic as psseismic, gaeio.src.horizon as horizon, gaeio.src.pointset as pointset, gaeio.src.gui as gui

def start(path=os.path.dirname(__file__)):
    """
    Start the GUI
    Args:
        path: starting path. Default is the package.
    Return:
        N/A
    """
    gui.start(startpath=path)


if __name__ == '__main__':
    start()
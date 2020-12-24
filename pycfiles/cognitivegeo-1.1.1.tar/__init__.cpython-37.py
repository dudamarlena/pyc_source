# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\__init__.py
# Compiled at: 2019-12-30 18:22:51
# Size of source mod 2**32: 1278 bytes
from __future__ import absolute_import, division, print_function
__version__ = '1.1'
__all__ = [
 'basic', 'core', 'vis', 'seismic', 'psseismic', 'pointset', 'gui']
import os, sys
sys.path.append(os.path.dirname(__file__)[:-13])
import cognitivegeo.src.basic as basic
import cognitivegeo.src.core as core
import cognitivegeo.src.vis as vis
import cognitivegeo.src.seismic as seismic
import cognitivegeo.src.psseismic as psseismic
import cognitivegeo.src.pointset as pointset
import cognitivegeo.src.gui as gui
if __name__ == '__main__':
    gui.start(startpath=(os.path.dirname(__file__)))
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\__init__.py
# Compiled at: 2019-12-30 18:22:51
# Size of source mod 2**32: 1278 bytes
from __future__ import absolute_import, division, print_function
__version__ = '1.1'
__all__ = [
 'basic', 'core', 'vis', 'seismic', 'psseismic', 'pointset', 'gui']
import os, sys
sys.path.append(os.path.dirname(__file__)[:-13])
import cognitivegeo.src.basic as basic, cognitivegeo.src.core as core, cognitivegeo.src.vis as vis, cognitivegeo.src.seismic as seismic, cognitivegeo.src.psseismic as psseismic, cognitivegeo.src.pointset as pointset, cognitivegeo.src.gui as gui
if __name__ == '__main__':
    gui.start(startpath=(os.path.dirname(__file__)))
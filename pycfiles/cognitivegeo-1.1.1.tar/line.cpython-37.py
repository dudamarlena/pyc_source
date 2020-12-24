# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\vis\line.py
# Compiled at: 2019-12-13 22:46:40
# Size of source mod 2**32: 1201 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.vis.color as color
__all__ = [
 'line']
LineStyleList = [
 'Solid', 'Dashed', 'Dashdot', 'Dotted', 'None']
LineWidthList = [i for i in range(1, 20)]

class line:
    LineStyleList = LineStyleList
    LineWidthList = LineWidthList
    LineColorList = color.ColorList
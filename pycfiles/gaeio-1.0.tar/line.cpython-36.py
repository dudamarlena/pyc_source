# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\gaeio\src\vis\line.py
# Compiled at: 2020-04-25 14:33:31
# Size of source mod 2**32: 1098 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.color import color
__all__ = [
 'line']
LineStyleList = [
 'Solid', 'Dashed', 'Dashdot', 'Dotted', 'None']
LineWidthList = [i for i in range(1, 20)]

class line:
    LineStyleList = LineStyleList
    LineWidthList = LineWidthList
    LineColorList = color.ColorList
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\vis\marker.py
# Compiled at: 2019-12-13 22:46:40
# Size of source mod 2**32: 1249 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.vis.color as color
__all__ = [
 'marker']
MarkerStyleList = [
 '*', '+', 'o', 'v', '^', '<', '<',
 'x', 'X', '.', 'None']
MarkerSizeList = [i for i in range(1, 20)]

class marker:
    MarkerStyleList = MarkerStyleList
    MarkerSizeList = MarkerSizeList
    MarkerColorList = color.ColorList
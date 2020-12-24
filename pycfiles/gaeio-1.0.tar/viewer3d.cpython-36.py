# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\gaeio\src\vis\viewer3d.py
# Compiled at: 2020-04-25 14:33:31
# Size of source mod 2**32: 1103 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.core.keyboard import keyboard as core_key
__all__ = [
 'viewer3d']
GoHomeKeyList = core_key.LetterKeyList
ViewFromPropertyList = [
 'Inline', 'Crossline', 'Z']
ViewFromKeyList = core_key.LetterKeyList

class viewer3d:
    GoHomeKeyList = GoHomeKeyList
    ViewFromPropertyList = ViewFromPropertyList
    ViewFromKeyList = ViewFromKeyList
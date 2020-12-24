# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\vis\viewer3d.py
# Compiled at: 2019-12-13 22:46:40
# Size of source mod 2**32: 1206 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.keyboard as core_key
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
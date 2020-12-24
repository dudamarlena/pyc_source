# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\vis\player.py
# Compiled at: 2019-12-13 22:46:40
# Size of source mod 2**32: 1347 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.keyboard as core_key
__all__ = [
 'player']
PlayerPropertyList = [
 'First', 'Previous', 'Backward', 'Pause', 'Forward', 'Next', 'Last', 'Interval']
PlayerKeyList = core_key.LetterKeyList
PlayerIntervalList = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]

class player:
    PlayerPropertyList = PlayerPropertyList
    PlayerKeyList = PlayerKeyList
    PlayerIntervalList = PlayerIntervalList
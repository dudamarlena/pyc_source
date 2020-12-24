# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\vis\player.py
# Compiled at: 2019-12-13 22:46:40
# Size of source mod 2**32: 1347 bytes
import sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.keyboard import keyboard as core_key
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
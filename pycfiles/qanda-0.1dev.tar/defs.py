# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: qanda/defs.py
# Compiled at: 2011-06-23 06:23:18
"""
Various module-wide constants.
"""
import re
__all__ = [
 'SPACE_RE',
 'YESNO_SYNONYMS']
SPACE_RE = re.compile('\\s+')
ANSWER_YES = 'y'
ANSWER_NO = 'n'
YESNO_SYNONYMS = {'yes': 'y', 
   'no': 'n', 
   'true': 'y', 
   'false': 'n', 
   'on': 'y', 
   'off': 'n'}
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Py-konval/konval/konval/defs.py
# Compiled at: 2011-07-21 10:24:16
"""
Various module-wide constants.

"""
__docformat__ = 'restructuredtext en'
import re
__all__ = [
 'TRUE_FALSE_DICT',
 'CANON_SPACE_RE']
TRUE_STRS = [
 'TRUE',
 'T',
 'ON',
 'YES',
 'Y',
 '+',
 '1',
 1]
FALSE_STRS = [
 'FALSE',
 'F',
 'OFF',
 'NO',
 'N',
 '-',
 '0',
 0]
TRUE_FALSE_DICT = {}
for v in TRUE_STRS:
    TRUE_FALSE_DICT[v] = True

for v in FALSE_STRS:
    TRUE_FALSE_DICT[v] = False

CANON_SPACE_RE = re.compile('[\\-_\\s]+')
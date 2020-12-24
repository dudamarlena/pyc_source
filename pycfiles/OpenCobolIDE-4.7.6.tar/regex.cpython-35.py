# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.cobol/pyqode/cobol/api/regex.py
# Compiled at: 2016-12-29 05:32:02
# Size of source mod 2**32: 940 bytes
"""
This module contains the various regular expressions used through the whole
project.

"""
from pyqode.qt import QtCore
STRUCT_PATTERN = QtCore.QRegExp('((^|^\\s*)\\d\\d [\\w\\-]+\\.$)')
PARAGRAPH_PATTERN = QtCore.QRegExp('((^|^\\s*)\\.?[\\w\\-]+\\.\\s*$)')
LOOP_PATTERN = QtCore.QRegExp('(^|^\\s)PERFORM.*(VARYING|UNTIL|TIMES|WITH|TEST|AFTER)*')
BRANCH_START = QtCore.QRegExp('((^|\\s)IF\\b|ELSE)')
BRANCH_END = QtCore.QRegExp('END-(PERFORM|IF|READ)\\.?')
DIVISION = QtCore.QRegExp('.*\\s+DIVISION.*\\.*')
SECTION = QtCore.QRegExp('.*\\s+SECTION.*\\.*')
VAR_PATTERN = QtCore.QRegExp('\\s*\\d+\\s.*.+')
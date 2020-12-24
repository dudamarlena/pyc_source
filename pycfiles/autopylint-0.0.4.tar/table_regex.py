# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/table_regex.py
# Compiled at: 2018-01-10 14:39:00
"""
Regexes used for the editor's table
"""
import re
MODULE_NAME = re.compile('\n    ^\\*+\\s\n    Module\\s+\n    (?P<filename>[\\w\\d\\._-]+)\n    $\n', re.VERBOSE)
PYLINT_ITEM = re.compile("\n    ^\n    (?P<type>[ERCW]):\n    \\s*\n    (?P<where1>\\d+),\n    \\s*\n    (?P<where2>-?\\d+):\n    \\s+\n    (?P<desc>[\\w\\d\\s\\.\\(\\)/',]+?)\n    \\s\n    \\(\n    (?P<error>[\\w_\\.-]+?)\n    \\)\n    $\n", re.VERBOSE)
PYLINT_SEMI_ITEM = re.compile('\n    ^\n    (?P<type>[ERCW]):\n    \\s*\n    (?P<where1>\\d+),\n    \\s*\n    (?P<where2>-?\\d+):\n    \\s+\n    (?P<desc>[\\w\\d\\s\\.\\(\\)/]+?)\n    $\n', re.VERBOSE)
PYLINT_ERROR_ITEM = re.compile('\n    ^\n    [\\^\\s\\|]+\n    \\(\n    (?P<error>[\\w_\\.-]+)\n    \\)\n    $\n', re.VERBOSE)
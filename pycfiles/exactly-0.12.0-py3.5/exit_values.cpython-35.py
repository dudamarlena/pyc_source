# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/exit_values.py
# Compiled at: 2018-05-11 22:17:20
# Size of source mod 2**32: 299 bytes
from exactly_lib.common.exit_value import ExitValue
from exactly_lib.util.ansi_terminal_color import ForegroundColor
ALL_PASS = ExitValue(0, 'OK', ForegroundColor.GREEN)
INVALID_SUITE = ExitValue(3, 'INVALID_SUITE', ForegroundColor.YELLOW)
FAILED_TESTS = ExitValue(4, 'ERROR', ForegroundColor.RED)
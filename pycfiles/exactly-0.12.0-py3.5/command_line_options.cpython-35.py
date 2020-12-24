# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/cli/definitions/program_modes/test_suite/command_line_options.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 273 bytes
from exactly_lib.util.cli_syntax import short_and_long_option_syntax
OPTION_FOR_REPORTER__LONG = 'reporter'
OPTION_FOR_REPORTER = short_and_long_option_syntax.long_syntax(OPTION_FOR_REPORTER__LONG)
REPORTER_OPTION_ARGUMENT = 'REPORTER'
TEST_SUITE_FILE_ARGUMENT = 'FILE'
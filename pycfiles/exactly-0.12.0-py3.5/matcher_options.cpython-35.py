# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/string_matcher/matcher_options.py
# Compiled at: 2020-01-31 11:01:50
# Size of source mod 2**32: 633 bytes
from exactly_lib.definitions import logic
from exactly_lib.definitions.primitives.file_or_dir_contents import EMPTINESS_CHECK_ARGUMENT
from exactly_lib.definitions.primitives.str_matcher import MATCH_REGEX_OR_GLOB_PATTERN_CHECK_ARGUMENT
from exactly_lib.util.cli_syntax.elements import argument as a
NOT_ARGUMENT = logic.NOT_OPERATOR_NAME
EMPTY_ARGUMENT = EMPTINESS_CHECK_ARGUMENT
EQUALS_ARGUMENT = 'equals'
MATCHES_ARGUMENT = MATCH_REGEX_OR_GLOB_PATTERN_CHECK_ARGUMENT
FULL_MATCH_ARGUMENT_OPTION = a.OptionName(long_name='full')
NUM_LINES_ARGUMENT = 'num-lines'
LINE_ARGUMENT = 'line'
NUM_LINES_DESCRIPTION = 'number of lines'
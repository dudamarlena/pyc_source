# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/cli_syntax/option_parsing.py
# Compiled at: 2018-04-20 07:05:01
# Size of source mod 2**32: 329 bytes
from exactly_lib.util.cli_syntax.elements.argument import OptionName
from exactly_lib.util.cli_syntax.option_syntax import long_option_syntax

def matches(option_name: OptionName, actual_argument_element: str) -> bool:
    option_syntax = long_option_syntax(option_name.long)
    return actual_argument_element == option_syntax
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/cli_syntax/option_syntax.py
# Compiled at: 2020-01-29 09:08:20
# Size of source mod 2**32: 691 bytes
from exactly_lib.util.cli_syntax.elements.argument import OptionName
OPTION_PREFIX_CHARACTER = '-'

def is_option_string(string: str) -> bool:
    return string and string[0] == OPTION_PREFIX_CHARACTER


def long_option_syntax(name: str) -> str:
    """
    Syntax for a long option.
    :param name: The option name without any "option" syntax prefix ("--).
    """
    return OPTION_PREFIX_CHARACTER + name


def option_syntax(option_name: OptionName) -> str:
    """
    Renders an :class:`OptionName`

    The long name is used if it exists.
    """
    if option_name.long:
        return long_option_syntax(option_name.long)
    raise ValueError('missing long option')
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/cli_syntax/short_and_long_option_syntax.py
# Compiled at: 2018-04-20 07:05:01
# Size of source mod 2**32: 714 bytes
from exactly_lib.util.cli_syntax.elements.argument import ShortAndLongOptionName

def short_syntax(character: str) -> str:
    """
    Syntax for a short option.
    :param character: The single option character.
    """
    return '-' + character


def long_syntax(name: str) -> str:
    """
    Syntax for a long option.
    :param name: The option name without any "option" syntax prefix ("--).
    """
    return '--' + name


def option_syntax(option_name: ShortAndLongOptionName) -> str:
    """
    Renders an :class:`OptionName`

    The long name is used if it exists.
    """
    if option_name.long:
        return long_syntax(option_name.long)
    else:
        return short_syntax(option_name.short)
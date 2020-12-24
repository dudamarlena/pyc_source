# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/cli/definitions/common_cli_options.py
# Compiled at: 2019-01-29 09:32:34
# Size of source mod 2**32: 998 bytes
from exactly_lib.definitions import instruction_arguments, misc_texts
from exactly_lib.util.cli_syntax import short_and_long_option_syntax
HELP_COMMAND = 'help'
SUITE_COMMAND = 'suite'
SYMBOL_COMMAND = 'symbol'
COMMAND_DESCRIPTIONS = {HELP_COMMAND: 'Help system (use "{} {}" for help on help.)'.format(HELP_COMMAND, HELP_COMMAND), 
 SUITE_COMMAND: '{} (use "{} {}" for help.)'.format(misc_texts.SUITE_COMMAND_SINGLE_LINE_DESCRIPTION, HELP_COMMAND, SUITE_COMMAND), 
 
 SYMBOL_COMMAND: '{} (use "{} {}" for help.)'.format(misc_texts.SYMBOL_COMMAND_SINGLE_LINE_DESCRIPTION, HELP_COMMAND, SYMBOL_COMMAND)}
SHELL_COMMAND = instruction_arguments.COMMAND_ARGUMENT.name
OPTION_FOR_ACTOR__LONG = 'actor'
OPTION_FOR_ACTOR = short_and_long_option_syntax.long_syntax(OPTION_FOR_ACTOR__LONG)
ACTOR_OPTION_ARGUMENT = SHELL_COMMAND
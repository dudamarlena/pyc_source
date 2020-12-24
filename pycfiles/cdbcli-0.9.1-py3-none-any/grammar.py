# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/src/cdbcli/build/lib/cdbcli/grammar.py
# Compiled at: 2016-07-12 22:52:21
from prompt_toolkit.contrib.regular_languages import compiler
from .commands import COMMANDS

def _build_pattern((command, operand_pattern)):
    command_pattern = command.replace(' ', '\\s')
    if operand_pattern:
        return ('(\\s*(?P<command>{command_pattern})\\s+{operand_pattern})').format(command_pattern=command_pattern, operand_pattern=operand_pattern)
    else:
        return ('(\\s*(?P<command>{command_pattern}))').format(command_pattern=command_pattern)


def _create_grammar():
    patterns = map(_build_pattern, [ (command, operand_pattern) for command, (_, operand_pattern) in COMMANDS.iteritems()
                                   ])
    patterns = ('|').join(patterns)
    return compiler.compile(patterns)


grammar = _create_grammar()
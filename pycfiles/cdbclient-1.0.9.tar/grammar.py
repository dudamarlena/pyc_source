# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
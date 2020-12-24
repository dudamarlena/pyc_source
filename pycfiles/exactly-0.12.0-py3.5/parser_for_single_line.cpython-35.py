# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/actors/util/executor_made_of_parts/parser_for_single_line.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 1631 bytes
import shlex
from typing import Sequence
from exactly_lib.actors.util.executor_made_of_parts.parts import ExecutableObjectParser
from exactly_lib.actors.util.source_code_lines_utils import all_source_code_lines
from exactly_lib.test_case.actor import ParseException
from exactly_lib.test_case.phases.act import ActPhaseInstruction
from exactly_lib.test_case.result import svh

class ParserForSingleLineUsingStandardSyntax(ExecutableObjectParser):
    __doc__ = '\n    A parser that fails if there is not one, and only one, line that is not\n    empty and not a comment.\n\n    :returns The single non-empty line\n    '

    def apply(self, instructions: Sequence[ActPhaseInstruction]) -> str:
        return _parse_single_line(instructions)


class ParserForSingleLineUsingStandardSyntaxSplitAccordingToShellSyntax(ExecutableObjectParser):
    __doc__ = '\n    A parser that fails if there is not one, and only one, line that is not\n    empty and not a comment.\n\n    :returns The single non-empty line, split according to shell syntax.\n    '

    def apply(self, instructions: Sequence[ActPhaseInstruction]) -> list:
        single_line = _parse_single_line(instructions)
        return shlex.split(single_line)


def _parse_single_line(instructions: Sequence[ActPhaseInstruction]) -> str:
    non_empty_lines = all_source_code_lines(instructions)
    if not non_empty_lines:
        raise ParseException(svh.new_svh_validation_error__str('No lines with source code found'))
    if len(non_empty_lines) > 1:
        raise ParseException(svh.new_svh_validation_error__str('More than one line with source code found'))
    return non_empty_lines[0]
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/actors/util/source_code_lines_utils.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 581 bytes
from typing import Sequence, List
from exactly_lib.section_document.syntax import is_empty_line, is_comment_line
from exactly_lib.test_case.phases.act import ActPhaseInstruction

def all_source_code_lines(instructions: Sequence[ActPhaseInstruction]) -> List[str]:
    ret_val = []
    for instruction in instructions:
        for line in instruction.source_code().lines:
            if _is_source_code_line(line):
                ret_val.append(line)

    return ret_val


def _is_source_code_line(line: str) -> bool:
    return not (is_empty_line(line) or is_comment_line(line))
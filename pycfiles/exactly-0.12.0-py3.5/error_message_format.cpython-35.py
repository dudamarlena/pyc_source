# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/err_msg/error_message_format.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 332 bytes
from typing import List
from exactly_lib.util.line_source import LineSequence

def source_lines(lines: LineSequence) -> str:
    return 'Line {}:\n\n{}'.format(lines.first_line.line_number, lines.text)


def source_line_sequence(source: LineSequence) -> List[str]:
    return list(source.lines)
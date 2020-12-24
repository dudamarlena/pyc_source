# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/line_matcher/model_construction.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1052 bytes
from typing import Iterator, Tuple
from exactly_lib.type_system.logic.line_matcher import LineMatcherLine

def model_iter_from_file_line_iter(lines: Iterator[str]) -> Iterator[LineMatcherLine]:
    """
    Gives a sequence of line matcher models, corresponding to input lines read from file.
    New lines are expected to appear only as last character of lines, or not at all, if
    last line is not ended with new line in the file.

    @:param strings: lines from an input source
    """
    return enumerate((l.rstrip('\n') for l in lines), 1)


def original_and_model_iter_from_file_line_iter(lines: Iterator[str]) -> Iterator[Tuple[(str, LineMatcherLine)]]:
    """
    Gives a sequence of pairs, corresponding to each element in lines.
    (original line, line-matcher-model-for-line).

    See also docs of model_iter_from_file_line_iter.

    @:param strings: lines from an input source
    """
    return ((original, (line_num, original.rstrip('\n'))) for line_num, original in enumerate(lines, 1))
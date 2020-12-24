# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/messages/expected_found.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 508 bytes
from exactly_lib.common.report_rendering import text_docs
from exactly_lib.common.report_rendering.text_doc import TextRenderer
_EXPECTED_HEADER = 'Expected : '
_FOUND_HEADER = 'Found    : '

def unexpected_lines(expected: str, found: str) -> TextRenderer:
    return text_docs.major_blocks_of_string_lines(unexpected_lines_str(expected, found))


def unexpected_lines_str(expected: str, found: str) -> str:
    return '\n'.join([
     _EXPECTED_HEADER + expected,
     _FOUND_HEADER + found])
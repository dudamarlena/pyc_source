# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/falign/falign.py
# Compiled at: 2020-03-14 19:14:54
# Size of source mod 2**32: 7238 bytes
"""faligning comments and variable declarations."""
from typing import List, Optional

class FAlign:
    __doc__ = 'Aligning comments and sometimes variable declarations.'

    def __init__(self, min_space_before_comment: int=1, comment_start_column: Optional[int]=None, ignore_offset: Optional[int]=None):
        self.min_space_before_comment = min_space_before_comment
        self.comment_start_column = comment_start_column
        self.ignore_offset = ignore_offset

    def falign(self, lines: List[str]) -> List[str]:
        """aligns input file and writes to output file."""
        output_lines = []
        block_slice = slice(None)
        while True:
            block_slice = self.next_block_slice(block_slice.stop, lines)
            if block_slice.start is None:
                break
            next_block_code_indent = None
            next_block_slice = block_slice
            while next_block_code_indent is None:
                next_block_slice = self.next_block_slice(next_block_slice.stop, lines)
                if next_block_slice.start is None:
                    break
                else:
                    next_block_code_indent = FAlign._code_indent(lines[next_block_slice])

            block = lines[block_slice]
            self._align_block_comments(block, next_block_code_indent)
            output_lines.extend(block)

        return output_lines

    def _align_block_comments(self, lines: List[str], next_block_code_indent: Optional[int]=None) -> None:
        to_align = []
        align_index = 0 if (self.comment_start_column is None or self.comment_start_column <= 0) else (self.comment_start_column - 1)
        for iline, line in enumerate(lines):
            comment_index = self._comment_index(line)
            if not comment_index is None:
                if comment_index == 0:
                    continue
                else:
                    code_length = len(line[:comment_index].rstrip())
                    if code_length + self.min_space_before_comment > align_index:
                        align_index = code_length + self.min_space_before_comment
                    if self._first_non_whitespace(lines[iline]) == '!':
                        code_indent = self._code_indent(lines[iline:])
                        if code_indent is None:
                            code_indent = next_block_code_indent
                        indent = code_indent if self.ignore_offset is None else code_indent + self.ignore_offset + 1
                        if code_indent is not None:
                            if 0 < comment_index < indent:
                                lines[iline] = ' ' * code_indent + lines[iline][comment_index:]
                                continue
                            else:
                                pass
                        if comment_index == code_indent:
                            continue
                to_align.append(iline)

        for iline in to_align:
            comment_index = self._comment_index(lines[iline])
            if not comment_index is None:
                if comment_index == 0:
                    continue
                comment = lines[iline][comment_index:]
                code = lines[iline][:comment_index].rstrip()
                code_length = len(code)
                lines[iline] = code + ' ' * (align_index - code_length) + comment

    @staticmethod
    def _code_indent(lines: List[str]) -> Optional[int]:
        """Gives the current indent of the current line of code, if the current
        line contains no code looks for the next line of code."""
        for iline, _ in enumerate(lines):
            if FAlign._is_empty(lines[iline]):
                continue
            inws = FAlign._first_non_whitespace_index(lines[iline])
            if inws is None:
                continue
            if lines[iline][inws] == '!':
                continue
            return inws

    @staticmethod
    def _comment_index(line: str) -> Optional[int]:
        string_delimiter = None
        for iline, _ in enumerate(line):
            char = line[iline]
            if string_delimiter:
                if char != string_delimiter:
                    continue
                elif string_delimiter and char == string_delimiter:
                    string_delimiter = None
                    continue
                if char in ("'", '"'):
                    string_delimiter = char
                    continue
                if char == '!':
                    return iline

    @staticmethod
    def _first_non_whitespace(line: str) -> Optional[str]:
        i = FAlign._first_non_whitespace_index(line)
        if i is None:
            return
        return line[i]

    @staticmethod
    def _first_non_whitespace_index(line: str) -> Optional[int]:
        for iline, _ in enumerate(line):
            if line[iline].strip():
                return iline

    @staticmethod
    def next_block_slice(current: Optional[int], lines: List[str]) -> slice:
        """Finds next block of code and includes leading and trailing empty
        lines."""
        if not current:
            start = 0
        else:
            if current < 0:
                start = 0
            else:
                start = current
        if current is not None:
            if current >= len(lines):
                return slice(None)
        end = start
        while end >= len(lines):
            return slice(start, end)
            if FAlign._is_empty(lines[end]):
                while 1:
                    if end >= len(lines):
                        return slice(start, end)
                    if not FAlign._is_empty(lines[end]):
                        return slice(start, end)
                        end = end + 1

            end = end + 1

    @staticmethod
    def _is_empty(string: str) -> bool:
        return not string.strip()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/libmotop/Block.py
# Compiled at: 2013-10-02 10:11:51
"""Imports for Python 3 compatibility"""
from __future__ import print_function
import sys

class Block:
    """Class to print blocks of ordered printables."""

    def __init__(self, columnHeaders):
        self.__columnHeaders = columnHeaders
        self.__columnWidths = [6] * len(self.__columnHeaders)

    def reset(self, lines):
        self.__lines = lines

    def __len__(self):
        return len(self.__lines)

    def __cell(self, value):
        if isinstance(value, tuple):
            return (' / ').join(self.__cell(value) for value in value)
        else:
            if value is not None:
                return str(value)
            return ''

    def __printLine(self, line, leftWidth, bold=False):
        """Print the cells separated by 2 spaces, cut the part after the width."""
        for (index, value) in enumerate(line):
            cell = self.__cell(value)
            if leftWidth < len(self.__columnHeaders[index]):
                break
            if index + 1 < len(line):
                self.__columnWidths[index] = max(len(cell) + 2, self.__columnWidths[index])
            if bold and sys.stdout.isatty():
                print('\x1b[1m', end='')
            print(cell.ljust(self.__columnWidths[index])[:leftWidth], end='')
            if bold and sys.stdout.isatty():
                print('\x1b[0m', end='')
            leftWidth -= self.__columnWidths[index]

        print()

    def print(self, height, width):
        """Print the lines, cut the ones after the height."""
        assert height > 1
        self.__printLine(self.__columnHeaders, width, True)
        height -= 1
        for line in self.__lines:
            if height <= 1:
                break
            assert len(line) <= len(self.__columnHeaders)
            height -= 1
            self.__printLine(line, width)
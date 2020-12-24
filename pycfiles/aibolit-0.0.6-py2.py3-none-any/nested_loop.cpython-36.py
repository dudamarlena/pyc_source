# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/patterns/nested_loop/nested_loop.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1704 bytes
from typing import List
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType

class NestedLoop:
    __doc__ = '\n    Returns lines in the file where\n    nested FOR/IF blocks are located\n    '

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        """Return line numbers in the file where patterns are found"""
        pattern = NestedBlocks(2, [
         BlockType.WHILE,
         BlockType.FOR,
         BlockType.DO])
        return pattern.value(filename)
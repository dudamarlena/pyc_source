# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/patterns/nested_loop/nested_loop.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1704 bytes
from typing import List
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType

class NestedLoop:
    """NestedLoop"""

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        """Return line numbers in the file where patterns are found"""
        pattern = NestedBlocks(2, [
         BlockType.WHILE,
         BlockType.FOR,
         BlockType.DO])
        return pattern.value(filename)
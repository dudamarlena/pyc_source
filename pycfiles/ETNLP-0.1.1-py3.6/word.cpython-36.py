# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/utils/word.py
# Compiled at: 2019-04-04 14:31:30
# Size of source mod 2**32: 508 bytes
from typing import List
from utils.vectors import Vector

class Word:
    __doc__ = 'A single word (one line of the input vector embedding file)'

    def __init__(self, text: str, vector: Vector, frequency: int) -> None:
        self.text = text
        self.vector = vector
        self.frequency = frequency

    def __repr__(self) -> str:
        vector_preview = ', '.join(map(str, self.vector[:2]))
        return f"{self.text} [{vector_preview}, ...]"
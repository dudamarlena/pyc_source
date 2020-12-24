# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\arcade_types.py
# Compiled at: 2020-03-29 13:19:22
# Size of source mod 2**32: 529 bytes
__doc__ = '\nModule specifying data custom types used for type hinting.\n'
from typing import Tuple
from typing import List
from typing import Union
from typing import Sequence
RGB = Union[(Tuple[(int, int, int)], List[int])]
RGBA = Union[(Tuple[(int, int, int, int)], List[int])]
Color = Union[(RGB, RGBA)]
Point = Union[(Tuple[(float, float)], List[float])]
Vector = Point
PointList = Sequence[Point]
Rect = Union[(Tuple[(float, float, float, float)], List[float])]
RectList = Union[(Tuple[(Rect, ...)], List[Rect])]
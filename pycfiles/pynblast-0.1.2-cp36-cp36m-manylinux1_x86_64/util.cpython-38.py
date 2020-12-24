# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/barnesc/work/code/nblast-rs/nblast-py/pynblast/util.py
# Compiled at: 2020-04-20 10:20:54
# Size of source mod 2**32: 1780 bytes
from typing import NewType
import enum, numpy as np

class StrEnum(str, enum.Enum):

    def __new__(cls, *args):
        for arg in args:
            if not isinstance(arg, (str, enum.auto)):
                raise TypeError('Values of StrEnums must be strings: {} is a {}'.format(repr(arg), type(arg)))
            return (super().__new__)(cls, *args)

    def __str__(self):
        return self.value

    def _generate_next_value_(name, *_):
        return name


Idx = NewType('Idx', int)

def raise_if_none(result, *idxs):
    if result is None:
        raise IndexError(f"Index(es) not in arena: {idxs}")
    return result


class Symmetry(StrEnum):
    """Symmetry"""
    ARITHMETIC_MEAN = 'arithmetic_mean'
    GEOMETRIC_MEAN = 'geometric_mean'
    HARMONIC_MEAN = 'harmonic_mean'
    MIN = 'min'
    MAX = 'max'


def rectify_tangents(orig: np.ndarray, inplace=False) -> np.ndarray:
    """Normalises orientation of tangents.

    Makes the first nonzero element positive.
    """
    if not inplace:
        orig = orig.copy()
    prev_zero = np.full((len(orig)), True, dtype=bool)
    for this_col in orig.T:
        to_flip = np.logical_and(prev_zero, this_col < 0)
        orig[to_flip, :] *= -1
        prev_zero = np.logical_and(prev_zero, this_col == 0)
        if not prev_zero.any():
            break
        return orig
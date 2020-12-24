# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/legaul/venv36/lib/python3.6/site-packages/minegauler/types.py
# Compiled at: 2020-01-02 18:47:19
# Size of source mod 2**32: 4945 bytes
"""
types.py - Type definitions

June 2018, Lewis Gaul

Exports:
CellContentsType (class)
    Base class for cell contents types.
CellMineType (class)
    Base class for cell contents of a mine type.
CellUnclicked, CellNum, CellMine, CellHitMine, CellFlag, CellwrongFlag (class)
    CellContentsType implementations.

GameState (Enum)
    The possible states of a game.

GameFlagMode (Enum)
    The possible flagging modes for a game.
"""
import enum, functools

class _NumericCellContentsMixin:
    __doc__ = '\n    A mixin for numeric cell contents types, allowing adding and subtracting integers.\n    '
    char: str

    def __init__(self, num):
        if not isinstance(num, int):
            raise TypeError('Number should be an integer')
        self.num = num

    def __repr__(self):
        return self.char + str(self.num)

    def __add__(self, obj):
        if type(obj) is not int:
            raise TypeError('Can only add integers to cell contents types')
        else:
            return self.__class__(self.num + obj)

    def __sub__(self, obj):
        if type(obj) is not int:
            raise TypeError('Can only subtract integers from cell contents types')
        else:
            return self.__class__(self.num - obj)


class CellContentsType:
    __doc__ = 'Abstract base class for contents of a minesweeper board cell.'
    char: str

    @functools.lru_cache(maxsize=None)
    def __new__(cls, *args):
        if cls == CellContentsType:
            raise TypeError('Base class should not be instantiated')
        return super().__new__(cls)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.char


class CellUnclicked(CellContentsType):
    __doc__ = 'Unclicked cell on a minesweeper board.'
    char = '#'


class CellNum(_NumericCellContentsMixin, CellContentsType):
    __doc__ = 'Number shown in a cell on a minesweeper board.'
    char = ''

    def __init__(self, num):
        super().__init__(num)
        if num < 0:
            raise ValueError('Cell value cannot be negative')


class CellMineType(_NumericCellContentsMixin, CellContentsType):
    __doc__ = 'Abstract base class for the number of a mine type in a cell.'

    def __new__(cls, num=1):
        if cls == CellMineType:
            raise TypeError(f"{type(cls)} should be used as a base class and not instantiated directly")
        return super().__new__(cls, num)

    def __init__(self, num=1):
        super().__init__(num)
        if num < 1:
            raise ValueError('Mine-type cell contents must represent one or more mines')

    @staticmethod
    def get_class_from_char(char):
        """
        Get the class of mine-like cell contents using the character
        representation.

        Arguments:
        char (str, length 1)
            The character representation of a cell contents type.

        Return:
            The cell contents class.
        """
        for cls in [CellMine, CellHitMine, CellFlag, CellWrongFlag]:
            if cls.char == char:
                return cls


class CellMine(CellMineType):
    __doc__ = 'Number of mines in a cell shown on a minesweeper board.'
    char = 'M'


class CellHitMine(CellMineType):
    __doc__ = 'Number of hit mines in a cell shown on a minesweeper board.'
    char = '!'


class CellFlag(CellMineType):
    __doc__ = 'Number of flags in a cell shown on a minesweeper board.'
    char = 'F'


class CellWrongFlag(CellFlag):
    __doc__ = 'Number of incorrect flags in a cell shown on a minesweeper board.'
    char = 'X'


class GameState(str, enum.Enum):
    __doc__ = '\n    Enum representing the state of a game.\n    '
    READY = 'READY'
    ACTIVE = 'ACTIVE'
    WON = 'WON'
    LOST = 'LOST'

    def started(self) -> bool:
        return self is not self.READY

    def finished(self) -> bool:
        return self in [self.WON, self.LOST]


class FaceState(enum.Enum):
    READY = 'ready'
    ACTIVE = 'active'
    WON = 'won'
    LOST = 'lost'


class CellImageType(enum.Flag):
    BUTTONS = enum.auto()
    NUMBERS = enum.auto()
    MARKERS = enum.auto()
    ALL = BUTTONS | NUMBERS | MARKERS


class UIMode(enum.Enum):
    GAME = enum.auto()
    CREATE = enum.auto()
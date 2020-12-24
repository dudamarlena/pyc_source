# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/p52/p52/base.py
# Compiled at: 2019-12-04 08:49:18
# Size of source mod 2**32: 2230 bytes


class P52Object:

    def __init__(self, *args, **kwargs):
        self.__name__ = kwargs.get('name')
        self.__unicode__ = kwargs.get('unicode')
        self.__symbol__ = kwargs.get('symbol')

    @property
    def name(self):
        return self.__name__

    @property
    def unicode(self):
        return self.__unicode__

    @property
    def symbol(self):
        return self.__symbol__


class Suit(P52Object):

    def __init__(self, *args, **kwargs):
        (P52Object.__init__)(self, *args, **kwargs)


class Rank(P52Object):

    def __init__(self, *args, **kwargs):
        (P52Object.__init__)(self, *args, **kwargs)
        self.__int__ = kwargs.get('value')

    @property
    def value(self):
        return self.__int__


class Card(Suit, Rank, object):

    def __init__(self, *args, **kwargs):
        super(Suit, self).__init__()
        super(Rank, self).__init__()
        if args:
            for a in args:
                if isinstance(a, Rank):
                    self.rank = a
                if isinstance(a, Suit):
                    self.suit = a

        if kwargs:
            self.suit = kwargs.get('suit')
            self.rank = kwargs.get('rank')
        self.trump = bool(kwargs.get('trump'))
        self.__name__ = f"{self.rank.name} of {self.suit.name}"
        self.__unicode__ = f"{self.rank.unicode}{self.suit.unicode}"
        self.__symbol__ = f"{self.rank.symbol}{self.suit.symbol}"

    @property
    def show(self):
        return f"{self.rank.symbol}{self.suit.unicode}"

    def __str__(self):
        return self.show

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return self.rank.value

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __ne__(self, other):
        return int(self) != int(other)

    def __add__(self, other):
        return int(self) + int(other)

    def __sub__(self, other):
        return int(self) - int(other)
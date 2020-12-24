# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/snap/t3mlite/perm4.py
# Compiled at: 2018-08-17 21:53:27
from operator import inv

def _make_opp_dict():

    def swap(t):
        return (
         t[1], t[0])

    dict = {(0, 1): (2, 3), (2, 0): (1, 3), (1, 2): (0, 3)}
    for k in list(dict.keys()):
        dict[dict[k]] = k
        dict[swap(dict[k])] = swap(k)
        dict[swap(k)] = swap(dict[k])

    return dict


class Perm4:

    def __init__(self, init, sign=1):
        self.dict = {}
        if len(init) == 4:
            for i in range(4):
                self.dict[i] = init[i]

        else:
            self.dict = init
            v = init.items()
            x = self.opposite[(v[0][0], v[1][0])]
            y = self.opposite[(v[0][1], v[1][1])]
            self.dict[x[0]] = y[sign]
            self.dict[x[1]] = y[(1 - sign)]

    opposite = _make_opp_dict()

    def image(self, bitmap):
        image = 0
        mask = 1
        for i in range(4):
            if bitmap & 1 << i:
                image = image | 1 << self.dict[i]

        return image

    def __repr__(self):
        return str(self.tuple())

    def __call__(self, a_tuple):
        image = []
        for i in a_tuple:
            image.append(self.dict[i])

        return tuple(image)

    def __getitem__(self, index):
        return self.dict[index]

    def __mul__(self, other):
        composition = {}
        for i in range(4):
            composition[i] = self.dict[other.dict[i]]

        return Perm4(composition)

    def __invert__(self):
        inverse = {}
        for i in range(4):
            inverse[self.dict[i]] = i

        return Perm4(inverse)

    def sign(self):
        sign = 0
        for i, j in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
            sign = sign ^ (self.dict[i] < self.dict[j])

        return sign

    def tuple(self):
        the_tuple = ()
        for i in range(4):
            the_tuple = the_tuple + (self.dict[i],)

        return the_tuple

    _rawS4 = [
     (0, 1, 2, 3),
     (0, 1, 3, 2),
     (0, 2, 1, 3),
     (0, 2, 3, 1),
     (0, 3, 1, 2),
     (0, 3, 2, 1),
     (1, 0, 2, 3),
     (1, 0, 3, 2),
     (1, 2, 0, 3),
     (1, 2, 3, 0),
     (1, 3, 0, 2),
     (1, 3, 2, 0),
     (2, 0, 1, 3),
     (2, 0, 3, 1),
     (2, 1, 0, 3),
     (2, 1, 3, 0),
     (2, 3, 0, 1),
     (2, 3, 1, 0),
     (3, 0, 1, 2),
     (3, 0, 2, 1),
     (3, 1, 0, 2),
     (3, 1, 2, 0),
     (3, 2, 0, 1),
     (3, 2, 1, 0)]

    @staticmethod
    def S4():
        """" 
    All permutations in S4
    """
        for p in Perm4._rawS4:
            yield Perm4(p)

    _rawA4 = [(0, 1, 2, 3),
     (0, 2, 3, 1),
     (0, 3, 1, 2),
     (1, 0, 3, 2),
     (1, 2, 0, 3),
     (1, 3, 2, 0),
     (2, 0, 1, 3),
     (2, 1, 3, 0),
     (2, 3, 0, 1),
     (3, 0, 2, 1),
     (3, 1, 0, 2),
     (3, 2, 1, 0)]

    @staticmethod
    def A4():
        """
     All even permutations in A4
     """
        for p in Perm4._rawA4:
            yield Perm4(p)

    _rawKleinFour = [(0, 1, 2, 3),
     (1, 0, 3, 2),
     (2, 3, 0, 1),
     (3, 2, 1, 0)]

    @staticmethod
    def KleinFour():
        """
     Z/2 x Z/2 as a subgroup of A4.
     """
        for p in Perm4._rawKleinFour:
            yield Perm4(p)
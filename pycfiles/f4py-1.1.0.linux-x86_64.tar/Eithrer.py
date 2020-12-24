# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/f4py/Eithrer.py
# Compiled at: 2016-03-10 01:40:29
from f4py.Maybe import maybe
from f4py.Monad import Monad

class Either(Monad):

    def __init__(self):
        raise Exception('Direct usage of either monad!')

    def is_left(self):
        return False

    def is_right(self):
        return False

    def get_left(self):
        return maybe(self._get_left())

    def get_right(self):
        return maybe(self._get_right())

    def map(self, mapper):
        if self.is_left():
            return Left(mapper(self._get_left()))
        return Right(mapper(self._get_right()))

    def bimap(self, left_mapper, right_mapper):
        return self.map(left_mapper if self.is_left() else right_mapper)

    def flat_map(self, mapper):
        return mapper(self._get_left() if self.is_left() else self._get_right())

    def flat_bimap(self, left_mapper, right_mapper):
        return self.flat_map(left_mapper if self.is_left() else right_mapper)

    def unpack(self):
        if self.is_left():
            return self._get_left()
        return self._get_right()

    def peek(self, mapper):
        mapper(self._get_left() if self.is_left() else self._get_right())
        return self

    def flip(self):
        if self.is_left():
            return right(self._get_left())
        return left(self._get_right())

    @classmethod
    def left(cls, value):
        return Left(value)

    @classmethod
    def right(cls, value):
        return Right(value)

    @classmethod
    def of(cls, pair):
        assert isinstance(pair, tuple)
        if pair[0] is not None:
            return left(pair[0])
        else:
            return right(pair[1])

    def _get_left(self):
        return

    def _get_right(self):
        return


class Left(Either):

    def __init__(self, value):
        self.value = value

    def is_left(self):
        return True

    def _get_left(self):
        return self.value

    def __str__(self):
        return 'Left ' + str(self.value)


class Right(Either):

    def __init__(self, value):
        self.value = value

    def is_right(self):
        return True

    def _get_right(self):
        return self.value

    def __str__(self):
        return 'Right ' + str(self.value)


def left(value):
    return Either.left(value)


def right(value):
    return Either.right(value)


def either(pair):
    return Either.of(pair)
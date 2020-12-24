# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/freedev/Desktop/supermovies/supermovies/rankable.py
# Compiled at: 2016-09-30 09:30:21
# Size of source mod 2**32: 407 bytes


class RankableMixin:

    def thumbs_up(self):
        self.increment_rank()

    def thumbs_down(self):
        self.decrement_rank()

    @property
    def normalized_rank(self):
        return self.get_rank() / 10

    @property
    def status(self):
        if self.is_a_hit():
            return 'Hit'
        return 'Flop'

    def is_a_hit(self):
        return self.get_rank() >= 10

    def __lt__(self, other):
        return other.get_rank() < self.get_rank()
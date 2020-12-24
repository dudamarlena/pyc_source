# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\fabric\balancing.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 4873 bytes
"""Implementing load balancing"""
import decimal

def _calc_ratio(part, whole):
    """Calculate ratio

    Returns int
    """
    return int((part / whole * 100).quantize((decimal.Decimal('1')),
      rounding=(decimal.ROUND_HALF_DOWN)))


class BaseScheduling(object):
    __doc__ = 'Base class for all scheduling classes dealing with load balancing'

    def __init__(self):
        """Initialize"""
        self._members = []
        self._ratios = []

    def set_members(self, *args):
        """Set members and ratios

        This methods sets the members using the arguments passed. Each
        argument must be a sequence where the second item is the weight.
        The first element is an identifier. For example:

            ('server1', 0.6), ('server2', 0.8)

        Setting members means that the load will be reset. If the members
        are the same as previously set, nothing will be reset or set.

        If no arguments were given the members will be set to an empty
        list.

        Raises ValueError when weight can't be converted to a Decimal.
        """
        raise NotImplementedError

    def get_next(self):
        """Returns the next member"""
        raise NotImplementedError

    @property
    def members(self):
        """Returns the members of this loadbalancer"""
        return self._members

    @property
    def ratios(self):
        """Returns the ratios for all members"""
        return self._ratios


class WeightedRoundRobin(BaseScheduling):
    __doc__ = 'Class for doing Weighted Round Robin balancing'

    def __init__(self, *args):
        super(WeightedRoundRobin, self).__init__()
        self._load = []
        self._next_member = 0
        self._nr_members = 0
        if args:
            (self.set_members)(*args)

    @property
    def load(self):
        """Returns the current load"""
        return self._load

    def set_members(self, *args):
        if not args:
            self._members = []
            return
        new_members = []
        for member in args:
            member = list(member)
            try:
                member[1] = decimal.Decimal(str(member[1]))
            except decimal.InvalidOperation:
                raise ValueError("Member '{member}' is invalid".format(member=member))

            new_members.append(tuple(member))

        new_members.sort(key=(lambda x: x[1]), reverse=True)
        if self._members == new_members:
            return
        self._members = new_members
        self._nr_members = len(new_members)
        min_weight = min(i[1] for i in self._members)
        self._ratios = []
        for _, weight in self._members:
            self._ratios.append(int(weight / min_weight * 100))

        self.reset()

    def reset(self):
        """Reset the load"""
        self._next_member = 0
        self._load = [0] * self._nr_members

    def get_next(self):
        """Returns the next member"""
        if self._ratios == self._load:
            self.reset()
        current = self._next_member
        while self._load[current] == self._ratios[current]:
            current = (current + 1) % self._nr_members

        self._load[current] += 1
        self._next_member = (current + 1) % self._nr_members
        return self._members[current]

    def __repr__(self):
        return '{class_}(load={load}, ratios={ratios})'.format(class_=(self.__class__),
          load=(self.load),
          ratios=(self.ratios))

    def __eq__(self, other):
        return self._members == other.members
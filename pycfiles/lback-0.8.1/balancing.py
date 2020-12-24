# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mysql\connector\fabric\balancing.pyc
# Compiled at: 2014-07-26 22:44:23
"""Implementing load balancing"""
import decimal

def _calc_ratio(part, whole):
    return int((part / whole * 100).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_DOWN))


class WeightedRoundRobin(object):
    """Class for doing Weighted Round Robin balancing"""

    def __init__(self, *args):
        """Initializing"""
        self._members = []
        self._sum_weights = 0
        self._ratios = []
        self._load = []
        if args:
            self.set_members(*args)

    @property
    def members(self):
        """Returns the members of this loadbalancer"""
        return self._members

    @property
    def ratios(self):
        """Returns the ratios for all members"""
        return self._ratios

    @property
    def load(self):
        """Returns the current load"""
        return self._load

    def set_members(self, *args):
        """Set members and ratios

        This methods sets thes members using the arguments passed. Each
        argument must be a sequence second item is the weight. The first
        element is an identifier. For example:

            ('server1', 0.6), ('server2', 0.8)

        Setting members means that the load will be reset. If the members
        are the same as previously set, nothing will be reset or set.

        Raises ValueError when weight can't be converted to a Decimal.
        """
        new_members = []
        for member in args:
            member = list(member)
            try:
                member[1] = decimal.Decimal(str(member[1]))
            except decimal.InvalidOperation:
                raise ValueError(("Member '{member}' is invalid").format(member=member))

            new_members.append(tuple(member))

        new_members.sort(key=lambda x: x[1], reverse=True)
        if self._members == new_members:
            return
        self._members = new_members
        self._members.sort(key=lambda x: x[1], reverse=True)
        self._sum_weights = sum([ i[1] for i in self._members ])
        self._ratios = []
        for name, weight in self._members:
            self._ratios.append(_calc_ratio(weight, self._sum_weights))

        self.reset()

    def reset(self):
        """Reset the load"""
        self._load = [
         0] * len(self._members)

    def get_next(self):
        """Returns the next member"""
        if self._ratios == self._load:
            self.reset()
        for i, ratio in enumerate(self._ratios):
            if self._load[i] < ratio:
                self._load[i] += 1
                return self._members[i]

    def __repr__(self):
        return ('{class_}(load={load}, ratios={ratios})').format(class_=self.__class__, load=self.load, ratios=self.ratios)

    def __eq__(self, other):
        return self._members == other.members
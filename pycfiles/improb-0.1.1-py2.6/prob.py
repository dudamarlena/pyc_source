# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/improb/lowprev/prob.py
# Compiled at: 2011-06-09 03:27:23
"""A module for working with probability measures."""
from __future__ import division, absolute_import, print_function
import math, random, fractions
from improb import PSpace, Gamble, Event, _str_keys_values
from improb.lowprev.linvac import LinVac
from improb.lowprev.lowpoly import LowPoly

class Prob(LinVac):
    """A probability measure, implemented as a
    :class:`~improb.lowprev.linvac.LinVac` whose natural extension is
    calculated via expectation; see :meth:`get_precise`.

    >>> p = Prob(5, prob=['0.1', '0.2', '0.3', '0.05', '0.35'])
    >>> print(p)
    0 : 1/10
    1 : 1/5
    2 : 3/10
    3 : 1/20
    4 : 7/20
    >>> print(p.get_precise([2, 4, 3, 8, 1]))
    53/20
    >>> print(p.get_precise([2, 4, 3, 8, 1], [0, 1]))
    10/3

    >>> p = Prob(3, prob={(0,): '0.4'})
    >>> print(p)
    0 : 2/5
    1 : undefined
    2 : undefined
    >>> p.extend()
    >>> print(p)
    0 : 2/5
    1 : 3/10
    2 : 3/10
    """

    def __str__(self):
        return _str_keys_values(self.pspace, (self.get(({omega: 1}, True), ('undefined',
                                                                            'undefined'))[0] for omega in self.pspace))

    def _make_value(self, value):
        (lprev, uprev) = LowPoly._make_value(self, value)
        if self.number_cmp(lprev, uprev) != 0:
            raise ValueError('can only specify precise prevision')
        return (
         lprev, uprev)

    def is_valid(self, raise_error=False):

        def oops(msg):
            if raise_error:
                raise ValueError(msg)
            else:
                return False

        if any(self.number_cmp(value[0], value[1]) != 0 for value in self.itervalues()):
            return oops('probabilities must be precise')
        if any(self.number_cmp(value[0], 0) == -1 for value in self.itervalues()):
            return oops('probabilities must be non-negative')
        if self.number_cmp(sum(value[0] for value in self.itervalues()), 1) != 0:
            return oops('probabilities must sum to one')
        return True

    def get_linvac(self, epsilon):
        r"""Convert probability into a linear vacuous mixture:

        .. math::

           \underline{E}(f)=(1-\epsilon)E(f)+\epsilon\inf f"""
        epsilon = self.make_number(epsilon)
        return LinVac(self.pspace, lprob=[ (1 - epsilon) * self[({omega: 1}, True)][0] for omega in self.pspace
                                         ], number_type=self.number_type)

    def get_lowprev(self, gamble, event=True, algorithm='linear'):
        return get_precise(gamble, event, algorithm)

    def get_precise(self, gamble, event=True, algorithm='linear'):
        r"""Calculate the conditional expectation,

        .. math::

           E(f|A)=
           \frac{
           \sum_{\omega\in A}p(\omega)f(\omega)
           }{
           \sum_{\omega\in A}p(\omega)
           }

        where :math:`p(\omega)` is simply the probability of the
        singleton :math:`\omega`::

            self[{omega: 1}, True][0]
        """
        if algorithm is None:
            algorithm = 'linear'
        if algorithm != 'linear':
            return LinVac.get_lower(self, gamble, event, algorithm)
        else:
            self.is_valid(raise_error=True)
            gamble = self.make_gamble(gamble)
            if event is True or isinstance(event, Event) and event.is_true():
                return sum(self[({omega: 1}, True)][0] * gamble[omega] for omega in self.pspace)
            event = self.pspace.make_event(event)
            event_prob = self.get_precise(event.indicator(self.number_type))
            if event_prob == 0:
                raise ZeroDivisionError('cannot condition on event with zero probability')
            return self.get_precise(gamble * event) / event_prob
            return

    @classmethod
    def make_random(cls, pspace=None, division=None, zero=True, number_type='float'):
        """Generate a random probability mass function.

        >>> import random
        >>> random.seed(25)
        >>> print(Prob.make_random("abcd", division=10))
        a : 0.4
        b : 0.0
        c : 0.1
        d : 0.5
        >>> random.seed(25)
        >>> print(Prob.make_random("abcd", division=10, zero=False))
        a : 0.3
        b : 0.1
        c : 0.2
        d : 0.4
        """
        pspace = PSpace.make(pspace)
        lpr = cls(pspace=pspace, number_type=number_type)
        probs = [ -math.log(random.random()) for omega in pspace ]
        sum_probs = sum(probs)
        probs = [ prob / sum_probs for prob in probs ]
        if division is not None:
            probs = [ int(prob * division + 0.5) + (0 if zero else 1) for prob in probs
                    ]
            while sum(probs) < division:
                probs[random.randrange(len(probs))] += 1

            while sum(probs) > division:
                while True:
                    idx = random.randrange(len(probs))
                    if probs[idx] > (1 if zero else 2):
                        probs[idx] -= 1
                        break

            probs = [ fractions.Fraction(prob, division) for prob in probs ]
        return cls(pspace=pspace, number_type=number_type, prob=probs)

    def extend(self, keys=None, lower=True, upper=True, algorithm='linear'):
        if algorithm is None:
            algorithm = 'linear'
        if algorithm != 'linear':
            LinVac.extend(self, keys, lower, upper, algorithm)
            return
        else:
            num_undefined = len(self.pspace) - len(self)
            if num_undefined == 0:
                return
            mass = sum(self.get(({omega: 1}, True), (0, 0))[0] for omega in self.pspace)
            remaining_mass = (1 - mass) / num_undefined
            value = (remaining_mass, remaining_mass)
            for omega in self.pspace:
                key = ({omega: 1}, True)
                if key not in self:
                    self[key] = value

            return
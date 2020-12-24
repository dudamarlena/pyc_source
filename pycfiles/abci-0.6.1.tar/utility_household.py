# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/utility_household.py
# Compiled at: 2018-03-06 09:22:50
import abce
from tools import is_zero

class UtilityHousehold(abce.Agent, abce.Household):

    def init(self, rounds):
        self.last_round = rounds - 1
        if self.id == 0 or self.id == 2:

            def utility_function(a, b, c):
                utility = max(a ** 0.2, b ** 0.5 * c ** 0.3)
                a = 0
                b = 0.9 * b
                return (
                 utility, locals())

            self.utility_function = utility_function
        elif self.id == 1 or self.id == 3:
            self.utility_function = self.create_cobb_douglas_utility_function({'a': 0.2, 'b': 0.5, 'c': 0.3})

    def one(self):
        pass

    def two(self):
        pass

    def three(self):
        pass

    def clean_up(self):
        pass

    def consumption(self):
        if self.id == 0:
            self.create('a', 10)
            self.create('b', 10)
            self.create('c', 10)
            utility = self.consume(self.utility_function, {'a': 5, 'b': 3, 'c': 1})
            assert utility == max(1.379729661461215, 1.7320508075688772 * 1.0), utility
            assert self['a'] == 5
            assert self['b'] == 9.7
            assert self['c'] == 10
            self.destroy('a')
            self.destroy('b')
            self.destroy('c')
        elif self.id == 1:
            self.create('a', 10)
            self.create('b', 10)
            self.create('c', 10)
            utility = self.consume(self.utility_function, {'a': 5, 'b': 3, 'c': 1})
            assert utility == 1.379729661461215 * 1.7320508075688772 * 1.0, utility
            assert self['a'] == 5
            assert self['b'] == 7
            assert self['c'] == 9
            self.consume(self.utility_function, ['a', 'b', 'c'])
            assert self['a'] == 0
            assert self['b'] == 0
            assert self['c'] == 0
            pu = self.utility_function(**{'a': 5, 'b': 300, 'c': 10})
            assert pu == 1.379729661461215 * 17.320508075688775 * 1.9952623149688795
        elif self.id == 2:
            self.create('a', 10)
            self.create('b', 10)
            self.create('c', 10)
            utility = self.consume(self.utility_function, ['a', 'b', 'c'])
            assert is_zero(utility - max(1.5848931924611136, 3.1622776601683795 * 1.9952623149688795)), (
             utility, max(1.5848931924611136, 3.1622776601683795 * 1.9952623149688795))
            assert self['a'] == 0
            assert self['b'] == 9
            assert self['c'] == 10
            self.destroy('a')
            self.destroy('b')
            self.destroy('c')
        elif self.id == 3:
            self.create('a', 10)
            self.create('b', 10)
            self.create('c', 10)
            utility = self.consume(self.utility_function, ['a', 'b', 'c'])
            assert is_zero(utility - 1.5848931924611136 * 3.1622776601683795 * 1.9952623149688795), (utility, 1.5848931924611136 * 3.1622776601683795 * 1.9952623149688795)
            assert self['a'] == 0
            assert self['b'] == 0
            assert self['c'] == 0
            pu = self.utility_function(**{'a': 5, 'b': 300, 'c': 10})
            assert pu == 1.379729661461215 * 17.320508075688775 * 1.9952623149688795

    def all_tests_completed(self):
        if self.round == self.last_round and self.id == 0:
            print 'Test consume:                             \tOK'
            print 'Test set_utility_function:                \tOK'
            print 'Test set_cobb_douglas_utility_function    \tOK'
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/production_firm.py
# Compiled at: 2017-12-09 17:42:02
import abce
from tools import is_zero
from abce.agents import Firm

class ProductionFirm(abce.Agent, Firm):

    def init(self, simulation_parameters, agent_parameters):
        self.last_round = simulation_parameters['rounds'] - 1
        if self.id == 0:

            def mes(goods):
                return max(goods['a'] ** 2, goods['a'] ** 0.5 * goods['b'])

            use = {'a': 1, 'b': 0.1}
            self.set_production_function(mes, 'consumption_good', use)
        elif self.id == 1:
            self.set_cobb_douglas('consumption_good', 5, {'a': 2, 'b': 1})
        elif self.id == 2:
            self.leontief = self.set_leontief('consumption_good', {'a': 3, 'b': 1})
        elif self.id == 3:

            def many_goods_pf(goods):
                output = {'soft_rubber': goods['a'] ** 0.25 * goods['b'] ** 0.5 * goods['c'] ** 0.25, 'hard_rubber': goods['a'] ** 0.1 * goods['b'] ** 0.2 * goods['c'] ** 0.01, 
                   'waste': goods['b'] / 2}
                return output

            use = {'a': 1, 'b': 0.1, 'c': 0}
            self.set_production_function_many_goods(many_goods_pf, use)
        elif self.id == 4:
            self.set_leontief('car', {'wheels': 4, 'chassi': 1})
        elif self.id == 5:
            self.set_ces('consumption_good', gamma=0.5, shares={'a': 0.25, 
               'b': 0.25, 'c': 0.5})
        elif self.id == 6:
            self.set_ces('consumption_good', gamma=0.5, multiplier=2)

    def production(self):
        if self.id == 0:
            self.create('a', 2)
            self.create('b', 2)
            self.produce({'a': 1, 'b': 2})
            assert self['a'] == 1, self['a']
            assert self['b'] == 1.8, self['b']
            assert self['consumption_good'] == 2.0, self['consumption_good']
            self.destroy('a', 1)
            self.destroy('b', 1.8)
            self.destroy('consumption_good', 2.0)
            output = self.predict_produce_output({'a': 10, 'b': 10})
            assert output['consumption_good'] == max(100, 31.622776601683796)
            input = self.predict_produce_input({'a': 10, 'b': 10})
            assert input['a'] == 10, input['a']
            assert input['b'] == 1, input['b']
            nv = self.net_value(output, input, {'consumption_good': 10, 'a': 1, 'b': 2})
            assert nv == 1000 - (10 + 2), nv
        elif self.id == 1:
            self.create('a', 2)
            self.create('b', 2)
            self.produce({'a': 1, 'b': 2})
            assert self['a'] == 1, self['a']
            assert self['b'] == 0, self['b']
            assert self['consumption_good'] == 5 * 1 * 2, self['consumption_good']
            self.destroy('a', 1)
            self.destroy('consumption_good', 5 * 1 * 2)
        elif self.id == 2:
            self.create('a', 2)
            self.create('b', 2)
            self.produce({'a': 1, 'b': 2})
            assert self['a'] == 1, self['a']
            assert self['b'] == 0, self['b']
            assert self['consumption_good'] == min(3, 2), self['consumption_good']
            self.destroy('a', 1)
            self.destroy('consumption_good', min(3, 2))
        elif self.id == 3:
            self.create('a', 10)
            self.create('b', 10)
            self.create('c', 10)
            self.produce({'a': 1, 'b': 2, 'c': 5})
            assert self['a'] == 9, self['a']
            assert self['b'] == 9.8, self['b']
            assert self['c'] == 10, self['c']
            assert self['soft_rubber'] == 1.0 * 1.4142135623730951 * 1.4953487812212205
            assert self['hard_rubber'] == 1.0 * 1.148698354997035 * 1.0162245912673256
            assert self['waste'] == 2 / 2, self['waste']
            self.destroy('a')
            self.destroy('b')
            self.destroy('c')
            self.destroy('soft_rubber')
            self.destroy('hard_rubber')
            self.destroy('waste')
        elif self.id == 4:
            input_goods = {'wheels': 4, 'chassi': 1}
            price_vector = {'wheels': 10, 'chassi': 100, 'car': 1000}
            nv = self.predict_net_value(input_goods, price_vector)
            assert nv == 860
        elif self.id == 5:
            self.create('a', 2)
            self.create('b', 2)
            self.create('c', 4)
            self.produce({'a': 1, 'b': 2, 'c': 4})
            assert self['a'] == 1, self['a']
            assert self['b'] == 0, self['b']
            assert self['c'] == 0, self['c']
            expected = (0.25 * 1.0 + 0.25 * 1.4142135623730951 + 0.5 * 2.0) ** (1 / 0.5)
            assert self['consumption_good'] == expected, (
             self['consumption_good'], expected)
            self.destroy('a', 1)
            self.destroy('consumption_good', expected)
        elif self.id == 6:
            self.create('a', 2)
            self.create('b', 2)
            self.create('c', 2)
            self.create('d', 2)
            self.create('e', 2)
            self.produce({'a': 1, 'b': 2, 'c': 2, 'd': 2, 'e': 2})
            assert self['a'] == 1, self['a']
            assert self['b'] == 0, self['b']
            assert self['c'] == 0, self['c']
            assert self['d'] == 0, self['d']
            assert self['e'] == 0, self['e']
            expected = 2 * (0.2 * 1.0 + 0.2 * 1.4142135623730951 + 0.2 * 1.4142135623730951 + 0.2 * 1.4142135623730951 + 0.2 * 1.4142135623730951) ** (1 / 0.5)
            assert is_zero(self['consumption_good'] - expected), (self['consumption_good'], expected)
            self.destroy('a', 1)
            self.destroy('consumption_good', expected)

    def all_tests_completed(self):
        if self.round == self.last_round and self.id == 0:
            print 'Test produce:                             \tOK'
            print 'Test set_production_function              \tOK'
            print 'Test set_production_function_many_goods:  \tOK'
            print 'Test leontief:                            \tOK'
            print 'Test create_production_function_many_goods\tOK'
            print 'Test predict_produce_output               \tOK'
            print 'Test predict_produce_input                \tOK'
            print 'Test net_value                            \tOK'
            print 'Test predict_net_value                    \tOK'
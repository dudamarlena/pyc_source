# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_utils_metaheuristics.py
# Compiled at: 2020-01-17 14:24:21
# Size of source mod 2**32: 726 bytes
import unittest, pychemia.utils.metaheuristics

class MetaheuristicFunctionTest(unittest.TestCase):

    def test_metaheuristic(self):
        """
        Test (pychemia.utils.metaheuristics)                        :
        """
        for i in ('Sphere', 'Ackley', 'Rosenbrock', 'Beale', 'GoldsteinPrice', 'Booth',
                  'BukinN6', 'Matyas', 'LeviN13', 'ThreeHump', 'Easom', 'CrossInTray',
                  'Eggholder', 'HolderTable', 'McCormick', 'SchafferN2', 'SchafferN4',
                  'StyblinskiTang'):
            func = eval('pychemia.utils.metaheuristics.' + i + '()')
            print(i)
            print(func.mindim)
            print(func.minimum(func.mindim))
            print(func.fminimum(func.mindim))
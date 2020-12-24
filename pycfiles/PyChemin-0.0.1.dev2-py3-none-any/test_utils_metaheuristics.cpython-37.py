# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
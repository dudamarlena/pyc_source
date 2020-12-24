# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_population.py
# Compiled at: 2020-01-17 14:46:56
# Size of source mod 2**32: 1883 bytes
import unittest, os
from .local_mongo import has_local_mongo
from pychemia.population import LJCluster, RelaxStructures, OrbitalDFTU, NonCollinearMagMoms, RealFunction

def funx2(x):
    return x ** 2


class PopulationTest(unittest.TestCase):

    def test_ljcluster(self):
        """
        Test (pychemia.population.LJCluster)                        :
        """
        if not has_local_mongo():
            return
        popu = LJCluster('test', 'Ne4')
        popu.add_random()
        popu.add_random()
        popu.pcdb.clean()

    def test_structure(self):
        """
        Test (pychemia.population.RelaxStructures)                  :
        """
        if not has_local_mongo():
            return
        popu = RelaxStructures('test', 'NaCl')
        popu.add_random()
        popu.add_random()
        popu.pcdb.clean()

    def test_noncoll(self):
        """
        Test (pychemia.population.NonCollinearMagMoms)              :
        """
        if not has_local_mongo():
            return
        popu = NonCollinearMagMoms('test', source_dir='tests/data/vasp_02')
        popu.add_random()
        popu.add_random()
        popu.pcdb.clean()

    def test_dftu(self):
        """
        Test (pychemia.population.OrbitalDFTU)                      :
        """
        if not has_local_mongo():
            return
        print(os.getcwd())
        popu = OrbitalDFTU('test', 'tests/data/abinit_05/abinit.in')
        popu.add_random()
        popu.add_random()
        popu.pcdb.clean()

    def test_euclidean(self):
        """
        Test (pychemia.population.RealFunction)                     :
        """
        if not has_local_mongo():
            return
        popu = RealFunction(funx2, 2, [-1, 1])
        popu.add_random()
        popu.add_random()


if __name__ == '__main__':
    unittest.main()
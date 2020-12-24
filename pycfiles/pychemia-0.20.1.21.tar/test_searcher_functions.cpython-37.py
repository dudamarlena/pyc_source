# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_searcher_functions.py
# Compiled at: 2020-01-17 14:23:53
# Size of source mod 2**32: 3219 bytes
import unittest, numpy as np, logging
from pychemia import pcm_log
from pychemia.searcher import FireFly, HarmonySearch, ParticleSwarm, GeneticAlgorithm
from pychemia.population import RealFunction
from pychemia.utils.metaheuristics import Sphere
logging.basicConfig(level=(logging.DEBUG))

class SearcherTest(unittest.TestCase):

    def test_harmony(self):
        """
        Test (pychemia.searcher.harmony)                            :
        """
        pcm_log.debug('HarmonySearch')
        mini = Sphere().minimum(3)
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=False)
        searcher = HarmonySearch(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=True)
        searcher = HarmonySearch(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        assert np.linalg.norm(np.array(searcher.population.db[searcher.population.best_candidate]['x']) - mini) < 0.2

    def test_swarm(self):
        """
        Test (pychemia.searcher.swarm)                              :
        """
        pcm_log.debug('ParticleSwarm')
        mini = Sphere().minimum(3)
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=False)
        searcher = ParticleSwarm(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=True)
        searcher = ParticleSwarm(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        assert np.linalg.norm(np.array(searcher.population.db[searcher.population.best_candidate]['x']) - mini) < 0.2

    def test_firefly(self):
        """
        Test (pychemia.searcher.firefly)                            :
        """
        pcm_log.debug('FireFly')
        mini = Sphere().minimum(3)
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=False)
        searcher = FireFly(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=True)
        searcher = FireFly(popu, {'delta':0.1,  'gamma':0.1,  'beta0':0.8,  'alpha0':0,  'multi_move':True}, generation_size=16,
          stabilization_limit=5)
        searcher.run()
        assert np.linalg.norm(np.array(searcher.population.db[searcher.population.best_candidate]['x']) - mini) < 0.2

    def test_genetic(self):
        """
        Test (pychemia.searcher.genetic)                            :
        """
        pcm_log.debug('GeneticAlgorithm')
        mini = Sphere().minimum(3)
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=False)
        searcher = GeneticAlgorithm(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        popu = RealFunction((Sphere.function), 3, [-1, 1], local_minimization=True)
        searcher = GeneticAlgorithm(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        assert np.linalg.norm(np.array(searcher.population.db[searcher.population.best_candidate]['x']) - mini) < 0.2
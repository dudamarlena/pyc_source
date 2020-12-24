# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_searcher_noncollinear.py
# Compiled at: 2020-01-17 14:24:07
# Size of source mod 2**32: 2580 bytes
import os, unittest
from pychemia import pcm_log, HAS_PYMONGO
from pychemia.population import NonCollinearMagMoms
from pychemia.searcher import HarmonySearch, FireFly, GeneticAlgorithm
from .local_mongo import has_local_mongo
import logging

class SearcherTest(unittest.TestCase):

    def test_harmony(self):
        """
        Test (pychemia.searcher.harmony) with NonCollinearMagMoms   :
        """
        logging.basicConfig(level=(logging.DEBUG))
        if not HAS_PYMONGO:
            print('Could not load pymongo, leaving now')
            return
        else:
            return has_local_mongo() or None
        pcm_log.debug('HarmonySearch')
        source = 'tests/data/vasp_02'
        assert os.path.isfile(source + os.sep + 'INCAR')
        assert os.path.isfile(source + os.sep + 'POSCAR')
        popu = NonCollinearMagMoms('test', source, debug=True)
        popu.pcdb.clean()
        searcher = HarmonySearch(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        popu.pcdb.clean()

    def test_firefly(self):
        """
        Test (pychemia.searcher.firefly) with NonCollinearMagMoms   :
        """
        logging.basicConfig(level=(logging.DEBUG))
        if not HAS_PYMONGO:
            print('Could not load pymongo, leaving now')
            return
        else:
            return has_local_mongo() or None
        pcm_log.debug('HarmonySearch')
        source = 'tests/data/vasp_02'
        assert os.path.isfile(source + os.sep + 'INCAR')
        assert os.path.isfile(source + os.sep + 'POSCAR')
        popu = NonCollinearMagMoms('test', source, debug=True)
        popu.pcdb.clean()
        searcher = FireFly(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        popu.pcdb.clean()

    def test_genetic(self):
        """
        Test (pychemia.searcher.genetic) with NonCollinearMagMoms   :
        """
        logging.basicConfig(level=(logging.DEBUG))
        if not HAS_PYMONGO:
            print('Could not load pymongo, leaving now')
            return
        else:
            return has_local_mongo() or None
        pcm_log.debug('HarmonySearch')
        source = 'tests/data/vasp_02'
        assert os.path.isfile(source + os.sep + 'INCAR')
        assert os.path.isfile(source + os.sep + 'POSCAR')
        popu = NonCollinearMagMoms('test', source, debug=True)
        popu.pcdb.clean()
        searcher = GeneticAlgorithm(popu, generation_size=16, stabilization_limit=5)
        searcher.run()
        popu.pcdb.clean()
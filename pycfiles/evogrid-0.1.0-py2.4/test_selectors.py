# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/tests/test_selectors.py
# Compiled at: 2006-07-11 11:57:27
from zope.testing import doctest
import unittest, random
from copy import deepcopy
from itertools import islice
from zope.interface.verify import verifyClass, verifyObject
import evogrid.common.selectors
from evogrid.common.selectors import BaseSelector, EliteSelector, RandomSelector, TournamentSelector, ProviderFromSelectorAndPool
from evogrid.interfaces import IProvider, ISelector, IRemoverSelector, ICopierSelector

class FakeEvaluatedReplicator:
    __module__ = __name__

    def __init__(self, ev=0):
        self.evaluation = ev

    def replicate(self):
        return deepcopy(self)

    def __repr__(self):
        return '<%s object with evaluation=%r>' % (self.__class__.__name__, self.evaluation)


class FixtureForSelectorTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        random.seed('seed to make the tests reproducible')
        self.pool = [ FakeEvaluatedReplicator(i) for i in xrange(5) ]


class SelectorTestCase(FixtureForSelectorTestCase):
    __module__ = __name__

    def _test_provider(self, selector, expected_evaluations, nb_to_provide=None):
        pool = self.pool
        initial_pool_len = len(pool)
        provider = ProviderFromSelectorAndPool(selector, pool)
        self.assert_(verifyObject(IProvider, provider))
        if nb_to_provide is None:
            nb_to_provide = len(expected_evaluations)
        selected = list(islice(provider, nb_to_provide))
        self.assertEquals([ rep.evaluation for rep in selected ], expected_evaluations)
        self.assertEquals(len(pool), initial_pool_len)
        for rep in selected:
            self.assert_(rep in pool)

        return

    def test_BaseSelector(self):
        pool = self.pool
        known_to_be_the_max = pool[4]
        base_selector = BaseSelector()
        self.assertEquals(base_selector._max(pool), known_to_be_the_max)
        random.shuffle(pool)
        self.assertEquals(base_selector._max(pool), known_to_be_the_max)
        random.shuffle(pool)
        self.assertEquals(base_selector._max(pool), known_to_be_the_max)
        random.shuffle(pool)
        self.assertEquals(base_selector._max(pool), known_to_be_the_max)

    def test_RandomSelector(self):
        pool = self.pool
        self.assert_(verifyClass(ISelector, RandomSelector))
        random_selector = RandomSelector()
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 3)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 2)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)

    def test_RandomSelector_provider(self):
        self._test_provider(RandomSelector(), [4, 3, 4, 2])

    def test_EliteSelector(self):
        pool = self.pool
        self.assert_(verifyClass(ISelector, EliteSelector))
        elite_selector = EliteSelector()
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)

    def test_EliteSelector_provider(self):
        self._test_provider(EliteSelector(), [4] * 42)

    def test_2OpponentsTournamentSelector(self):
        pool = self.pool
        self.assert_(verifyClass(ISelector, TournamentSelector))
        tournament_selector = TournamentSelector(n=2)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 3)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 1)
        self.assertEquals(len(pool), 5)
        self.assert_(rep in pool)

    def test_2OpponentsTournamentSelector_provider(self):
        self._test_provider(TournamentSelector(), [4, 4, 4, 4, 3, 1])

    def test_6OpponnentsTournamentSelector(self):
        pool = self.pool
        self.assert_(verifyClass(ISelector, TournamentSelector))
        tournament_selector = TournamentSelector(n=6)
        self.assertRaises(ValueError, tournament_selector.select_from, pool)

    def test_6OpponentsTournamentSelector_provider(self):
        self._test_provider(TournamentSelector(n=6), [], nb_to_provide=10)


class CopierSelectorTestCase(FixtureForSelectorTestCase):
    __module__ = __name__

    def _test_provider(self, selector, expected_evaluations, nb_to_provide=None):
        pool = self.pool
        initial_pool_len = len(pool)
        provider = ProviderFromSelectorAndPool(selector, pool)
        self.assert_(verifyObject(IProvider, provider))
        if nb_to_provide is None:
            nb_to_provide = len(expected_evaluations)
        selected = list(islice(provider, nb_to_provide))
        self.assertEquals([ rep.evaluation for rep in selected ], expected_evaluations)
        self.assertEquals(len(pool), initial_pool_len)
        for rep in selected:
            self.assert_(rep not in pool)

        return

    def test_RandomSelector(self):
        pool = self.pool
        random_selector = ICopierSelector(RandomSelector())
        self.assert_(verifyObject(ICopierSelector, random_selector))
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 3)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 2)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)

    def test_RandomSelector_provider(self):
        self._test_provider(ICopierSelector(RandomSelector()), [4, 3, 4, 2])

    def test_EliteSelector(self):
        pool = self.pool
        elite_selector = ICopierSelector(EliteSelector())
        self.assert_(verifyObject(ICopierSelector, elite_selector))
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)

    def test_EliteSelector_provider(self):
        self._test_provider(ICopierSelector(EliteSelector()), [4] * 42)

    def test_2OpponentsTournamentSelector(self):
        pool = self.pool
        tournament_selector = ICopierSelector(TournamentSelector(n=2))
        self.assert_(verifyObject(ICopierSelector, tournament_selector))
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 3)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)
        rep = tournament_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 1)
        self.assertEquals(len(pool), 5)
        self.assert_(rep not in pool)

    def test_2OpponentsTournamentSelector_provider(self):
        self._test_provider(ICopierSelector(TournamentSelector()), [
         4, 4, 4, 4, 3, 1])

    def test_6OpponnentsTournamentSelector(self):
        pool = self.pool
        tournament_selector = ICopierSelector(TournamentSelector(n=6))
        self.assert_(verifyObject(ICopierSelector, tournament_selector))
        self.assertRaises(ValueError, tournament_selector.select_from, pool)

    def test_6OpponentsTournamentSelector_provider(self):
        self._test_provider(ICopierSelector(TournamentSelector(n=6)), [], nb_to_provide=10)


class RemoverSelectorTestCase(FixtureForSelectorTestCase):
    __module__ = __name__

    def _test_provider(self, selector, expected_evaluations, nb_remaining=0):
        pool = self.pool
        provider = ProviderFromSelectorAndPool(selector, pool)
        self.assert_(verifyObject(IProvider, provider))
        selected = list(provider)
        self.assertEquals([ rep.evaluation for rep in selected ], expected_evaluations)
        self.assertEquals(len(pool), nb_remaining)
        for rep in selected:
            self.assert_(rep not in pool)

    def test_RandomSelector(self):
        pool = self.pool
        random_selector = IRemoverSelector(RandomSelector())
        self.assert_(verifyObject(IRemoverSelector, random_selector))
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 4)
        self.assert_(rep not in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 2)
        self.assertEquals(len(pool), 3)
        self.assert_(rep not in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 3)
        self.assertEquals(len(pool), 2)
        self.assert_(rep not in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 1)
        self.assertEquals(len(pool), 1)
        self.assert_(rep not in pool)
        rep = random_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 0)
        self.assertEquals(len(pool), 0)
        self.assert_(rep not in pool)
        self.assertRaises(ValueError, random_selector.select_from, pool)

    def test_RandomSelector_provider(self):
        self._test_provider(IRemoverSelector(RandomSelector()), [4, 2, 3, 1, 0])

    def test_EliteSelector(self):
        pool = self.pool
        elite_selector = IRemoverSelector(EliteSelector())
        self.assert_(verifyObject(IRemoverSelector, elite_selector))
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 4)
        self.assert_(rep not in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 3)
        self.assertEquals(len(pool), 3)
        self.assert_(rep not in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 2)
        self.assertEquals(len(pool), 2)
        self.assert_(rep not in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 1)
        self.assertEquals(len(pool), 1)
        self.assert_(rep not in pool)
        rep = elite_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 0)
        self.assertEquals(len(pool), 0)
        self.assert_(rep not in pool)
        self.assertRaises(ValueError, elite_selector.select_from, pool)

    def test_EliteSelector_provider(self):
        self._test_provider(IRemoverSelector(EliteSelector()), [4, 3, 2, 1, 0])

    def test_3OpponentsTournamentSelector(self):
        pool = self.pool
        tournamenent_selector = IRemoverSelector(TournamentSelector(n=3))
        self.assert_(verifyObject(IRemoverSelector, tournamenent_selector))
        rep = tournamenent_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 4)
        self.assert_(rep not in pool)
        rep = tournamenent_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 3)
        self.assertEquals(len(pool), 3)
        self.assert_(rep not in pool)
        rep = tournamenent_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 2)
        self.assertEquals(len(pool), 2)
        self.assert_(rep not in pool)
        self.assertRaises(ValueError, tournamenent_selector.select_from, pool)

    def test_3OpponentsTournamentSelector_provider(self):
        self._test_provider(IRemoverSelector(TournamentSelector(n=3)), [
         4, 3, 2], nb_remaining=2)

    def test_5OpponnentsTournamentSelector(self):
        pool = self.pool
        tournamenent_selector = IRemoverSelector(TournamentSelector(n=5))
        self.assert_(verifyObject(IRemoverSelector, tournamenent_selector))
        rep = tournamenent_selector.select_from(pool)
        self.assertEquals(rep.evaluation, 4)
        self.assertEquals(len(pool), 4)
        self.assertRaises(ValueError, tournamenent_selector.select_from, pool)

    def test_5OpponentsTournamentSelector_provider(self):
        self._test_provider(IRemoverSelector(TournamentSelector(n=5)), [
         4], nb_remaining=4)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SelectorTestCase))
    suite.addTests(unittest.makeSuite(CopierSelectorTestCase))
    suite.addTests(unittest.makeSuite(RemoverSelectorTestCase))
    suite.addTests(doctest.DocTestSuite(evogrid.common.selectors))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
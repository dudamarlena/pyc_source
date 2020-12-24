# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/pypokerengine/api/game_test.py
# Compiled at: 2017-02-24 03:36:19
import pypokerengine.api.game as G
from nose.tools import raises
from tests.base_unittest import BaseUnitTest
from examples.players.fold_man import FoldMan

class GameTest(BaseUnitTest):

    def test_start_poker(self):
        config = G.setup_config(1, 100, 10)
        config.register_player('p1', FoldMan())
        config.register_player('p2', FoldMan())
        result = G.start_poker(config)
        p1, p2 = [ result['players'][i] for i in range(2) ]
        self.eq('p1', p1['name'])
        self.eq(110, p1['stack'])
        self.eq('p2', p2['name'])
        self.eq(90, p2['stack'])

    def test_start_poker_with_ante(self):
        config = G.setup_config(1, 100, 10, 15)
        config.register_player('p1', FoldMan())
        config.register_player('p2', FoldMan())
        result = G.start_poker(config)
        p1, p2 = [ result['players'][i] for i in range(2) ]
        self.eq('p1', p1['name'])
        self.eq(125, p1['stack'])
        self.eq('p2', p2['name'])
        self.eq(75, p2['stack'])

    def test_set_blind_structure(self):
        config = G.setup_config(1, 100, 10)
        config.register_player('p1', FoldMan())
        config.register_player('p2', FoldMan())
        config.set_blind_structure({1: {'ante': 5, 'small_blind': 10}})
        result = G.start_poker(config)
        p1, p2 = [ result['players'][i] for i in range(2) ]
        self.eq(115, p1['stack'])
        self.eq(85, p2['stack'])

    def test_start_poker_validation_when_no_player(self):
        config = G.setup_config(1, 100, 10)
        with self.assertRaises(Exception) as (e):
            result = G.start_poker(config)
        self.assertIn('no player', str(e.exception))

    def test_start_poker_validation_when_one_player(self):
        config = G.setup_config(1, 100, 10)
        config.register_player('p1', FoldMan())
        with self.assertRaises(Exception) as (e):
            result = G.start_poker(config)
        self.assertIn('only 1 player', str(e.exception))

    @raises(TypeError)
    def test_register_player_when_invalid(self):
        config = G.setup_config(1, 100, 10)
        config.register_player('p1', 'dummy')
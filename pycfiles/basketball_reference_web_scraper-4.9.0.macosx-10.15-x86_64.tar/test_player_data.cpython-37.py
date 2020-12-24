# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/tests/unit/test_player_data.py
# Compiled at: 2020-03-05 11:58:35
# Size of source mod 2**32: 520 bytes
from unittest import TestCase
from basketball_reference_web_scraper.data import PlayerData

class TestPlayerData(TestCase):

    def test_instantiation(self):
        data = PlayerData(name='some name',
          resource_location='some location',
          league_abbreviations=[
         'NBA', 'ABA', 'NBA', 'ABA'])
        self.assertEqual(data.name, 'some name')
        self.assertEqual(data.resource_location, 'some location')
        self.assertEqual(data.league_abbreviations, {'NBA', 'ABA'})
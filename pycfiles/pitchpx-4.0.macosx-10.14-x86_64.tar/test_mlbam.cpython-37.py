# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shinyorke/python_venv/pitchpx/lib/python3.7/site-packages/tests/pitchpx/test_mlbam.py
# Compiled at: 2018-12-12 04:43:08
# Size of source mod 2**32: 773 bytes
from unittest import TestCase, main
from pitchpx.mlbam import MlbAm
__author__ = 'Shinichi Nakagawa'

class TestMlbAm(TestCase):
    __doc__ = '\n    MLBAM scrape class testing\n    '

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_game_number(self):
        """
        Game number Test
        """
        self.assertEqual(MlbAm._get_game_number('gid_2015_08_12_balmlb_seamlb_1/'), 1)
        self.assertEqual(MlbAm._get_game_number('gid_2015_05_06_arimlb_colmlb_1/'), 1)
        self.assertEqual(MlbAm._get_game_number('gid_2015_05_06_arimlb_colmlb_2/'), 2)
        self.assertEqual(MlbAm._get_game_number('gid_2015_09_12_detmlb_clemlb_1_bak/'), 1)


if __name__ == '__main__':
    main()
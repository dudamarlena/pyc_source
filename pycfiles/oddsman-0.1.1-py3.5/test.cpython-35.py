# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/oddsman/test.py
# Compiled at: 2017-06-27 10:57:05
# Size of source mod 2**32: 215 bytes
from oddsman import OddsWatcher
odds_man = OddsWatcher()
todays_race_id = odds_man.get_race_ids('0625')
print(todays_race_id)
race_id = '201702010412'
odds_dict = odds_man.get_race_odds(race_id)
print(odds_dict)
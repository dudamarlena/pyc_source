# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/basketball_reference_web_scraper/errors.py
# Compiled at: 2020-01-27 20:46:58
# Size of source mod 2**32: 889 bytes


class InvalidDate(Exception):

    def __init__(self, day, month, year):
        message = 'Date with year set to {year}, month set to {month}, and day set to {day} is invalid'.format(year=year,
          month=month,
          day=day)
        super().__init__(message)


class InvalidSeason(Exception):

    def __init__(self, season_end_year):
        message = 'Season end year of {season_end_year} is invalid'.format(season_end_year=season_end_year)
        super().__init__(message)


class InvalidPlayerAndSeason(Exception):

    def __init__(self, player_identifier, season_end_year):
        message = 'Player with identifier "{player_identifier}" in season ending in {season_end_year} is invalid'.format(player_identifier=player_identifier,
          season_end_year=season_end_year)
        super().__init__(message)
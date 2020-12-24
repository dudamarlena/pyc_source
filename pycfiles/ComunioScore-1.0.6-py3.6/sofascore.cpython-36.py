# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/score/sofascore.py
# Compiled at: 2020-05-01 18:27:16
# Size of source mod 2**32: 3396 bytes
import logging, requests
from ComunioScore.exceptions import SofascoreRequestError

class SofaScore:
    __doc__ = ' Base class SofaScore to retrieve statistics from  sofascore.com\n\n    USAGE:\n            sofascore = SofaScore()\n            sofascore.get_date_data(date="2019-09-22")\n\n    '

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class SofaScore')
        self.date_url = 'https://www.sofascore.com/football//{date}/json'
        self.event_url = 'https://www.sofascore.com/event/{event_id}/json'
        self.lineups_url = 'https://www.sofascore.com/event/{event_id}/lineups/json'
        self.player_stats_url = 'https://www.sofascore.com/event/{event_id}/player/{player_id}/statistics/json'
        self.season_url = 'http://api.sofascore.com/mobile/v4/unique-tournament/35/season/{season_id}/events'
        self.headers = {'Accept': 'application/json'}

    def __request_api(self, url):
        """ request data from sofascore url

        :param url: specific url depending on requested data

        :return: json dict
        """
        try:
            resp = requests.get(url, headers=(self.headers))
            status_code = resp.status_code
            if status_code == 403:
                raise SofascoreRequestError('Could not load data from Sofascore API')
            json_dict = resp.json()
            return json_dict
        except requests.exceptions.RequestException as ex:
            self.logger.error('Could no retrieve data from Sofascore: {}'.format(ex))
            return {}
        except ValueError as ex:
            self.logger.error(ex)
            return {}

    def get_date_data(self, date):
        """ get data from given date

        :param date: date string: "2019-09-22"
        :return: json dict
        """
        date_url = self.date_url.format(date=date)
        return self._SofaScore__request_api(url=date_url)

    def get_match_data(self, match_id):
        """ get data from given match id

        :param match_id: number for a specific match
        :return: json dict
        """
        match_url = self.event_url.format(event_id=match_id)
        return self._SofaScore__request_api(url=match_url)

    def get_lineups_match(self, match_id):
        """ get squad lineups for given match id

        :param match_id: number for a specific match
        :return: json dict
        """
        lineups_url = self.lineups_url.format(event_id=match_id)
        return self._SofaScore__request_api(url=lineups_url)

    def get_player_stats(self, match_id, player_id):
        """ get stats from given player and match

        :param match_id: id from match
        :param player_id: id from player
        :return: json dict
        """
        player_stats_url = self.player_stats_url.format(event_id=match_id, player_id=player_id)
        return self._SofaScore__request_api(url=player_stats_url)

    def get_season(self, season_id):
        """ get season data from given season_id

        :param season_id: unique id for sofascore
        :return: json dict
        """
        season_url = self.season_url.format(season_id=season_id)
        return self._SofaScore__request_api(url=season_url)
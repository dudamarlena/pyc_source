# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\soccer\core.py
# Compiled at: 2018-02-27 10:04:42
# Size of source mod 2**32: 11574 bytes
""" Central class for the soccer data api. """
import time, datetime, logging
from .data_connectors import FDOConnector, TMConnector
from .writers import BasicWriter, HTMLWriter, JSONWriter, BootstrapWriter
from .exceptions import NoDataConnectorException, SoccerDBNotFoundException
from .util import get_settings, get_current_season, get_season_range, SORT_OPTIONS

class Soccer(object):
    __doc__ = '\n    Central class for the soccer data api.\n    '

    def __init__(self, config_path=None, fdo_apikey=None, writer='basic'):
        self.logger = logging.getLogger(__name__)
        self.dc = None
        if config_path is None:
            config_path = 'soccer.cfg'
        self.season = get_current_season()
        self.settings = get_settings(config_path)
        self.logger.debug(f"Loaded Settings: {self.settings}")
        self._create_data_connectors(fdo_apikey=fdo_apikey, mongo_settings=(self.settings))
        self._get_writer(writer)

    def _create_data_connectors(self, fdo_apikey=None, mongo_settings=None):
        if fdo_apikey is not None:
            self.dc = FDOConnector(fdo_apikey)
        elif mongo_settings is not None:
            try:
                self.dc = TMConnector(mongo_settings)
            except SoccerDBNotFoundException:
                pass

        else:
            self.dc = FDOConnector()

    def _get_writer(self, writer):
        if writer == 'basic':
            self.writer = BasicWriter()
        else:
            if writer == 'json':
                self.writer = JSONWriter()
            else:
                if writer == 'html':
                    self.writer = HTMLWriter()
                else:
                    if writer == 'bootstrap':
                        self.writer = BootstrapWriter()
                    else:
                        self.writer = BasicWriter()

    def get_table(self, league_code, teams=None, timeframe=None, rank=None):
        seasons = self.dc._get_seasons_from_timeframe(timeframe)
        if league_code is None:
            if teams is not None:
                if len(teams) > 0:
                    team_season = self.dc.get_team_by_seasons(teams[0]['team_id'], seasons)
                    if team_season is not None:
                        league_code = team_season['competition']['league_code']
                    else:
                        return
            else:
                return
        else:
            if rank is None:
                if teams is None or not teams:
                    if len(seasons) == 1:
                        return self.writer.league_table(self.dc.get_table(league_code=league_code, timeframe=timeframe))
                    else:
                        return self.writer.multi_table({'title_table':{'name':'Winners', 
                          'table':self.dc.get_title_table(league_code=league_code, timeframe=timeframe)}, 
                         'league_table':{'name':'Aggregated table', 
                          'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}})
                else:
                    if len(teams) == 1:
                        if len(seasons) == 1:
                            return self.writer.rank_table(self.dc.get_table(league_code=league_code, teams=teams, timeframe=timeframe), teams=teams)
                        else:
                            return self.writer.multi_table({'ranks_of_teams':{'name':'Placements', 
                              'table':self.dc.get_ranks_of_teams(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'rank_table':{'name':'Aggregated table', 
                              'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}},
                              teams=teams)
                    else:
                        if len(seasons) == 1:
                            return self.writer.multi_table({'h2h_table':{'name':'Head 2 Head', 
                              'table':self.dc.get_table(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'rank_table':{'name':'Full table', 
                              'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}},
                              teams=teams)
                        else:
                            return self.writer.multi_table({'ranks_of_teams':{'name':'Placements', 
                              'table':self.dc.get_ranks_of_teams(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'h2h_table':{'name':'Head 2 Head table', 
                              'table':self.dc.get_table(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'league_table':{'name':'Full table', 
                              'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}},
                              teams=teams)
            else:
                if teams is None or not teams:
                    if len(seasons) == 1:
                        return self.writer.rank_table(self.dc.get_table(league_code=league_code, teams=teams, timeframe=timeframe), rank=rank, teams=teams)
                    else:
                        return self.writer.multi_table({'title_table':{'name':'Placements', 
                          'table':self.dc.get_title_table(league_code=league_code, timeframe=timeframe, rank=rank)}, 
                         'rank_table':{'name':'Aggregated table', 
                          'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}},
                          rank=rank)
                else:
                    if len(teams) == 1:
                        if len(seasons) == 1:
                            return self.writer.rank_table(self.dc.get_table(league_code=league_code, teams=teams, timeframe=timeframe), rank=rank, teams=teams)
                        else:
                            return self.writer.multi_table({'ranks_of_teams':{'name':'Placements', 
                              'table':self.dc.get_ranks_of_teams(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'rank_table':{'name':'Aggregated table', 
                              'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}},
                              rank=rank,
                              teams=teams)
                    else:
                        if len(seasons) == 1:
                            return self.writer.multi_table({'h2h_table':{'name':'Head 2 Head', 
                              'table':self.dc.get_table(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'rank_table':{'name':'Full table', 
                              'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}},
                              teams=teams)
                        else:
                            return self.writer.multi_table({'ranks_of_teams':{'name':'Placements', 
                              'table':self.dc.get_ranks_of_teams(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'h2h_table':{'name':'Head 2 Head table', 
                              'table':self.dc.get_table(league_code=league_code, teams=teams, timeframe=timeframe)}, 
                             'rank_table':{'name':'Full table', 
                              'table':self.dc.get_table(league_code=league_code, timeframe=timeframe)}},
                              teams=teams,
                              rank=rank)

    def get_fixtures(self, league_code=None, teams=None, timeframe=None, count=None, future=None, home=True, away=True):
        return self.writer.fixture_list(self.dc.get_fixtures(league_code=league_code, teams=teams, timeframe=timeframe, count=count, future=future, home=home, away=away))

    def get_current_matchday(self, competition):
        return self.dc.get_current_matchday(competition)

    def get_titles(self, league_code, teams=None, timeframe=None, rank=None):
        if teams is None:
            return self.writer.title_table(self.dc.get_title_table(league_code=league_code, teams=teams, timeframe=timeframe, rank=rank))
        else:
            return self.writer.ranks_of_teams(self.dc.get_ranks_of_teams(league_code=league_code, teams=teams, timeframe=timeframe))

    def get_goal_table(self, league_code=None, players=None, timeframe=None):
        return self.writer.goal_table(self.dc.get_scorer_table(league_code=league_code, players=players, timeframe=timeframe, goals=True))

    def get_assist_table(self, league_code=None, players=None, timeframe=None):
        return self.writer.assist_table(self.dc.get_scorer_table(league_code=league_code, players=players, timeframe=timeframe, assists=True))

    def get_scorer_table(self, league_code=None, players=None, timeframe=None):
        return self.writer.scorer_table(self.dc.get_scorer_table(league_code=league_code, players=players, timeframe=timeframe, goals=True, assists=True))

    def search_team(self, query):
        return self.dc.search_team(query)

    def search_player(self, query):
        return self.dc.search_player(query)
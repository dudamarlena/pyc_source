# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/base_league.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 3783 bytes
from abc import ABC
from typing import List, Tuple
from .base_settings import BaseSettings
from utils.logger import Logger
from requests.espn_requests import EspnFantasyRequests

class BaseLeague(ABC):
    __doc__ = 'Creates a League instance for Public/Private ESPN league'

    def __init__(self, league_id: int, year: int, sport: str, espn_s2=None, swid=None, username=None, password=None, debug=False):
        self.logger = Logger(name=f"{sport} league", debug=debug)
        self.league_id = league_id
        self.year = year
        self.teams = []
        self.draft = []
        self.player_map = {}
        cookies = None
        if espn_s2:
            if swid:
                cookies = {'espn_s2':espn_s2, 
                 'SWID':swid}
        self.espn_request = EspnFantasyRequests(sport=sport, year=year, league_id=league_id, cookies=cookies, logger=(self.logger))
        if username:
            if password:
                self.espn_request.authentication(username, password)

    def __repr__(self):
        return 'League(%s, %s)' % (self.league_id, self.year)

    def _fetch_league(self, SettingsClass=BaseSettings):
        data = self.espn_request.get_league()
        self.currentMatchupPeriod = data['status']['currentMatchupPeriod']
        self.scoringPeriodId = data['scoringPeriodId']
        self.firstScoringPeriod = data['status']['firstScoringPeriod']
        if self.year < 2018:
            self.current_week = data['scoringPeriodId']
        else:
            self.current_week = self.scoringPeriodId if self.scoringPeriodId <= data['status']['finalScoringPeriod'] else data['status']['finalScoringPeriod']
        self.settings = SettingsClass(data['settings'])
        return data

    def _fetch_teams(self, data, TeamClass):
        """Fetch teams in league"""
        teams = data['teams']
        members = data['members']
        schedule = data['schedule']
        team_roster = {}
        for team in data['teams']:
            team_roster[team['id']] = team['roster']
        else:
            for team in teams:
                for member in members:
                    if not 'owners' not in team:
                        member = team['owners'] or None
                        break
                    else:
                        if member['id'] == team['owners'][0]:
                            break
                        roster = team_roster[team['id']]
                        self.teams.append(TeamClass(team, roster=roster, member=member, schedule=schedule))

            else:
                self.teams = sorted((self.teams), key=(lambda x: x.team_id), reverse=False)

    def _fetch_players(self):
        data = self.espn_request.get_pro_players()
        for player in data:
            self.player_map[player['id']] = player['fullName']

    def _get_pro_schedule(self, scoringPeriodId: int=None):
        data = self.espn_request.get_pro_schedule()
        pro_teams = data['settings']['proTeams']
        pro_team_schedule = {}
        for team in pro_teams:
            if team['id'] != 0 and str(scoringPeriodId) in team['proGamesByScoringPeriod'].keys():
                game_data = team['proGamesByScoringPeriod'][str(scoringPeriodId)][0]
                pro_team_schedule[team['id']] = (game_data['homeProTeamId'], game_data['date']) if team['id'] == game_data['awayProTeamId'] else (game_data['awayProTeamId'], game_data['date'])
            return pro_team_schedule

    def standings(self) -> List:
        standings = sorted((self.teams), key=(lambda x:         if x.final_standing != 0:
x.final_standing # Avoid dead code: x.standing),
          reverse=False)
        return standings
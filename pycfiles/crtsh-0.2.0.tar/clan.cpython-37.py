# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/clan.py
# Compiled at: 2019-12-05 09:43:09
# Size of source mod 2**32: 1110 bytes
from datetime import datetime
import logging, math
from pyroyale import Clan
from crtools import leagueinfo

class ProcessedClan:

    def __init__(self, clan, current_war, config):
        self.tag = clan.tag
        self.name = clan.name
        self.badge_id = clan.badge_id
        self.type = clan.type
        self.clan_score = clan.clan_score
        self.required_trophies = clan.required_trophies
        self.donations_per_week = clan.donations_per_week
        self.clan_war_trophies = clan.clan_war_trophies
        self.clan_chest_level = clan.clan_chest_level
        self.clan_chest_max_level = clan.clan_chest_max_level
        self.members = clan.members
        self.location = clan.location
        self.description = clan.description
        self.clan_chest_status = clan.clan_chest_status
        self.clan_chest_points = clan.clan_chest_points
        self.war_league = leagueinfo.get_war_league_from_score(self.clan_war_trophies)
        self.war_league_name = config['strings'][('war-league-' + self.war_league)]
        self.current_war_state = current_war.state
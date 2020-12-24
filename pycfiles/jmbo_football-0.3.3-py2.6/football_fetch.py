# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football/management/commands/football_fetch.py
# Compiled at: 2013-01-16 06:50:03
import datetime, urllib2
from lxml import etree
from django.db.models import Q
from django.conf import settings
from football365.management.commands.football365_fetch import Command as BaseCommand
from football.models import LeagueGroup, League, Team, LogEntry, Fixture

class Command(BaseCommand):
    pipeline = {'table': ('table_raw', 'xml2dom', 'table_structure', 'table_commit'), 
       'fixtures': ('fixtures_raw', 'xml2dom', 'fixtures_structure', 'fixtures_commit'), 
       'results': ('results_raw', 'xml2dom', 'results_structure', 'results_commit')}

    def table_commit(self, call, data):
        leagues = League.objects.filter(football365_di=call.football365_service_id)
        for league in leagues:
            for obj in league.logentry_set.all():
                obj.delete()

            for row in data:
                try:
                    team = Team.objects.get(Q(football365_teamcode=row['TEAMCODE']) | Q(title=row['TEAM']), leagues=league)
                except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                    continue

                LogEntry.objects.create(league=league, team=team, played=row['PLAYED'], won=row['WON'], drawn=row['DRAWN'], lost=row['LOST'], goals=row['GOALSFOR'], points=row['POINTS'], goal_difference=row['GOALDIFFERENCE'])

        leagues = League.objects.all()
        for league in leagues:
            groups = LeagueGroup.objects.filter(league=league, football365_di=call.football365_service_id)
            for group in groups:
                for obj in league.logentry_set.filter(group=group):
                    obj.delete()

                for row in data:
                    try:
                        team = Team.objects.get(Q(football365_teamcode=row['TEAMCODE']) | Q(title=row['TEAM']), leagues=league)
                    except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                        continue

                    try:
                        logentry = LogEntry.objects.get(league=league, team=team)
                        logentry.group = group
                        logentry.save()
                    except LogEntry.DoesNotExist:
                        LogEntry.objects.create(league=league, group=group, team=team, played=row['PLAYED'], won=row['WON'], drawn=row['DRAWN'], lost=row['LOST'], goals=row['GOALSFOR'], points=row['POINTS'], goal_difference=row['GOALDIFFERENCE'])

    def fixtures_commit(self, call, data):
        leagues = League.objects.filter(football365_di=call.football365_service_id)
        for league in leagues:
            for row in data:
                try:
                    home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                    away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                    continue

                q = league.fixture_set.filter(home_team=home_team, away_team=away_team, datetime=row['STARTTIME'])
                if q.exists():
                    continue
                Fixture.objects.create(league=league, home_team=home_team, away_team=away_team, datetime=row['STARTTIME'])

        leagues = League.objects.all()
        for league in leagues:
            groups = LeagueGroup.objects.filter(league=league, football365_di=call.football365_service_id)
            for group in groups:
                for row in data:
                    try:
                        home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                        away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                    except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                        continue

                    q = league.fixture_set.filter(home_team=home_team, away_team=away_team, datetime=row['STARTTIME'])
                    if q.exists():
                        if q[0].group != group:
                            q[0].group = group
                            q[0].save()
                        continue
                    Fixture.objects.create(league=league, group=group, home_team=home_team, away_team=away_team, datetime=row['STARTTIME'])

    def results_commit(self, call, data):
        leagues = League.objects.filter(football365_di=call.football365_service_id)
        for league in leagues:
            for row in data:
                try:
                    home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                    away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                    continue

                q = league.fixture_set.filter(home_team=home_team, away_team=away_team, datetime__gte=row['DATE'], datetime__lt=row['DATE'] + datetime.timedelta(days=1))
                if q.exists():
                    fixture = q[0]
                    fixture.home_score = row['HOMETEAMSCORE']
                    fixture.away_score = row['AWAYTEAMSCORE']
                    fixture.completed = True
                    fixture.save()
                else:
                    Fixture.objects.create(league=league, home_team=home_team, away_team=away_team, datetime=row['DATE'], home_score=row['HOMETEAMSCORE'], away_score=row['AWAYTEAMSCORE'], completed=True)

        leagues = League.objects.all()
        for league in leagues:
            groups = LeagueGroup.objects.filter(league=league, football365_di=call.football365_service_id)
            for group in groups:
                for row in data:
                    try:
                        home_team = Team.objects.get(Q(football365_teamcode=row['HOMETEAMCODE']) | Q(title=row['HOMETEAM']), leagues=league)
                        away_team = Team.objects.get(Q(football365_teamcode=row['AWAYTEAMCODE']) | Q(title=row['AWAYTEAM']), leagues=league)
                    except (Team.DoesNotExist, Team.MultipleObjectsReturned):
                        continue

                    q = league.fixture_set.filter(home_team=home_team, away_team=away_team, datetime__gte=row['DATE'], datetime__lt=row['DATE'] + datetime.timedelta(days=1))
                    if q.exists():
                        fixture = q[0]
                        fixture.home_score = row['HOMETEAMSCORE']
                        fixture.away_score = row['AWAYTEAMSCORE']
                        fixture.completed = True
                        fixture.group = group
                        fixture.save()
                    else:
                        Fixture.objects.create(league=league, group=group, home_team=home_team, away_team=away_team, datetime=row['DATE'], home_score=row['HOMETEAMSCORE'], away_score=row['AWAYTEAMSCORE'], completed=True)
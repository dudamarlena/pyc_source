# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/serializers.py
# Compiled at: 2015-05-15 22:56:00
# Size of source mod 2**32: 15108 bytes
from __future__ import division
from django.db import transaction
from rest_framework import serializers
from warmama import fields, models

class MatchTeamSerializer(serializers.ModelSerializer):
    __doc__ = 'MatchTeam sub-serializer for MatchResults\n\n    Excluded fields:\n        matchresult\n\n    Extra fields:\n        index (int): Team index in the match, used to associate players with teams\n    '
    index = serializers.IntegerField()

    class Meta:
        model = models.MatchTeam
        exclude = ('matchresult', )


class MatchWeaponSerializer(serializers.ModelSerializer):
    __doc__ = 'MatchWeapon sub-serializer for MatchResults\n\n    Override fields:\n        weapon (str): Name of the weapon\n        acc_strong (float): Handles as a float instead of a Decimal\n        acc_weak (float): Handles as a float instead of a Decimal\n\n    Excluded fields:\n        player, match_result\n    '
    weapon = serializers.CharField(max_length=2)
    acc_strong = serializers.FloatField(required=False)
    acc_weak = serializers.FloatField(required=False)

    class Meta:
        model = models.MatchWeapon
        exclude = ('player', 'matchresult')


class MatchWeaponSetSerializer(serializers.BaseSerializer):
    __doc__ = 'Wrapper for serializing match weapons in the form\n\n    ```\n    {\n        "name": { stats... },\n        "name": { stats... },\n        ...\n    }\n    ```\n    '
    default_error_messages = {'invalid': 'data must be a dictionary', 
     'invalid_weapon': 'Invalid weapon data: {weapon}'}

    def __init__(self, *args, **kwargs):
        self.skip_invalid = kwargs.pop('skip_invalid', False)
        super(MatchWeaponSetSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        """Serialize an iterable of weapons"""
        result = {}
        for weapon in obj:
            weapon_serializer = MatchWeaponSerializer(weapon)
            data = weapon_serializer.data
            name = data.pop('weapon')
            result[name] = data

        return result

    def to_internal_value(self, data):
        """Deserialize data"""
        result = []
        try:
            iterweapons = data.items()
        except AttributeError:
            self.fail('invalid')

        for name, weapon in iterweapons:
            data = weapon.copy()
            data['weapon'] = name
            weapon_serializer = MatchWeaponSerializer(data=data)
            if weapon_serializer.is_valid():
                result.append(weapon_serializer.validated_data)
            elif not self.skip_invalid:
                self.fail('invalid_weapon', weapon=data)
                continue

        return result


class MatchAwardSerializer(serializers.ModelSerializer):
    __doc__ = 'MatchAward sub-serializer for MatchPlayer\n\n    Included fields:\n        count\n\n    Extra fields:\n        name (str): Name of the related award\n    '
    name = serializers.CharField(max_length=64)

    class Meta:
        model = models.MatchAward
        fields = ('name', 'count')


class MatchFragSerializer(serializers.ModelSerializer):
    __doc__ = 'MatchFrag sub-serializer for MatchPlayer\n\n    Override fields:\n        victim (int): Match players based on PlayerSessions\n        weapon (str): Name of the weapon\n\n    Excluded fields:\n        created, matchresult, attacker\n    '
    victim = serializers.PrimaryKeyRelatedField(queryset=models.PlayerSession.objects)
    weapon = serializers.CharField(max_length=2)

    class Meta:
        model = models.MatchFrag
        exclude = ('created', 'matchresult', 'attacker')


class MatchPlayerSerializer(serializers.ModelSerializer):
    __doc__ = 'MatchReport sub-serializer for MatchPlayer objects\n\n    Players are looked up by PlayerSession, not Player pk\n\n    Excluded fields:\n        player, matchresult, matchteam, oldrating, newrating,\n        teamkills, matchtime\n\n    Extra fields:\n        final (int): If falsey, the player quit before the match ended\n        sessionid (int): pk of player session, used to identify player\n        team (int): index of team this player was a member of\n        teamfrags (int): alias for player.teamkills\n        timeplayed (int): alias for player.matchtime\n        weapons (dict): Set of weapon stats for the player, see\n            MatchWeaponSetSerializer for details\n        awards (iterable): Iterable of Awards for the player\n        log_frags (iterable): Iterable of frags for the player\n    '
    final = serializers.IntegerField()
    sessionid = serializers.PrimaryKeyRelatedField(queryset=models.PlayerSession.objects)
    team = serializers.IntegerField(source='matchteam', required=False)
    teamfrags = serializers.IntegerField(source='teamkills', required=False)
    timeplayed = serializers.IntegerField(source='matchtime', min_value=1, required=False)
    weapons = MatchWeaponSetSerializer(required=False)
    awards = MatchAwardSerializer(many=True, required=False)
    log_frags = MatchFragSerializer(many=True, required=False)

    class Meta:
        model = models.MatchPlayer
        exclude = ('player', 'matchresult', 'matchteam', 'oldrating', 'newrating',
                   'teamkills', 'matchtime')


class MatchRaceRunSerializer(serializers.Serializer):
    __doc__ = 'MatchRaceRun sub-serializer for MatchResult\n\n    Fields:\n        session_id (int): PlayerSession for the racer\n        timestamp (int): POSIX Timestamp for the time race was finished\n        times (iterable): Iterable of sector times\n    '
    session_id = serializers.PrimaryKeyRelatedField(queryset=models.PlayerSession.objects)
    timestamp = fields.TimestampField(source='utctime')
    times = serializers.ListField(child=serializers.IntegerField(min_value=0))


class MatchResultSerializer(serializers.ModelSerializer):
    __doc__ = 'Match Result\n\n    Override Fields:\n        gametype (str): Maps to gametype objects by name\n        map (str): Maps to Map objects by name\n\n    Excluded Fields:\n        created, updated, server, uuid, matchtime, utctime, winner_team,\n        winner_player\n\n    Extra fields:\n        hostname (str): TODO I have no idea\n        racegame (bool): True if the game was race\n        timestamp (int): POSIX Timestamp when match finished\n        timeplayed (int): Length of the match in milliseconds\n    '
    gametype = serializers.CharField(max_length=16)
    map = serializers.CharField(max_length=64)
    hostname = serializers.CharField(max_length=128)
    racegame = serializers.BooleanField()
    timeplayed = serializers.IntegerField(min_value=66, source='matchtime')
    timestamp = fields.TimestampField(source='utctime')

    class Meta:
        model = models.MatchResult
        exclude = ('created', 'updated', 'server', 'uuid', 'matchtime', 'utctime',
                   'winner_team', 'winner_player')

    def create(self, validated_data):
        return super(MatchResultSerializer, self).create(validated_data)


class MatchSerializer(serializers.Serializer):
    __doc__ = 'Match Serializer\n\n    Fields:\n        match (dict): MatchResult\n        teams (iterable): MatchTeams\n        players (iterable): MatchPlayers (optional)\n        runs (iterable): RaceRuns (optional)\n    '
    match = MatchResultSerializer()
    teams = MatchTeamSerializer(many=True, required=False)
    players = MatchPlayerSerializer(many=True, required=False)
    runs = MatchRaceRunSerializer(many=True, required=False)

    def _init_cache(self):
        """Create caches for base models"""
        self._award_cache = {}
        self._weapon_cache = {}

    def _create_match_result(self, matchdata, server_id):
        """Create the MatchResult model from matchdata

        This may create a Gametype and Map model if nessecary
        """
        matchdata['gametype'], _ = models.Gametype.objects.get_or_create(name=matchdata['gametype'], defaults={'description': matchdata['gametype']})
        matchdata['map'], _ = models.Map.objects.get_or_create(mapname=matchdata['map'])
        return models.MatchResult.objects.create(server_id=server_id, **matchdata)

    def _create_match_teams(self, teamdata, matchresult):
        """Create Team models for the match

        Creates Team models and returns them in a dict of { teamindex : Team }
        """
        teams = {}
        for team in teamdata:
            index = team.pop('index')
            teams[index] = models.MatchTeam.objects.create(matchresult=matchresult, **team)

        return teams

    def _create_match_players(self, playerdata, matchteams):
        """Create MatchPlayers for the match

        Returns a map { session_id : MatchPlayer }
        """
        players = {}
        for matchplayer in playerdata:
            matchplayer.pop('final')
            player_session = matchplayer.pop('sessionid')
            matchplayer['player_id'] = player_session.user_id
            teamindex = matchplayer.pop('matchteam', None)
            if teamindex is not None:
                matchplayer['matchteam'] = matchteams[teamindex]
            players[player_session.pk] = models.MatchPlayer.objects.create(**matchplayer)

        return players

    def _create_match_awards(self, awarddata):
        """Create MatchAwards for the match

        This will create missing Award models if necessary
        """
        for matchaward in awarddata:
            name = matchaward.pop('name')
            if name not in self._award_cache:
                self._award_cache[name], _ = models.Award.objects.get_or_create(name=name)
            matchaward['award'] = self._award_cache[name]

        models.MatchAward.objects.bulk_create(models.MatchAward(**matchaward) for matchaward in awarddata)

    def _create_match_frags(self, fragdata):
        """Create MatchFrags for the match

        This will create missing Weapon models if necessary
        """
        for matchfrag in fragdata:
            name = matchfrag.pop('weapon')
            if name not in self._weapon_cache:
                self._weapon_cache[name], _ = models.Weapon.objects.get_or_create(name=name, defaults={'fullname': name})
            victim_session = matchfrag.pop('victim')
            matchfrag['victim_id'] = victim_session.user_id
            matchfrag['weapon'] = self._weapon_cache[name]

        models.MatchFrag.objects.bulk_create(models.MatchFrag(**matchfrag) for matchfrag in fragdata)

    def _create_match_weapons(self, weapondata):
        """Create MatchWeapons for the match

        This will create missing Weapon models if necessary
        """
        for matchweapon in weapondata:
            name = matchweapon.pop('weapon')
            if name not in self._weapon_cache:
                self._weapon_cache[name], _ = models.Weapon.objects.get_or_create(name=name, defaults={'fullname': name})
            matchweapon['weapon'] = self._weapon_cache[name]

        models.MatchWeapon.objects.bulk_create(models.MatchWeapon(**matchweapon) for matchweapon in weapondata)

    def _create_runs(self, rundata, map_id, server_id):
        """Create Raceruns and RaceSectors for the match"""
        sectors = []
        for racerun in rundata:
            player_session = racerun.pop('session_id')
            times = sorted(racerun.pop('times'))
            racerun['map_id'] = map_id
            racerun['server_id'] = server_id
            racerun['player_id'] = player_session.user_id
            runobj = models.RaceRun.objects.create(**racerun)
            if not times:
                continue
            sectors.append(models.RaceSector(run=runobj, sector=-1, time=times[(-1)]))
            sectors.extend(models.RaceSector(run=runobj, sector=index, time=time) for index, time in enumerate(times[:-1]))

        models.RaceSector.objects.bulk_create(sectors)

    def _get_player_data(self, playerdata, matchresult):
        """Pull the awards, frags, and weapons out of players

        Returns a tuple `(awards, frags, weapons)` where each entry is a list of
        data for that model. The returned data is ready to be used in the
        relevant `_create_*` method. The argument `playerdata` will be modified
        to have the nested values removed.
        """
        awards = []
        frags = []
        weapons = []
        for player in playerdata:
            pid = player['sessionid'].user_id
            player['matchresult'] = matchresult
            player_awards = player.pop('awards', [])
            player_frags = player.pop('log_frags', [])
            player_weapons = player.pop('weapons', [])
            awards.extend(dict(player_id=pid, matchresult=matchresult, **awd) for awd in player_awards)
            frags.extend(dict(attacker_id=pid, matchresult=matchresult, **frag) for frag in player_frags)
            weapons.extend(dict(player_id=pid, matchresult=matchresult, **weapon) for weapon in player_weapons)

        return (awards, frags, weapons)

    @transaction.atomic
    def create(self, data):
        """Save the validated_data to all the associated model objects"""
        ssession = data.get('server_session', None)
        assert isinstance(ssession, models.ServerSession), 'A valid server session was not provided. Serializer must be savedusing `.save(server_session=ServerSessionObject)`'
        if not 'players' in data:
            assert 'runs' in data, 'No players section or runs section in match'
        if not 'teams' in data:
            assert not data['match'].get('teamgame', True), 'No teams section in match'
        self._init_cache()
        sid = ssession.user_id
        data['match'].pop('hostname', '')
        data['match'].pop('racegame', False)
        matchresult = self._create_match_result(data['match'], sid)
        matchteams = self._create_match_teams(data.get('teams', []), matchresult)
        players = data.get('players', [])
        awards, frags, weapons = self._get_player_data(players, matchresult)
        matchplayers = self._create_match_players(players, matchteams)
        self._create_match_awards(awards)
        self._create_match_frags(frags)
        self._create_match_weapons(weapons)
        self._create_runs(data.get('runs', []), matchresult.map_id, sid)
        self._init_cache()
        return (matchresult, matchplayers)
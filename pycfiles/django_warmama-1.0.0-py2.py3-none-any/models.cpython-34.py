# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/models.py
# Compiled at: 2015-05-16 12:30:25
# Size of source mod 2**32: 24327 bytes
"""Warmama database models"""
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Award(models.Model):
    __doc__ = 'Award\n\n    Attributes:\n        name (str): Name of the map.\n    '
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'awards'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Achievement(models.Model):
    __doc__ = 'Achievement\n\n    Attributes:\n        name (str): Name of the achievement\n        description (str): Description of the achievement\n        numgotten (int): (default: 0) #TODO no idea what this is for\n    '
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    numgotten = models.IntegerField(default=0)

    class Meta:
        db_table = 'achievements'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Gametype(models.Model):
    __doc__ = 'Gametype\n\n    Attributes:\n        name (str): Abbreviated name of the gametype.\n        description (str): Long name of the gametype.\n\n    Reverse lookup attributes:\n        matches (QuerySet): MatchResult objects for every match of the gametype\n    '
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=32)

    class Meta:
        db_table = 'gametypes'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Map(models.Model):
    __doc__ = 'Map\n\n    Attributes:\n        mapname (str): Name of the map\n\n    Reverse lookup attributes:\n        matches (QuerySet): MatchResult objects for every match on the map\n    '
    mapname = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'mapnames'

    def __str__(self):
        return '{0}'.format(self.mapname)


@python_2_unicode_compatible
class Weapon(models.Model):
    __doc__ = 'Weapon\n\n    Attributes:\n        name (str): Abbreviated name of the weapon.\n        fullname (str): Long name of the weapon.\n    '
    name = models.CharField(max_length=2, unique=True)
    fullname = models.CharField(max_length=16)

    class Meta:
        db_table = 'weapons'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Player(models.Model):
    __doc__ = 'Player class\n\n    Attributes:\n        created (datetime): Time when the record was created\n        updated (datetime): Time when the record was last modified\n        login (str): Login username. This field must be unique\n        nickname (str): Ingame nickname with color codes\n        ip (str): IPv4 address\n        ipv6 (str): IPv6 address\n        location (str): Two letter country code\n        banned (bool): Player is banned (default: False)\n\n    Reverse lookup attributes:\n        session (PlayerSession): Session the player is connected with\n        stats (QuerySet): PlayerStat objects for the player\n        achievements (QuerySet): PlayerAchievement objects for the player\n        matches (QuerySet): MatchPlayer objects for the player\n    '
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    login = models.CharField(max_length=64, unique=True)
    nickname = models.CharField(max_length=64, blank=True)
    ip = models.CharField(max_length=22, blank=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    location = models.CharField(max_length=2, blank=True, db_index=True)
    banned = models.BooleanField(default=False)

    class Meta:
        db_table = 'players'

    def __str__(self):
        return '{0}'.format(self.login)


@python_2_unicode_compatible
class Server(models.Model):
    __doc__ = 'Server class\n\n    Attributes:\n        created (datetime): Time when the record was created\n        updated (datetime): Time when the record was last modified\n        login (str): Login username. This field must be unique\n        regip (str): IPv4 address server registered with\n        regipv6 (str): IPv6 address server registered with\n        hostname (str): Hostname\n        ip (str): IPv4 address server logged in with TODO: will this ever differ from regip?\n        ipv6 (str): IPv6 address server logged in with TODO: will this ever differ from regipv6?\n        location (str): Two letter country code\n        banned (bool): Banned (default: False)\n        demos_baseurl (str): `sv_uploads_demos_baseurl` value for server\n\n    Reverse lookup attributes:\n        session (ServerSession): Session the server is connected with\n        matches (QuerySet): MatchResult objects for every match the server hosted\n    '
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    login = models.CharField(max_length=64, unique=True)
    regip = models.CharField(max_length=22, blank=True, db_index=True)
    regipv6 = models.CharField(max_length=54, blank=True)
    hostname = models.CharField(max_length=64, blank=True)
    ip = models.CharField(max_length=22, blank=True, db_index=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    location = models.CharField(max_length=2, blank=True, db_index=True)
    banned = models.BooleanField(default=False)
    demos_baseurl = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = 'servers'

    def __str__(self):
        return '{0}'.format(self.regip)


@python_2_unicode_compatible
class ServerSession(models.Model):
    __doc__ = 'Server session class\n\n    Attributes:\n        created (datetime): Time when the record was created\n        updated (datetime): Time when the record was last modified\n        user (Server): Server the session belongs to\n        ip (str): IPv4 address\n        ipv6 (str): IPv6 address\n        digest (str): #TODO Used for remote authentication?\n        port (int): Port game is being served on.\n        next_match_uuid (str): #TODO No idea what this is for\n    '
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('Server', related_name='session', db_index=True)
    ip = models.CharField(max_length=22, blank=True, db_index=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    digest = models.CharField(default=uuid.uuid4, max_length=36)
    port = models.IntegerField()
    next_match_uuid = models.CharField(max_length=36, blank=True, unique=True)

    class Meta:
        db_table = 'sessions_server'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class PlayerSession(models.Model):
    __doc__ = 'Player session class\n\n    If a player is requesting a connection, `ticket_id`, `ticket_server`, and\n    `ticket_expiration` will be defined and `server_session` will be `None`.\n\n    If a player has connected to a server `ticket_id`, `ticket_server`, and\n    `ticket_expiration` will be `None` and `server_session` will be defined.\n\n    If a player has disconnected, the session is over. All the fields will be\n    `None` and `purgable` will be `True`.\n\n    Attributes:\n        created (datetime): Time when the record was created\n        updated (datetime): Time when the record was last modified\n        user (Player): Player\n        ip (str): IPv4 address\n        ipv6 (str): IPv6 address\n        digest (str): #TODO Used for remote authentication?\n        ticket_id (int): Identifier for the ticket\n        ticket_server (ServerSession): ServerSession that client requested to connect to\n        ticket_expiration (datetime): Time when the ticket expires\n        server_session (ServerSession): ServerSession that client is connected to\n        purgable (bool): True if the session may be purged (default: False)\n\n    Reverse lookup attributes:\n        purge_player (PurgePlayer): Purge object for the session\n    '
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('Player', related_name='session')
    ip = models.CharField(max_length=22, blank=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    digest = models.CharField(default=uuid.uuid4, max_length=32)
    ticket_id = models.IntegerField(default=0, blank=True, null=True)
    ticket_server = models.ForeignKey('ServerSession', blank=True, null=True, db_column='ticket_server', related_name='+', on_delete=models.SET_NULL, db_index=True)
    ticket_expiration = models.DateTimeField(blank=True, null=True)
    server_session = models.ForeignKey('ServerSession', blank=True, null=True, db_column='server_session', related_name='+', on_delete=models.SET_NULL, db_index=True)
    purgable = models.BooleanField(default=False)

    class Meta:
        db_table = 'sessions_player'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class PurgePlayer(models.Model):
    __doc__ = 'Purgable player sessions\n\n    Attributes:\n        created (datetime): Time when the record was created\n        updated (datetime): Time when the record was last modified\n        session (PlayerSession): PlayerSession that may be purged\n        player (Player): Player for the session\n        server_session (ServerSession): ServerSession that marked as purgable\n    '
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    session = models.OneToOneField('PlayerSession', related_name='purge_player', db_index=True)
    player = models.OneToOneField('Player', related_name='+', db_index=True)
    server_session = models.ForeignKey('ServerSession', blank=True, null=True, db_column='server_session', related_name='+', db_index=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'purge_players'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class LoginPlayer(models.Model):
    __doc__ = "Login players\n\n    Attributes:\n        created (datetime): Time when record was created\n        login (str): Player's login name\n        ready (bool): Ready state (default: True)\n        valid (bool): Valid state (default: True)\n        profile_url (str): Url to player profile\n        profile_url_rml (str): Url to player profile in rml format\n    "
    created = models.DateTimeField(auto_now_add=True)
    login = models.CharField(max_length=64, unique=True)
    ready = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)
    profile_url = models.CharField(max_length=255, blank=True)
    profile_url_rml = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'login_players'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class PlayerStat(models.Model):
    __doc__ = "Overall stats for a (player, gametype) pair\n\n    Attributes:\n        player (Player): Player stats belong to\n        created (datetime): Time the record was first created\n        updated (datetime): Time the record was last modified\n        gametype (Gametype): Gametype the stat is for\n        wins (int): Number of wins (default: 0)\n        losses (int): Number of losses (default: 0)\n        quits (int): Number of quits (default: 0)\n        rating (Decimal): Player's rating value (mu) for the gametype (default: 0)\n        deviation (Decimal): Player's rating deviation (sigma) for the gametype (default: 0)\n    "
    player = models.ForeignKey('Player', related_name='stats')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    gametype = models.ForeignKey('Gametype', related_name='+')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    quits = models.IntegerField(default=0)
    rating = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    deviation = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'player_stats'
        unique_together = ('player', 'gametype')

    def __str__(self):
        return '{0} {1}'.format(self.gametype_id, self.player_id)


@python_2_unicode_compatible
class PlayerAchievement(models.Model):
    __doc__ = 'Achievements a player has won\n\n    Attributes:\n        player (Player): Player\n        created (datetime): Time the record was first created\n        updated (datetime): Time the record was last modified\n        achievement (Achievement): Achievement\n    '
    player = models.ForeignKey('Player', related_name='achievements', db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    achievement = models.ForeignKey('Achievement', related_name='+')

    class Meta:
        db_table = 'player_achievements'

    def __str__(self):
        return '{0} {1}'.format(self.achievement_id, self.player_id)


@python_2_unicode_compatible
class MatchResult(models.Model):
    __doc__ = "Match Result\n\n    Attributes:\n        created (datetime): Time the record was first created\n        updated (datetime): Time the record was last modified\n        server (Server): Server the match was hosted on\n        gametype (Gametype): Gametype for the match\n        uuid (str): Unique identifier string for the match result (default: uuid.uuid4)\n        instagib (bool): True if match was instagib (default: False)\n        teamgame (bool): True if match was teamgame (default: False)\n        map_id (int): Pointer to map's pk\n        timelimit (int): Time limit for the match (default: 0)\n        scorelimit (int): Score limit for the match (default: 0)\n        gamedir (str): `fs_game` value for the match\n        matchtime (int): Length of the match in seconds (default: 0)\n        utctime (datetime): Time the match was ended\n        winner_team (MatchTeam): Winning MatchTeam\n        winner_player (MatchPlayer): Winning MatchPlayer\n        demo_filename (str): Name of demo file for the match\n\n    Reverse lookup attributes:\n        teams (QuerySet): MatchTeam objects in the match\n        players (QuerySet): MatchPlayer objects in the match\n        frags (QuerySet): MatchFrag objects in the match\n    "
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    server = models.ForeignKey('Server', related_name='matches', db_index=True)
    gametype = models.ForeignKey('Gametype', related_name='matches', db_index=True)
    uuid = models.CharField(default=uuid.uuid4, max_length=36, unique=True)
    instagib = models.BooleanField(default=False)
    teamgame = models.BooleanField(default=False)
    map = models.ForeignKey('Map', related_name='matches')
    timelimit = models.IntegerField(default=0)
    scorelimit = models.IntegerField(default=0)
    gamedir = models.CharField(max_length=64, blank=True)
    matchtime = models.IntegerField(default=0)
    utctime = models.DateTimeField()
    winner_team = models.ForeignKey('MatchTeam', related_name='+', blank=True, null=True, db_index=True)
    winner_player = models.ForeignKey('MatchPlayer', related_name='+', blank=True, null=True, db_index=True)
    demo_filename = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = 'match_results'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class MatchTeam(models.Model):
    __doc__ = 'Team in a match\n\n    Attributes:\n        matchresult (MatchResult): MatchResult the team was a member of\n        name (str): Name of the team\n        score (int): Score earned by the team (default: 0)\n\n    Reverse lookup attributes:\n        players (QuerySet): MatchPlayer objects in the match\n    '
    matchresult = models.ForeignKey('MatchResult', related_name='teams', db_index=True)
    name = models.CharField(max_length=64)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'match_teams'
        unique_together = ('matchresult', 'name')

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class MatchPlayer(models.Model):
    __doc__ = "Player results in a match\n\n    Attributes:\n        player (Player): Player\n        matchresult (MatchResult): MatchResult\n        matchteam (MatchTeam): MatchTeam\n        name (str): Player's name in match TODO: is this login or nickname?\n        score (int): Score earned (default: 0)\n        frags (int): Frags made (default: 0)\n        deaths (int): Times killed (default: 0)\n        teamkills (int): Betrayal kills (default: 0)\n        suicides (int): Suicides made (default: 0)\n        numrounds (int): Rounds played in the match (default: 0)\n        ga_taken (int): Green armors taken (default: 0)\n        ya_taken (int): Yellow armors taken (default: 0)\n        ra_taken (int): Red armors taken (default: 0)\n        mh_taken (int): Mega healths taken (default: 0)\n        uh_taken (int): Ultra healths taken (default: 0)\n        quads_taken (int): Quad damages taken (default: 0)\n        shells_taken (int): Wsw shells taken (default: 0)\n        bombs_planted (int): Bombs planted (default: 0)\n        bombs_defused (int): Bombs defused (default: 0)\n        flags_capped (int): Flags captured (default: 0)\n        matchtime (int): Playtime in seconds (default: 0)\n        oldrating (Decimal): Player's rating before the match (default: 0)\n        newrating (Decimal): Player's rating after the match (default: 0)\n    "
    player = models.ForeignKey('Player', related_name='matches', db_index=True)
    matchresult = models.ForeignKey('MatchResult', related_name='players', db_index=True)
    matchteam = models.ForeignKey('MatchTeam', related_name='players', blank=True, null=True, db_index=True)
    name = models.CharField(max_length=64, blank=True)
    score = models.IntegerField(default=0)
    frags = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    teamkills = models.IntegerField(default=0)
    suicides = models.IntegerField(default=0)
    numrounds = models.IntegerField(default=0)
    ga_taken = models.IntegerField(default=0)
    ya_taken = models.IntegerField(default=0)
    ra_taken = models.IntegerField(default=0)
    mh_taken = models.IntegerField(default=0)
    uh_taken = models.IntegerField(default=0)
    quads_taken = models.IntegerField(default=0)
    shells_taken = models.IntegerField(default=0)
    bombs_planted = models.IntegerField(default=0)
    bombs_defused = models.IntegerField(default=0)
    flags_capped = models.IntegerField(default=0)
    matchtime = models.IntegerField(default=0)
    oldrating = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    newrating = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'match_players'
        unique_together = ('player', 'matchresult')

    def __str__(self):
        return '{0}'.format(self.player_id)


@python_2_unicode_compatible
class MatchAward(models.Model):
    __doc__ = 'Player awards for a match\n\n    Attributes:\n        player (Player): Player\n        matchresult (MatchResult): MatchResult\n        award (Award): Award\n        count (int): Number of times earned in the match (default: 0)\n    '
    player = models.ForeignKey('Player', related_name='+', db_index=True)
    matchresult = models.ForeignKey('MatchResult', related_name='+', db_index=True)
    award = models.ForeignKey('Award', related_name='+', db_index=True)
    count = models.IntegerField(default=0)

    class Meta:
        db_table = 'match_awards'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class MatchWeapon(models.Model):
    __doc__ = 'Weapon statistics for a player match\n\n    Attributes:\n        player (Player): Player\n        matchresult (MatchResult): MatchResult\n        weapon (Weapon): Weapon\n        shots_strong (int): Number of shots made with strong ammo (default: 0)\n        hits_stong (int): Number of hits made with strong ammo (default: 0)\n        dmg_strong (int): Total damage dealt with strong ammo (default: 0)\n        frags_strong (int): Number of kills made with strong ammo (default: 0)\n        acc_strong (Decimal): Accuracy with strong ammo, hits / shots (default: 0)\n        shots_weak (int): Number of shots made with weak ammo (default: 0)\n        hits_weak (int): Number of hits made with weak ammo (default: 0)\n        dmg_weak (int): Total damage dealt with weak ammo (default: 0)\n        frags_weak (int): Number of kills made with weak ammo (default: 0)\n        acc_weak (Decimal): Accuracy with weak ammo, hits / shots (default: 0)\n    '
    player = models.ForeignKey('Player', related_name='+', db_index=True)
    matchresult = models.ForeignKey('MatchResult', related_name='+', db_index=True)
    weapon = models.ForeignKey('Weapon', related_name='+', db_index=True)
    shots_strong = models.IntegerField(default=0)
    hits_strong = models.IntegerField(default=0)
    dmg_strong = models.IntegerField(default=0)
    frags_strong = models.IntegerField(default=0)
    acc_strong = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    shots_weak = models.IntegerField(default=0)
    hits_weak = models.IntegerField(default=0)
    dmg_weak = models.IntegerField(default=0)
    frags_weak = models.IntegerField(default=0)
    acc_weak = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'match_weapons'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class MatchFrag(models.Model):
    __doc__ = 'Frags made in a match\n\n    Attributes:\n        created (datetime): Time the record was created\n        matchresult (MatchResult): MatchResult\n        attacker (MatchPlayer): attacker\n        victim (MatchPlayer): victim\n        weapon (Weapon): Weapon used in the frag, may be None\n        time (int): match time in seconds the frag was made (default: 0)\n    '
    created = models.DateTimeField(auto_now_add=True)
    matchresult = models.ForeignKey('MatchResult', related_name='frags', db_index=True)
    attacker = models.ForeignKey('Player', related_name='+', db_index=True)
    victim = models.ForeignKey('Player', related_name='+', db_index=True)
    weapon = models.ForeignKey('Weapon', blank=True, null=True, db_index=True)
    time = models.IntegerField(default=0)

    class Meta:
        db_table = 'frag_log'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class RaceRun(models.Model):
    __doc__ = 'Race run\n\n    Attributes:\n        created (datetime): Time when the record was created\n        map (Map): Map\n        server (Server): Server\n        player (Player): Player\n        utctime (datetime): Time when the race was finished\n\n    Reverse lookup attributes:\n        sectors (QuerySet): RaceSectors for the run\n    '
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    map = models.ForeignKey('Map', related_name='+', db_index=True)
    server = models.ForeignKey('Server', related_name='+', db_index=True)
    player = models.ForeignKey('Player', related_name='+', db_index=True)
    utctime = models.DateTimeField()

    class Meta:
        db_table = 'race_runs'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class RaceSector(models.Model):
    __doc__ = 'Race sector / checkpoint\n\n    Attributes:\n        created (datetime): Time the record was created\n        run (RaceRun): RaceRun this belongs to\n        sector (int): Id of the sector on the map, `-1` indicates the total\n            race time.\n        time (int): Time when the sector was crossed in milliseconds (default: 0)\n    '
    created = models.DateTimeField(auto_now_add=True)
    run = models.ForeignKey('RaceRun', related_name='sectors', db_index=True)
    sector = models.IntegerField()
    time = models.IntegerField(default=0, db_index=True)

    class Meta:
        db_table = 'race_sectors'
        unique_together = ('run', 'sector')

    def __str__(self):
        return '{0}'.format(self.pk)
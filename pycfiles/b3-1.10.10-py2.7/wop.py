# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\wop.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'xlr8or'
__version__ = '1.5'
import re, string, b3, b3.events, b3.parsers.punkbuster
from b3.parsers.q3a.abstractParser import AbstractParser

class WopParser(AbstractParser):
    gameName = 'wop'
    privateMsg = False
    PunkBuster = None
    _clientConnectID = None
    _clientConnectGuid = None
    _clientConnectIp = None
    _line_length = 65
    _line_color_prefix = ''
    _commands = {'message': '%(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'addip %(cid)s', 
       'tempban': 'clientkick %(cid)s'}
    _eventmap = {}
    _lineClear = re.compile('^(?:[0-9:]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s(?P<data>(?P<cid>[0-9]+)\\s(?P<cl_guid>[0-9A-Z]{32})\\s+(?P<ip>[0-9.]+):(?P<port>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<acid>[0-9]+)\\s(?P<cid>[0-9]+)\\s(?P<aweap>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s(?P<data>(?P<cid>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>say):\\s*(?P<data>(?P<name>[^:]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>ClientConnect):\\s*(?P<data>(?P<bcid>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>.*)$', re.IGNORECASE))
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\\s+(?P<qport>[0-9]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _reColor = re.compile('(\\^.)|[\\x00-\\x20]|[\\x7E-\\xff]')
    MOD_UNKNOWN = '0'
    MOD_SHOTGUN = '1'
    MOD_GAUNTLET = '2'
    MOD_MACHINEGUN = '3'
    MOD_GRENADE = '4'
    MOD_GRENADE_SPLASH = '5'
    MOD_ROCKET = '6'
    MOD_ROCKET_SPLASH = '7'
    MOD_PLASMA = '8'
    MOD_PLASMA_SPLASH = '9'
    MOD_RAILGUN = '10'
    MOD_LIGHTNING = '11'
    MOD_BFG = '12'
    MOD_BFG_SPLASH = '13'
    MOD_KILLERDUCKS = '14'
    MOD_WATER = '15'
    MOD_SLIME = '16'
    MOD_LAVA = '17'
    MOD_CRUSH = '18'
    MOD_TELEFRAG = '19'
    MOD_FALLING = '20'
    MOD_SUICIDE = '21'
    MOD_TARGET_LASER = '22'
    MOD_TRIGGER_HURT = '23'
    MOD_GRAPPLE = '24'

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.clients.newClient('-1', guid='WORLD', name='World', hide=True, pbid='WORLD')
        if not self.config.has_option('server', 'punkbuster') or self.config.getboolean('server', 'punkbuster'):
            self.PunkBuster = b3.parsers.punkbuster.PunkBuster(self)
        self.debug('Forcing server cvar g_logsync to %s' % self._logSync)
        self.setCvar('g_logsync', self._logSync)
        mapname = self.getMap()
        if mapname:
            self.game.mapName = mapname
            self.info('map is: %s' % self.game.mapName)

    def getLineParts(self, line):
        """
        Parse a log line returning extracted tokens.
        :param line: The line to be parsed
        """
        line = re.sub(self._lineClear, '', line, 1)
        m = None
        for f in self._lineFormats:
            m = re.match(f, line)
            if m:
                break

        if m:
            client = None
            target = None
            return (
             m, m.group('action').lower(), m.group('data').strip(), client, target)
        else:
            self.verbose('Line did not match format: %s' % line)
            return

    def parseUserInfo(self, info):
        """
        Parse an infostring.
        :param info: The infostring to be parsed.
        """
        player_id, info = string.split(info, ' ', 1)
        if info[:1] != '\\':
            info += '\\'
        options = re.findall('\\\\([^\\\\]+)\\\\([^\\\\]+)', info)
        data = dict()
        for o in options:
            data[o[0]] = o[1]

        data['cid'] = player_id
        if 'n' in data:
            data['name'] = data['n']
        t = 0
        if 'team' in data:
            t = data['team']
        elif 't' in data:
            t = data['t']
        data['team'] = self.getTeam(t)
        if 'cl_guid' in data and 'pbid' not in data:
            data['pbid'] = data['cl_guid']
        return data

    def OnClientconnect(self, action, data, match=None):
        try:
            self._clientConnectID = match.group('cid')
        except IndexError:
            try:
                self._clientConnectID = match.group('bcid')
                self._clientConnectGuid = 'BOT' + str(match.group('bcid'))
                self._clientConnectIp = '0.0.0.0'
                self.bot('Bot connected!')
                return
            except IndexError:
                self.error('Parser could not connect client')
                return

        try:
            self._clientConnectGuid = match.group('cl_guid')
        except IndexError:
            self._clientConnectGuid = match.group('ip')

        self._clientConnectIp = match.group('ip')
        self.verbose('Client connected cid: %s, guid: %s, ip: %s' % (self._clientConnectID,
         self._clientConnectGuid,
         self._clientConnectIp))
        return

    def OnClientuserinfochanged(self, action, data, match=None):
        client_id = None
        client = None
        if self._clientConnectID is not None:
            client_id = self._clientConnectID
        self._clientConnectID = None
        bclient = self.parseUserInfo(data)
        self.verbose('Parsed user info %s' % bclient)
        if bclient:
            client = self.clients.getByCID(bclient['cid'])
            if client_id:
                bclient['cl_guid'] = self._clientConnectGuid
                self._clientConnectGuid = None
                bclient['ip'] = self._clientConnectIp
                self._clientConnectIp = None
            if client:
                bclient['cl_guid'] = client.guid
                bclient['ip'] = client.ip
                for k, v in bclient.iteritems():
                    setattr(client, k, v)

            else:
                bot = True if bclient['cl_guid'][:3] == 'BOT' else False
                client = self.clients.newClient(bclient['cid'], name=bclient['name'], ip=bclient['ip'], state=b3.STATE_ALIVE, guid=bclient['cl_guid'], bot=bot, data={'guid': bclient['cl_guid']})
        if client_id:
            return self.getEvent('EVT_CLIENT_JOIN', client=client)
        else:
            return

    def OnClientdisconnect(self, action, data, match=None):
        client = self.clients.getByCID(data)
        if client:
            client.disconnect()
        return

    def OnInitgame(self, action, data, match=None):
        options = re.findall('\\\\([^\\\\]+)\\\\([^\\\\]+)', data)
        for o in options:
            if o[0] == 'mapname':
                self.game.mapName = o[1]
            elif o[0] == 'g_gametype':
                self.game.gameType = self.defineGameType(o[1])
            elif o[0] == 'fs_game':
                self.game.modName = o[1]
            else:
                setattr(self.game, o[0], o[1])

        self.verbose('current gametype: %s' % self.game.gameType)
        self.game.startRound()
        return self.getEvent('EVT_GAME_ROUND_START', self.game)

    def OnSay(self, action, data, match=None):
        msg = string.split(data, ': ', 1)
        if not len(msg) == 2:
            return
        else:
            client = self.clients.getByExactName(msg[0])
            if client:
                self.verbose('Client found: %s' % client.name)
                return self.getEvent('EVT_CLIENT_SAY', msg[1], client)
            self.verbose('No client found!')
            return
            return

    def OnSayteam(self, action, data, match=None):
        msg = string.split(data, ': ', 1)
        if not len(msg) == 2:
            return
        else:
            client = self.clients.getByExactName(msg[0])
            if client:
                self.verbose('Client found: %s' % client.name)
                return self.getEvent('EVT_CLIENT_TEAM_SAY', msg[1], client, client.team)
            self.verbose('No client found!')
            return
            return

    def OnKill(self, action, data, match=None):
        """
         0:   MOD_UNKNOWN, Unknown Means od Death, shouldn't occur at all
         1:   MOD_SHOTGUN, Pumper
         2:   MOD_GAUNTLET, Punchy
         3:   MOD_MACHINEGUN, Nipper
         4:   MOD_GRENADE, Balloony
         5:   MOD_GRENADE_SPLASH, Ballony Splashdamage
         6:   MOD_ROCKET, Betty
         7:   MOD_ROCKET_SPLASH, Betty Splashdamage
         8:   MOD_PLASMA, BubbleG
         9:   MOD_PLASMA_SPLASH, BubbleG Splashdamage
        10:   MOD_RAILGUN, Splasher
        11:   MOD_LIGHTNING, Boaster
        12:   MOD_BFG, Imperius
        13:   MOD_BFG_SPLASH, Imperius Splashdamage
        14:   MOD_KILLERDUCKS, Killerducks
        15:   MOD_WATER, Died in Water
        16:   MOD_SLIME, Died in Slime
        17:   MOD_LAVA, Died in Lava
        18:   MOD_CRUSH, Killed by a Mover
        19:   MOD_TELEFRAG, Killed by a Telefrag
        20:   MOD_FALLING, Died due to falling damage, but there is no falling damage in WoP
        21:   MOD_SUICIDE, Commited Suicide
        22:   MOD_TARGET_LASER, Killed by a laser, which don't exist in WoP
        23:   MOD_TRIGGER_HURT, Killed by a trigger_hurt
        24:   MOD_GRAPPLE, Killed by grapple, not used in WoP
        """
        self.debug('OnKill: %s (%s)' % (match.group('aweap'), match.group('text')))
        victim = self.clients.getByCID(match.group('cid'))
        if not victim:
            self.debug('No victim')
            return None
        else:
            weapon = match.group('aweap')
            if not weapon:
                self.debug('No weapon')
                return None
            if match.group('aweap') in (self.MOD_WATER, self.MOD_LAVA, self.MOD_FALLING, self.MOD_TRIGGER_HURT):
                self.debug('OnKill: water/lava/falling/trigger_hurt should be suicides')
                attacker = victim
            else:
                attacker = self.clients.getByCID(match.group('acid'))
            if not attacker:
                self.debug('No attacker')
                return None
            damagetype = match.group('text').split()[-1:][0]
            if not damagetype:
                self.debug('No damage type, weapon: %s' % weapon)
                return None
            eventkey = 'EVT_CLIENT_KILL'
            if attacker.cid == victim.cid:
                eventkey = 'EVT_CLIENT_SUICIDE'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team:
                eventkey = 'EVT_CLIENT_KILL_TEAM'
            if not hasattr(victim, 'hitloc'):
                victim.hitloc = 'body'
            victim.state = b3.STATE_DEAD
            return self.getEvent(eventkey, (100, weapon, victim.hitloc, damagetype), attacker, victim)

    def OnItem(self, action, data, match=None):
        cid, item = string.split(data, ' ', 1)
        client = self.clients.getByCID(cid)
        if client:
            return self.getEvent('EVT_CLIENT_ITEM_PICKUP', item, client)
        else:
            return

    def defineGameType(self, gametype_int):
        """
        Translate the gametype to a readable format.
        """
        gametype = str(gametype_int)
        if gametype_int == '0':
            gametype = 'dm'
        elif gametype_int == '1':
            gametype = 'lvl'
        elif gametype_int == '2':
            gametype = 'sp'
        elif gametype_int == '3':
            gametype = 'syc-ffa'
        elif gametype_int == '4':
            gametype = 'lps'
        elif gametype_int == '5':
            gametype = 'tdm'
        elif gametype_int == '6':
            gametype = 'ctl'
        elif gametype_int == '7':
            gametype = 'syc-tp'
        elif gametype_int == '8':
            gametype = 'bb'
        return gametype

    def getNextMap(self):
        pass
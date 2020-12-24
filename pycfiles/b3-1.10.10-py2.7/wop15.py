# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\wop15.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'xlr8or, Courgette'
__version__ = '1.6'
import b3, b3.events, b3.parser, re, string
from b3.parsers.q3a.abstractParser import AbstractParser
DEBUG_EVENTS = False
MOD_UNKNOWN = '0'
MOD_PUMPER = '1'
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
GAMETYPE_FFA = '0'
GAMETYPE_1VS1 = '1'
GAMETYPE_SP = '2'
GAMETYPE_SYC = '3'
GAMETYPE_LPS = '4'
GAMETYPE_TFFA = '5'
GAMETYPE_CTL = '6'
GAMETYPE_TSYC = '7'
GAMETYPE_BB = '8'
TEAM_BASED_GAMETYPES = (
 GAMETYPE_TFFA, GAMETYPE_CTL, GAMETYPE_TSYC, GAMETYPE_BB)

class Wop15Parser(AbstractParser):
    gameName = 'wop15'
    _line_length = 65
    _line_color_prefix = ''
    _commands = {'message': 'stell %(cid)s "%(message)s"', 
       'say': 'ssay "%(message)s"', 
       'saybig': 'scp -1 "%(message)s"', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'banAddr %(cid)s', 
       'tempban': 'clientkick %(cid)s'}
    _eventMap = {}
    _lineClear = re.compile('^(?:[0-9:]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s(?P<data>(?P<cid>[0-9]+)\\s(?P<cl_guid>[0-9a-z]{32})\\s+(?P<ip>[0-9.]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s(?P<data>(?P<cid>[0-9]+)\\s+(?P<ip>[0-9.]+))$', re.IGNORECASE),
     re.compile('^(?P<action>Tell):\\s*(?P<data>(?P<cid>[-]?[0-9]+)\\s+(?P<tcid>[0-9]+)\\s+(?P<text>.+))$', re.IGNORECASE),
     re.compile('^(?P<action>Damage):\\s*(?P<data>(?P<cid>[0-9]+)\\s+(?P<aweap>[0-9a-z_]+)\\s+(?P<acid>[0-9]+)\\s+(?P<damage>\\d+)\\s+(?P<meansofdeath>\\d+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<acid>[0-9]+)\\s(?P<aweap>[0-9a-z_]+)\\s(?P<cid>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>.*)$', re.IGNORECASE))
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<team>[0-9]+)\\s+(?P<ping>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+)\\s+(?P<qport>[0-9]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _reColor = re.compile('(\\^.)|[\\x00-\\x20]|[\\x7E-\\xff]')

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.clients.newClient('-1', guid='WORLD', name='World', hide=True)
        self.clients.newClient('1022', guid='ENTITYNUM_WORLD', name='World', hide=True)
        self.debug('Forcing server cvar g_logsync to %s' % self._logSync)
        self.setCvar('g_logsync', self._logSync)
        mapname = self.getMap()
        if mapname:
            self.game.mapName = mapname
            self.info('map is: %s' % self.game.mapName)
        plist = self.getPlayerList()
        for cid, c in plist.iteritems():
            userinfostring = self.queryClientUserInfoByCid(cid)
            if userinfostring:
                self.OnClientuserinfo(None, userinfostring)

        return

    def OnClientconnect(self, action, data, match=None):
        try:
            cid = match.group('cid')
            self.verbose('Client connected cid: %s' % cid)
        except IndexError:
            pass

    def OnClientuserinfochanged(self, action, data, match=None):
        bclient = self.parseUserInfo(data)
        self.verbose('Parsed user info: %s' % bclient)
        if bclient:
            client = self.clients.getByCID(bclient['cid'])
            if client:
                bclient['ip'] = client.ip
                for k, v in bclient.iteritems():
                    setattr(client, k, v)

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

        self.verbose('Current gametype: %s' % self.game.gameType)
        self.game.startRound()
        self.debug('Joining players')
        self.joinPlayers()
        return self.getEvent('EVT_GAME_ROUND_START', self.game)

    def OnSay(self, action, data, match=None):
        msg = string.split(data, ' ', 1)
        if not len(msg) == 2:
            return
        else:
            if msg[0] == '-1':
                return
            else:
                client = self.getByCidOrJoinPlayer(msg[0])
                if client:
                    self.verbose('Client found: %s' % client.name)
                    return self.getEvent('EVT_CLIENT_SAY', msg[1], client)
                self.verbose('No client found')
                return

            return

    def OnSayteam(self, action, data, match=None):
        msg = string.split(data, ' ', 1)
        if not len(msg) == 2:
            return
        else:
            client = self.getByCidOrJoinPlayer(msg[0])
            if client:
                self.verbose('Client found: %s' % client.name)
                return self.getEvent('EVT_CLIENT_TEAM_SAY', msg[1], client, client.team)
            self.verbose('No client found')
            return
            return

    def OnTell(self, action, data, match=None):
        if match is None:
            return
        else:
            cid = match.group('cid')
            client = self.getByCidOrJoinPlayer(cid)
            target = self.getByCidOrJoinPlayer(match.group('tcid'))
            if client and cid != '-1':
                return self.getEvent('EVT_CLIENT_PRIVATE_SAY', match.group('text'), client, target)
            return

    def OnDamage(self, action, data, match=None):
        cid = match.group('cid')
        if not -1 < int(cid) < 64:
            cid = '1022'
        victim = self.clients.getByCID(cid)
        if not victim:
            self.debug('No victim')
            return None
        else:
            acid = match.group('acid')
            if not -1 < int(acid) < 64:
                acid = '1022'
            attacker = self.clients.getByCID(acid)
            if not attacker:
                self.debug('No attacker')
                return None
            if attacker.cid == victim.cid == '1022':
                self.debug('world damaging world -> ignoring')
                return None
            weapon = match.group('aweap')
            if not weapon:
                self.debug('No weapon')
                return None
            eventkey = 'EVT_CLIENT_DAMAGE'
            if attacker.cid == victim.cid:
                eventkey = 'EVT_CLIENT_DAMAGE_SELF'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team and self.game.gameType in TEAM_BASED_GAMETYPES:
                eventkey = 'EVT_CLIENT_DAMAGE_TEAM'
            if not hasattr(victim, 'hitloc'):
                victim.hitloc = 'body'
            damagepoints = float(match.group('damage'))
            return self.getEvent(eventkey, (damagepoints, weapon, victim.hitloc), attacker, victim)

    def OnKill(self, action, data, match=None):
        """
         0:   MOD_UNKNOWN, Unknown Means od Death, shouldn't occur at all
         1:   MOD_PUMPER, Pumper
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
        self.debug('OnKill: %s (%s)' % (match.group('aweap'), match.group('data')))
        cid = match.group('cid')
        if not -1 < int(cid) < 64:
            cid = '1022'
        victim = self.clients.getByCID(cid)
        if not victim:
            self.debug('No victim')
            return None
        else:
            acid = match.group('acid')
            if not -1 < int(acid) < 64:
                acid = '1022'
            attacker = self.clients.getByCID(acid)
            if not attacker:
                self.debug('No attacker')
                return None
            if attacker.cid == victim.cid == '1022':
                self.debug('World damaging world -> ignoring')
                return None
            weapon = match.group('aweap')
            if not weapon:
                self.debug('No weapon')
                return None
            eventkey = 'EVT_CLIENT_KILL'
            if attacker.cid == victim.cid:
                eventkey = 'EVT_CLIENT_SUICIDE'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team and self.game.gameType in TEAM_BASED_GAMETYPES:
                eventkey = 'EVT_CLIENT_KILL_TEAM'
            if not hasattr(victim, 'hitloc'):
                victim.hitloc = 'body'
            victim.state = b3.STATE_DEAD
            return self.getEvent(eventkey, (100, weapon, victim.hitloc), attacker, victim)

    def OnItem(self, action, data, match=None):
        cid, item = string.split(data, ' ', 1)
        client = self.getByCidOrJoinPlayer(cid)
        if client:
            return self.getEvent('EVT_CLIENT_ITEM_PICKUP', item, client)
        else:
            return

    def OnClientuserinfo(self, action, data, match=None):
        bot = False
        bclient = self.parseUserInfo(data)
        self.verbose('Parsed user info: %s' % bclient)
        if 'cl_guid' not in bclient and 'skill' in bclient:
            self.bot('Bot connecting')
            bclient['ip'] = '0.0.0.0'
            bot = True
        if 'cl_guid' in bclient:
            bclient['guid'] = bclient['cl_guid']
        if bclient:
            client = self.clients.getByCID(bclient['cid'])
            if client:
                for k, v in bclient.iteritems():
                    setattr(client, k, v)

            else:
                cid = bclient['cid']
                del bclient['cid']
                client = self.clients.newClient(cid, state=b3.STATE_ALIVE, bot=bot, **bclient)
            self.debug('Client is now: %s' % client)

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
            info = '\\' + info
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
        if 'cl_guid' in data and 'guid' not in data:
            data['guid'] = data['cl_guid']
        return data

    def defineGameType(self, gametype_int):
        """
        Translate the gametype to a readable format.
        """
        gametype = ''
        if gametype_int == GAMETYPE_FFA:
            gametype = 'FFA'
        elif gametype_int == GAMETYPE_1VS1:
            gametype = 'lVSl'
        elif gametype_int == GAMETYPE_SP:
            gametype = 'SP'
        elif gametype_int == GAMETYPE_SYC:
            gametype = 'SYC'
        elif gametype_int == GAMETYPE_LPS:
            gametype = 'LPS'
        elif gametype_int == GAMETYPE_TFFA:
            gametype = 'TFFA'
        elif gametype_int == GAMETYPE_CTL:
            gametype = 'CTL'
        elif gametype_int == GAMETYPE_TSYC:
            gametype = 'TSYC'
        elif gametype_int == GAMETYPE_BB:
            gametype = 'BB'
        return gametype

    def joinPlayers(self):
        """
        Join all the connected clients.
        """
        plist = self.getPlayerList()
        for cid, c in plist.iteritems():
            client = self.clients.getByCID(cid)
            if client:
                self.debug('Joining client: %s' % client.name)
                self.queueEvent(self.getEvent('EVT_CLIENT_JOIN', None, client))

        return

    def queryClientUserInfoByCid(self, cid):
        """
        userinfo 2
        --------
        ip                   192.168.10.1
        syc_color            0
        cl_voip              1
        cg_predictItems      1
        sex                  male
        handicap             100
        team_headmodel       padman
        team_model           padman
        headmodel            padman
        model                padman
        snaps                40
        rate                 25000
        name                 PadPlayer
        cl_guid              98E40E6546546546546546546543D572
        teamoverlay          1
        cg_smoothClients     0
        
        : dumpuser 4
        Player 4 is not on the server
        """
        if not -1 < int(cid) < 64:
            return None
        else:
            data = self.write('dumpuser %s' % cid)
            if not data:
                return None
            if data.split('\n')[0] != 'userinfo':
                self.debug('Dumpuser %s returned : %s' % (cid, data))
                self.debug('Client %s probably disconnected but its character is still hanging in game...' % cid)
                return None
            datatransformed = '%s ' % cid
            for line in data.split('\n'):
                if line.strip() == 'userinfo' or line.strip() == '--------':
                    continue
                var = line[:20].strip()
                val = line[20:].strip()
                datatransformed += '\\%s\\%s' % (var, val)

            return datatransformed

    def getByCidOrJoinPlayer(self, cid):
        if int(cid) > 63:
            self.debug('A client cid cannot be over 63 ! received : %s' % cid)
            return
        else:
            client = self.clients.getByCID(cid)
            if client is None:
                self.debug('Cannot find client by cid %r' % cid)
                self.debug(repr(self.clients))
                userinfostring = self.queryClientUserInfoByCid(cid)
                if userinfostring:
                    self.OnClientuserinfo(None, userinfostring)
                client = self.clients.getByCID(cid)
            return client

    def queueEvent(self, event, expire=10):
        """
        Queue an event for processing.
        :param event: The event to be enqueued
        :param expire: The amount of seconds after which the event will be discarded
        """
        try:
            if DEBUG_EVENTS:
                self.verbose2(event)
        finally:
            return b3.parser.Parser.queueEvent(self, event, expire)

    def getNextMap(self):
        pass
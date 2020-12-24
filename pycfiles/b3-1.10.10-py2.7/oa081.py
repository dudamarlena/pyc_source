# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\oa081.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'Courgette, GrosBedo'
__version__ = '0.14'
import b3, b3.clients, b3.events, re, string
from b3.parsers.q3a.abstractParser import AbstractParser

class Oa081Parser(AbstractParser):
    gameName = 'oa081'
    PunkBuster = None
    _connectingSlots = []
    _empty_name_default = 'EmptyNameDefault'
    _maplist = None
    _line_length = 65
    _line_color_prefix = ''
    _commands = {'message': 'say %(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'banaddr %(cid)s', 
       'tempban': 'clientkick %(cid)s', 
       'banByIp': 'banaddr %(ip)s', 
       'unbanByIp': 'bandel %(cid)s', 
       'banlist': 'listbans'}
    _eventMap = {}
    _lineClear = re.compile('^(?:[0-9:.]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<pbid>[0-9A-Z]{32}):\\s*(?P<name>[^:]+):\\s*(?P<num1>[0-9]+):\\s*(?P<num2>[0-9]+):\\s*(?P<ip>[0-9.]+):(?P<port>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<name>.+):\\s+(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>CTF):\\s+(?P<cid>[0-9]+)\\s+(?P<fid>[0-9]+)\\s+(?P<type>[0-9]+):\\s+(?P<data>.*(?P<color>RED|BLUE).*)$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<acid>[0-9]+)\\s(?P<cid>[0-9]+)\\s(?P<aweap>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>Award):\\s+(?P<cid>[0-9]+)\\s+(?P<awardtype>[0-9]+):\\s+(?P<data>(?P<name>.+) gained the (?P<awardname>\\w+) award!)$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+)\\s(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>tell):\\s(?P<data>(?P<name>.+) to (?P<aname>.+): (?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>sayteam):\\s(?P<data>(?P<name>.+): (?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>Item):\\s+(?P<cid>[0-9]+)\\s+(?P<data>.*)$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z_]\\w*):\\s*(?P<data>.*)$', re.IGNORECASE))
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+)\\s+(?P<qport>[0-9]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _reColor = re.compile('(\\^.)|[\\x00-\\x20]|[\\x7E-\\xff]')
    _reTeamScores = re.compile('^red:(?P<RedScore>.+)\\s+blue:(?P<BlueScore>.+)$', re.IGNORECASE)
    _rePlayerScore = re.compile('^score:\\s+(?P<score>[0-9]+)\\s+ping:\\s+(?P<ping>[0-9]+|CNCT|ZMBI)\\s+client:\\s+(?P<slot>[0-9]+)\\s+(?P<name>.*)$', re.IGNORECASE)
    _reBanList = re.compile('^Ban #(?P<cid>[0-9]+):\\s+(?P<ip>[0-9]+.[0-9]+.[0-9]+.[0-9]+)/(?P<range>[0-9]+)$', re.I)
    MOD_UNKNOWN = 0
    MOD_SHOTGUN = 1
    MOD_GAUNTLET = 2
    MOD_MACHINEGUN = 3
    MOD_GRENADE = 4
    MOD_GRENADE_SPLASH = 5
    MOD_ROCKET = 6
    MOD_ROCKET_SPLASH = 7
    MOD_PLASMA = 8
    MOD_PLASMA_SPLASH = 9
    MOD_RAILGUN = 10
    MOD_LIGHTNING = 11
    MOD_BFG = 12
    MOD_BFG_SPLASH = 13
    MOD_WATER = 14
    MOD_SLIME = 15
    MOD_LAVA = 16
    MOD_CRUSH = 17
    MOD_TELEFRAG = 18
    MOD_FALLING = 19
    MOD_SUICIDE = 20
    MOD_TARGET_LASER = 21
    MOD_TRIGGER_HURT = 22
    MOD_NAIL = 23
    MOD_CHAINGUN = 24
    MOD_PROXIMITY_MINE = 25
    MOD_KAMIKAZE = 26
    MOD_JUICED = 27
    MOD_GRAPPLE = 28
    Suicides = (
     MOD_WATER,
     MOD_SLIME,
     MOD_LAVA,
     MOD_CRUSH,
     MOD_FALLING,
     MOD_SUICIDE,
     MOD_TRIGGER_HURT)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.Events.createEvent('EVT_GAME_FLAG_RETURNED', 'Flag returned')
        self._eventMap['warmup'] = self.getEventID('EVT_GAME_WARMUP')
        self._eventMap['restartgame'] = self.getEventID('EVT_GAME_ROUND_END')
        self.clients.newClient('1022', guid='WORLD', name='World', hide=True, pbid='WORLD')
        mapname = self.getMap()
        if mapname:
            self.game.mapName = mapname
            self.info('map is: %s' % self.game.mapName)
        try:
            fs_game = self.getCvar('fs_game').getString()
            if fs_game == '':
                fs_game = 'baseoa'
            self.game.fs_game = fs_game
            self.game.modName = fs_game
            self.debug('fs_game: %s' % self.game.fs_game)
        except Exception:
            self.game.fs_game = None
            self.game.modName = None
            self.warning('Could not query server for fs_game')

        try:
            self.game.fs_basepath = self.getCvar('fs_basepath').getString().rstrip('/')
            self.debug('fs_basepath: %s' % self.game.fs_basepath)
        except Exception:
            self.game.fs_basepath = None
            self.warning('Could not query server for fs_basepath')

        try:
            self.game.fs_homepath = self.getCvar('fs_homepath').getString().rstrip('/')
            self.debug('fs_homepath: %s' % self.game.fs_homepath)
        except Exception:
            self.game.fs_homepath = None
            self.warning('Could not query server for fs_homepath')

        try:
            self.game.gameType = self.defineGameType(self.getCvar('g_gametype').getString())
            self.debug('g_gametype: %s' % self.game.gameType)
        except Exception:
            self.game.gameType = None
            self.warning('Could not query server for g_gametype')

        self.info('Discover connected clients')
        plist = self.getPlayerList()
        for cid, c in plist.iteritems():
            userinfostring = self.queryClientUserInfoByCid(cid)
            if userinfostring:
                self.OnClientuserinfochanged(None, userinfostring)

        return

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
                self.debug('XLR--------> line matched %s' % f.pattern)
                break

        if m:
            client = None
            target = None
            try:
                action = m.group('action').lower()
            except IndexError:
                action = 'damage'

            return (
             m, action, m.group('data').strip(), client, target)
        else:
            if '------' not in line:
                self.verbose('XLR--------> line did not match format: %s' % line)
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
        t = -1
        if 'team' in data:
            t = data['team']
        elif 't' in data:
            t = data['t']
        data['team'] = self.getTeam(t)
        if 'id' in data:
            data['guid'] = data['id']
            del data['id']
        if 'cl_guid' in data:
            data['guid'] = data['cl_guid']
        return data

    def OnClientconnect(self, action, data, match=None):
        client = self.clients.getByCID(data)
        self.debug('OnClientConnect: %s, %s' % (data, client))
        return self.getEvent('EVT_CLIENT_JOIN', client=client)

    def OnClientuserinfochanged(self, action, data, match=None):
        if data is None:
            return
        else:
            bclient = self.parseUserInfo(data)
            self.verbose('Parsed user info: %s' % bclient)
            if bclient:
                cid = bclient['cid']
                if cid in self._connectingSlots:
                    self.debug('Client on slot %s is already being connected' % cid)
                    return
                self._connectingSlots.append(cid)
                client = self.clients.getByCID(cid)
                if client:
                    for k, v in bclient.iteritems():
                        setattr(client, k, v)

                else:
                    if 'name' not in bclient:
                        bclient['name'] = self._empty_name_default
                    if 'guid' in bclient:
                        guid = bclient['guid']
                    else:
                        if 'skill' in bclient:
                            guid = 'BOT' + str(cid)
                            self.verbose('BOT connected!')
                            self.clients.newClient(cid, name=bclient['name'], ip='0.0.0.0', state=b3.STATE_ALIVE, guid=guid, data={'guid': guid}, team=bclient['team'], bot=True, money=20)
                            self._connectingSlots.remove(cid)
                            return
                        else:
                            self.info('We are missing the guid but this is not a bot either, dumpuser')
                            self._connectingSlots.remove(cid)
                            self.OnClientuserinfochanged(None, self.queryClientUserInfoByCid(cid))
                            return

                    if 'ip' not in bclient:
                        infoclient = self.parseUserInfo(self.queryClientUserInfoByCid(cid))
                        if 'ip' in infoclient:
                            bclient['ip'] = infoclient['ip']
                        else:
                            self.warning('Failed to get client ip')
                    if 'ip' in bclient:
                        self.clients.newClient(cid, name=bclient['name'], ip=bclient['ip'], state=b3.STATE_ALIVE, guid=guid, data={'guid': guid}, team=bclient['team'], bot=False, money=20)
                    else:
                        self.warning('Failed to get connect client')
                self._connectingSlots.remove(cid)
            return

    def OnKill(self, action, data, match=None):
        self.debug('OnKill: %s (%s)' % (match.group('aweap'), match.group('text')))
        victim = self.getByCidOrJoinPlayer(match.group('cid'))
        if not victim:
            self.debug('No victim')
            return None
        else:
            weapon = match.group('aweap')
            if not weapon:
                self.debug('No weapon')
                return None
            if match.group('aweap') in self.Suicides:
                self.debug('OnKill: fixed attacker, suicide detected: %s' % match.group('text'))
                attacker = victim
            else:
                attacker = self.getByCidOrJoinPlayer(match.group('acid'))
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
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team != b3.TEAM_FREE and attacker.team == victim.team:
                eventkey = 'EVT_CLIENT_KILL_TEAM'
            if not hasattr(victim, 'hitloc'):
                victim.hitloc = 'body'
            victim.state = b3.STATE_DEAD
            return self.getEvent(eventkey, (100, weapon, victim.hitloc, damagetype), attacker, victim)

    def OnClientdisconnect(self, action, data, match=None):
        client = self.clients.getByCID(data)
        if client:
            client.disconnect()
        return

    def OnInitgame(self, action, data, match=None):
        self.debug('OnInitgame: %s' % data)
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

        self.verbose('...self.console.game.gameType: %s' % self.game.gameType)
        self.game.startRound()
        self.debug('Synchronizing client info...')
        self.clients.sync()
        return self.getEvent('EVT_GAME_ROUND_START', data=self.game)

    def OnSayteam(self, action, data, match=None):
        client = self.clients.getByExactName(match.group('name'))
        if not client:
            self.verbose('No client found')
            return None
        else:
            data = match.group('text')
            client.name = match.group('name')
            return self.getEvent('EVT_CLIENT_TEAM_SAY', data, client, -1)

    def OnTell(self, action, data, match=None):
        client = self.clients.getByExactName(match.group('name'))
        tclient = self.clients.getByExactName(match.group('aname'))
        if not client:
            self.verbose('No client found')
            return None
        else:
            data = match.group('text')
            if data and ord(data[:1]) == 21:
                data = data[1:]
            client.name = match.group('name')
            return self.getEvent('EVT_CLIENT_PRIVATE_SAY', data, client, tclient)

    def OnAction(self, cid, actiontype, data, match=None):
        client = self.clients.getByCID(cid)
        if not client:
            self.debug('No client found')
            return None
        else:
            self.verbose('OnAction: %s: %s %s' % (client.name, actiontype, data))
            return self.getEvent('EVT_CLIENT_ACTION', actiontype, client)

    def OnItem(self, action, data, match=None):
        client = self.getByCidOrJoinPlayer(match.group('cid'))
        if client:
            return self.getEvent('EVT_CLIENT_ITEM_PICKUP', match.group('data'), client)
        else:
            return

    def OnCtf(self, action, data, match=None):
        cid = match.group('cid')
        client = self.getByCidOrJoinPlayer(match.group('cid'))
        flagteam = self.getTeam(match.group('fid'))
        flagcolor = match.group('color')
        action_types = {'0': 'flag_taken', 
           '1': 'flag_captured', 
           '2': 'flag_returned', 
           '3': 'flag_carrier_kill'}
        try:
            action_id = action_types[match.group('type')]
        except KeyError:
            action_id = 'flag_action_' + match.group('type')
            self.debug('Unknown CTF action type: %s (%s)' % (match.group('type'), match.group('data')))

        self.debug('CTF Event: %s from team %s %s by %s' % (action_id, flagcolor, flagteam, client.name))
        if action_id == 'flag_returned':
            return self.getEvent('EVT_GAME_FLAG_RETURNED', flagcolor)
        else:
            return self.OnAction(cid, action_id, data)

    def OnAward(self, action, data, match=None):
        client = self.getByCidOrJoinPlayer(match.group('cid'))
        action_type = 'award_%s' % match.group('awardname')
        return self.getEvent('EVT_CLIENT_ACTION', action_type, client)

    def getTeam(self, team):
        """
        Return a B3 team given the team value.
        :param team: The team value
        """
        team = str(team).lower()
        if team == 'free' or team == '0':
            result = b3.TEAM_FREE
        elif team == 'red' or team == '1':
            result = b3.TEAM_RED
        elif team == 'blue' or team == '2':
            result = b3.TEAM_BLUE
        elif team == 'spectator' or team == '3':
            result = b3.TEAM_SPEC
        else:
            result = b3.TEAM_UNKNOWN
        return result

    def defineGameType(self, gametype_int):
        """
        Translate the gametype to a readable format (also for teamkill plugin!).
        """
        gametype = str(gametype_int)
        if gametype_int == '0':
            gametype = 'dm'
        elif gametype_int == '1':
            gametype = 'du'
        elif gametype_int == '3':
            gametype = 'tdm'
        elif gametype_int == '4':
            gametype = 'ctf'
        elif gametype_int == '8':
            gametype = 'el'
        elif gametype_int == '9':
            gametype = 'ctfel'
        elif gametype_int == '10':
            gametype = 'lms'
        elif gametype_int == '11':
            gametype = 'del'
        elif gametype_int == '12':
            gametype = 'dom'
        return gametype

    def connectClient(self, ccid):
        players = self.getPlayerList()
        self.verbose('connectClient() = %s' % players)
        for cid, p in players.iteritems():
            if int(cid) == int(ccid):
                self.debug('Client found in status/playerList')
                return p

    def getByCidOrJoinPlayer(self, cid):
        client = self.clients.getByCID(cid)
        if client:
            return client
        else:
            userinfostring = self.queryClientUserInfoByCid(cid)
            if userinfostring:
                self.OnClientuserinfochanged(None, userinfostring)
            return self.clients.getByCID(cid)
            return

    def queryClientUserInfoByCid(self, cid):
        """
        : dumpuser 5
        Player 5 is not on the server

        ]
con dumpuser 0
        userinfo
        --------
        ip                  81.56.143.41
        cg_cmdTimeNudge     0
        cg_delag            0
        cg_scorePlums       1
        cl_voip             0
        cg_predictItems     1
        cl_anonymous        0
        sex                 male
        handicap            100
        color2              7
        color1              2
        team_headmodel      sarge/classic
        team_model          sarge/classic
        headmodel           sarge/classic
        model               sarge/classic
        snaps               20
        rate                25000
        name                Courgette
        teamtask            0
        cl_guid             201AB4BBC40B4EC7445B49CE82D209EC
        teamoverlay         0
        """
        data = self.write('dumpuser %s' % cid)
        if not data:
            return None
        else:
            if data.split('\n')[0] != 'userinfo':
                self.debug('dumpuser %s returned : %s' % (cid, data))
                return None
            datatransformed = '%s ' % cid
            for line in data.split('\n'):
                if line.strip() == 'userinfo' or line.strip() == '--------':
                    continue
                var = line[:20].strip()
                val = line[20:].strip()
                datatransformed += '\\%s\\%s' % (var, val)

            return datatransformed

    def getMaps(self):
        """
        Return the available maps/levels name
        """
        if self._maplist is not None:
            return self._maplist
        else:
            data = self.write('fdir *.bsp')
            if not data:
                return []
            mapregex = re.compile('^maps/(?P<map>.+)\\.bsp$', re.I)
            maps = []
            for line in data.split('\n'):
                m = re.match(mapregex, line.strip())
                if m:
                    if m.group('map'):
                        maps.append(m.group('map'))

            return maps

    def getNextMap(self):
        """
        Return the next map/level name to be played.
        """
        data = self.write('nextmap')
        nextmap = self.findNextMap(data)
        if nextmap:
            return nextmap
        else:
            return 'no nextmap set or it is in an unrecognized format !'

    def findNextMap(self, data):
        self.debug('extracting nextmap name from: %s' % data)
        nextmapregex = re.compile('.*("|;)\\s*((?P<vstr>vstr (?P<vstrnextmap>[a-z0-9_]+))|(?P<map>map (?P<mapnextmap>[a-z0-9_]+)))', re.IGNORECASE)
        m = re.match(nextmapregex, data)
        if m:
            if m.group('map'):
                self.debug('found nextmap: %s' % m.group('mapnextmap'))
                return m.group('mapnextmap')
            if m.group('vstr'):
                self.debug('nextmap is redirecting to var: %s' % m.group('vstrnextmap'))
                data = self.write(m.group('vstrnextmap'))
                result = self.findNextMap(data)
                if result:
                    return result
                nextmapregex = re.compile('.*("|;)\\s*(?P<map>map (?P<mapnextmap>[a-z0-9_]+))"', re.IGNORECASE)
                m = re.match(nextmapregex, data)
                if m.group('map'):
                    self.debug('found nextmap: %s' % m.group('mapnextmap'))
                    return m.group('mapnextmap')
                self.debug('no nextmap found in this string!')
                return
        else:
            self.debug('no nextmap found in this string!')
            return
        return

    def rotateMap(self):
        """
        Load the next map/level
        """
        self.write('vstr nextmap')

    def ban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Ban a given client.
        :param client: The client to ban
        :param reason: The reason for this ban
        :param admin: The admin who performed the ban
        :param silent: Whether or not to announce this ban
        """
        self.debug('BAN : client: %s, reason: %s', client, reason)
        if isinstance(client, b3.clients.Client) and not client.guid:
            return self.kick(client, reason, admin, silent)
        else:
            if isinstance(client, str) and re.match('^[0-9]+$', client):
                self.write(self.getCommand('ban', cid=client, reason=reason))
                return
            if not client.id:
                self.error('Q3AParser.ban(): no client id, database must be down, doing tempban')
                return self.tempban(client, reason, '1d', admin, silent)
            if admin:
                variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
                fullreason = self.getMessage('banned_by', variables)
            else:
                variables = self.getMessageVariables(client=client, reason=reason)
                fullreason = self.getMessage('banned', variables)
            if client.cid is None:
                self.debug('EFFECTIVE BAN : %s', self.getCommand('banByIp', ip=client.ip, reason=reason))
                self.write(self.getCommand('banByIp', ip=client.ip, reason=reason))
            else:
                self.debug('EFFECTIVE BAN : %s', self.getCommand('ban', cid=client.cid, reason=reason))
                self.write(self.getCommand('ban', cid=client.cid, reason=reason))
            if not silent and fullreason != '':
                self.say(fullreason)
            self.queueEvent(self.getEvent('EVT_CLIENT_BAN', {'reason': reason, 'admin': admin}, client))
            client.disconnect()
            return

    def unban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Unban a client.
        :param client: The client to unban
        :param reason: The reason for the unban
        :param admin: The admin who unbanned this client
        :param silent: Whether or not to announce this unban
        """
        data = self.write(self.getCommand('banlist', cid=-1))
        if not data:
            self.debug('ERROR: unban cannot be done, no ban list returned')
        else:
            for line in data.split('\n'):
                m = re.match(self._reBanList, line.strip())
                if m:
                    if m.group('ip') == client.ip:
                        self.write(self.getCommand('unbanByIp', cid=m.group('cid'), reason=reason))
                        self.debug('EFFECTIVE UNBAN : %s', self.getCommand('unbanByIp', cid=m.group('cid')))
                if admin:
                    variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
                    fullreason = self.getMessage('unbanned_by', variables)
                else:
                    variables = self.getMessageVariables(client=client, reason=reason)
                    fullreason = self.getMessage('unbanned', variables)
                if not silent and fullreason != '':
                    self.say(fullreason)

    def getPlayerPings(self, filter_client_ids=None):
        """
        Returns a dict having players' id for keys and players' ping for values.
        :param filter_client_ids: If filter_client_id is an iterable, only return values for the given client ids.
        """
        data = self.write('status')
        if not data:
            return {}
        players = {}
        for line in data.split('\n'):
            m = re.match(self._regPlayer, line.strip())
            if m:
                if m.group('ping') == 'ZMBI':
                    pass
                else:
                    players[str(m.group('slot'))] = int(m.group('ping'))

        return players

    def sync(self):
        """
        For all connected players returned by self.get_player_list(), get the matching Client
        object from self.clients (with self.clients.get_by_cid(cid) or similar methods) and
        look for inconsistencies. If required call the client.disconnect() method to remove
        a client from self.clients.
        """
        plist = self.getPlayerList()
        mlist = dict()
        for cid, c in plist.iteritems():
            client = self.getByCidOrJoinPlayer(cid)
            if client:
                if client.guid and 'guid' in c.keys():
                    if client.guid == c['guid']:
                        self.debug('in-sync %s == %s', client.guid, c['guid'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s', client.guid, c['guid'])
                        client.disconnect()
                elif client.ip and 'ip' in c.keys():
                    if client.ip == c['ip']:
                        self.debug('in-sync %s == %s', client.ip, c['ip'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s', client.ip, c['ip'])
                        client.disconnect()
                else:
                    self.debug('no-sync: no guid or ip found')

        return mlist
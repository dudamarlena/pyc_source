# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\smg.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'xlr8or, Courgette'
__version__ = '0.1.8'
import b3, b3.events, b3.parsers.punkbuster, re, string, threading
from b3.parsers.q3a.abstractParser import AbstractParser

class SmgParser(AbstractParser):
    gameName = 'smg'
    PunkBuster = None
    _counter = {}
    _empty_name_default = 'EmptyNameDefault'
    _logSync = 1
    _maplist = None
    _clientConnectID = None
    _clientConnectGuid = None
    _clientConnectIp = None
    _line_length = 65
    _line_color_prefix = ''
    _commands = {'message': '%(cid)s %(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'banClient %(cid)s', 
       'tempban': 'clientkick %(cid)s'}
    _eventMap = {}
    _lineClear = re.compile('^(?:[0-9:.]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<pbid>[0-9A-Z]{32}):\\s*(?P<name>[^:]+):\\s*(?P<num1>[0-9]+):\\s*(?P<num2>[0-9]+):\\s*(?P<ip>[0-9.]+):(?P<port>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<name>.+):\\s+(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<acid>[0-9]+)\\s(?P<cid>[0-9]+)\\s(?P<aweap>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+)\\s(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z_]+):\\s*(?P<data>.*)$', re.IGNORECASE))
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\\s+(?P<qport>[0-9]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _reColor = re.compile('(\\^.)|[\\x00-\\x20]|[\\x7E-\\xff]')
    MOD_UNKNOWN = '0'
    MOD_KNIFE = '1'
    MOD_REM58 = '2'
    MOD_SCHOFIELD = '3'
    MOD_PEACEMAKER = '4'
    MOD_WINCHESTER66 = '5'
    MOD_LIGHTNING = '6'
    MOD_SHARPS = '7'
    MOD_REMINGTON_GAUGE = '8'
    MOD_SAWEDOFF = '9'
    MOD_WINCH97 = '10'
    MOD_GATLING = '11'
    MOD_DYNAMITE = '12'
    MOD_MOLOTOV = '13'
    MOD_WATER = '14'
    MOD_SLIME = '15'
    MOD_LAVA = '16'
    MOD_CRUSH = '17'
    MOD_TELEFRAG = '18'
    MOD_FALLING = '19'
    MOD_SUICIDE = '20'
    MOD_WORLD_DAMAGE = '21'
    MOD_TRIGGER_HURT = '22'
    MOD_NAIL = '23'
    MOD_CHAINGUN = '24'
    MOD_PROXIMITY_MINE = '25'
    MOD_BOILER = '26'
    Suicides = (
     MOD_WATER,
     MOD_SLIME,
     MOD_LAVA,
     MOD_CRUSH,
     MOD_TELEFRAG,
     MOD_FALLING,
     MOD_SUICIDE,
     MOD_TRIGGER_HURT,
     MOD_NAIL,
     MOD_CHAINGUN,
     MOD_PROXIMITY_MINE,
     MOD_BOILER)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.clients.newClient('-1', guid='WORLD', name='World', hide=True, pbid='WORLD')
        self._eventMap['warmup'] = self.getEventID('EVT_GAME_WARMUP')
        self._eventMap['restartgame'] = self.getEventID('EVT_GAME_ROUND_END')
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
        if 'ip' in data:
            tip = string.split(data['ip'], ':', 1)
            data['ip'] = tip[0]
            data['port'] = tip[1]
        t = 0
        if 'team' in data:
            t = data['team']
        elif 't' in data:
            t = data['t']
        data['team'] = self.getTeam(t)
        if 'cl_guid' in data:
            data['cl_guid'] = data['cl_guid'].lower()
        if 'pbid' in data:
            data['pbid'] = data['pbid'].lower()
        if 'cl_guid' in data and 'pbid' not in data:
            data['pbid'] = data['cl_guid']
        return data

    def OnClientconnect(self, action, data, match=None):
        self._clientConnectID = data
        client = self.clients.getByCID(data)
        return self.getEvent('EVT_CLIENT_JOIN', client=client)

    def OnClientuserinfo(self, action, data, match=None):
        bclient = self.parseUserInfo(data)
        self.verbose('Parsed user info: %s' % bclient)
        if bclient:
            cid = bclient['cid']
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
                    guid = 'BOT' + str(cid)
                    self.verbose('bot connected!')
                    self.clients.newClient(cid, name=bclient['name'], ip='0.0.0.0', state=b3.STATE_ALIVE, guid=guid, bot=True, data={'guid': guid})
                    return
                self._counter[cid] = 1
                t = threading.Timer(2, self.newPlayer, (cid, guid, bclient['name']))
                t.start()
                self.debug('%s connected, waiting for authentication...' % bclient['name'])
                self.debug('our authentication queue: %s' % str(self._counter))
        return

    def OnKill(self, action, data, match=None):
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
            if match.group('aweap') in self.Suicides:
                self.debug('OnKill: fixed attacker, suicide detected: %s' % match.group('text'))
                attacker = victim
            else:
                attacker = self.clients.getByCID(match.group('acid'))
            if not attacker:
                self.debug('No attacker')
                return None
            damagetype = match.group('text').split()[-1:][0]
            if not damagetype:
                self.debug('no damage type, weapon: %s' % weapon)
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

        self.verbose('...self.console.game.gameType: %s' % self.game.gameType)
        self.game.startRound()
        self.debug('synchronizing client info')
        self.clients.sync()
        return self.getEvent('EVT_GAME_ROUND_START', self.game)

    def OnSayteam(self, action, data, match=None):
        return self.OnSay(action, data, match)

    def getTeam(self, team):
        """
        Return a B3 team given the team value.
        :param team: The team value
        """
        if team == 'red':
            team = 1
        if team == 'blue':
            team = 2
        team = int(team)
        if team == 1:
            return b3.TEAM_RED
        else:
            if team == 2:
                return b3.TEAM_BLUE
            if team == 3:
                return b3.TEAM_SPEC
            return b3.TEAM_UNKNOWN

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
            gametype = 'ts'
        elif gametype_int == '5':
            gametype = 'br'
        return gametype

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
                self.debug('no nextmap found in this string')
                return
        else:
            self.debug('no nextmap found in this string')
            return
        return

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
            client = self.clients.getByCID(cid)
            if client:
                if client.guid and 'guid' in c:
                    if client.guid == c['guid']:
                        self.debug('in-sync %s == %s', client.guid, c['guid'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s', client.guid, c['guid'])
                        client.disconnect()
                elif client.ip and 'ip' in c:
                    if client.ip == c['ip']:
                        self.debug('in-sync %s == %s', client.ip, c['ip'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s', client.ip, c['ip'])
                        client.disconnect()
                else:
                    self.debug('no-sync: no guid or ip found')

        return mlist

    def connectClient(self, ccid):
        s = 'status'
        if self.PunkBuster:
            s = 'punkbuster'
        self.debug('getting the (%s) playerlist' % s)
        players = self.getPlayerList()
        self.verbose('connectClient() = %s' % players)
        for cid, p in players.iteritems():
            if int(cid) == int(ccid):
                self.debug('client found in status/playerList')
                return p

    def newPlayer(self, cid, guid, name):
        if not self._counter.get(cid):
            self.verbose('newPlayer thread no longer needed: key no longer available')
            return
        else:
            if self._counter.get(cid) == 'Disconnected':
                self.debug('%s disconnected: removing from authentication queue' % name)
                self._counter.pop(cid)
                return
            self.debug('newPlayer: %s, %s, %s' % (cid, guid, name))
            sp = self.connectClient(cid)
            if sp:
                ip = sp['ip']
                self.verbose('ip = %s' % ip)
                self._counter.pop(cid)
            else:
                if self._counter[cid] > 10:
                    self.debug('couldn not auth %s: giving up...' % name)
                    self._counter.pop(cid)
                    return
                else:
                    self.debug('%s not yet fully connected: retrying...#:%s' % (name, self._counter[cid]))
                    self._counter[cid] += 1
                    t = threading.Timer(4, self.newPlayer, (cid, guid, name))
                    t.start()
                    return

            self.clients.newClient(cid, name=name, ip=ip, state=b3.STATE_ALIVE, guid=guid, bot=False, data={'guid': guid})
            return
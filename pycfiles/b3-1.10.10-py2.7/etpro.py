# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\etpro.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'xlr8or, ailmanki'
__version__ = '0.0.11'
import re, string, b3, b3.clients, b3.events, b3.parsers.punkbuster
from b3.functions import prefixText
from b3.parsers.q3a.abstractParser import AbstractParser

class EtproParser(AbstractParser):
    gameName = 'etpro'
    PunkBuster = None
    IpsOnly = False
    IpCombi = False
    _empty_name_default = 'EmptyNameDefault'
    _logSync = 2
    _commands = {'message': 'm %(name)s %(message)s', 
       'say': 'cpmsay %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'banid %(cid)s', 
       'tempban': 'clientkick %(cid)s'}
    _eventMap = {}
    _lineClear = re.compile('^(?:[0-9:.]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<pbid>[0-9A-Z]{32}):\\s*(?P<name>[^:]+):\\s*(?P<num1>[0-9]+):\\s*(?P<num2>[0-9]+):\\s*(?P<ip>[0-9.]+):(?P<port>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<name>.+):\\s+(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<acid>[0-9]+)\\s(?P<cid>[0-9]+)\\s(?P<aweap>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+)\\s(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z_]+):\\s*(?P<data>(?P<acid>[0-9]+)\\s(?P<cid>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z_]+):\\s*(?P<data>(?P<cid>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z_]+):\\s*(?P<data>.*)$', re.IGNORECASE),
     re.compile('^\\[(?P<action>[a-z]+)]\\s(?P<data>.*)$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+)\\s(?P<data>(?P<command>[a-z]+):\\s(?P<origin>.*)\\sto\\s(?P<target>.*):\\s(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+)\\s(?P<data>(?P<command>[a-z]+):\\s(?P<origin>.*)\\sto\\s(?P<target>.*):)$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+)\\s(?P<data>(?P<command>[a-z]+):\\s(?P<text>.*))$', re.IGNORECASE))
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\\s+(?P<qport>[0-9]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _reColor = re.compile('(\\^.)|[\\x00-\\x20]|[\\x7E-\\xff]')
    MOD_UNKNOWN = '0'
    MOD_MACHINEGUN = '1'
    MOD_BROWNING = '2'
    MOD_MG42 = '3'
    MOD_GRENADE = '4'
    MOD_ROCKET = '5'
    MOD_KNIFE = '6'
    MOD_LUGER = '7'
    MOD_COLT = '8'
    MOD_MP40 = '9'
    MOD_THOMPSON = '10'
    MOD_STEN = '11'
    MOD_GARAND = '12'
    MOD_SNOOPERSCOPE = '13'
    MOD_SILENCER = '14'
    MOD_FG42 = '15'
    MOD_FG42SCOPE = '16'
    MOD_PANZERFAUST = '17'
    MOD_GRENADE_LAUNCHER = '18'
    MOD_FLAMETHROWER = '19'
    MOD_GRENADE_PINEAPPLE = '20'
    MOD_CROSS = '21'
    MOD_MAPMORTAR = '22'
    MOD_MAPMORTAR_SPLASH = '23'
    MOD_KICKED = '24'
    MOD_GRABBER = '25'
    MOD_DYNAMITE = '26'
    MOD_AIRSTRIKE = '27'
    MOD_SYRINGE = '28'
    MOD_AMMO = '29'
    MOD_ARTY = '30'
    MOD_WATER = '31'
    MOD_SLIME = '32'
    MOD_LAVA = '33'
    MOD_CRUSH = '34'
    MOD_TELEFRAG = '35'
    MOD_FALLING = '36'
    MOD_SUICIDE = '37'
    MOD_TARGET_LASER = '38'
    MOD_TRIGGER_HURT = '39'
    MOD_EXPLOSIVE = '40'
    MOD_CARBINE = '41'
    MOD_KAR98 = '42'
    MOD_GPG40 = '43'
    MOD_M7 = '44'
    MOD_LANDMINE = '45'
    MOD_SATCHEL = '46'
    MOD_TRIPMINE = '47'
    MOD_SMOKEBOMB = '48'
    MOD_MOBILE_MG42 = '49'
    MOD_SILENCED_COLT = '50'
    MOD_GARAND_SCOPE = '51'
    MOD_CRUSH_CONSTRUCTION = '52'
    MOD_CRUSH_CONSTRUCTIONDEATH = '53'
    MOD_CRUSH_CONSTRUCTIONDEATH_NOATTACKER = '54'
    MOD_K43 = '55'
    MOD_K43_SCOPE = '56'
    MOD_MORTAR = '57'
    MOD_AKIMBO_COLT = '58'
    MOD_AKIMBO_LUGER = '59'
    MOD_AKIMBO_SILENCEDCOLT = '60'
    MOD_AKIMBO_SILENCEDLUGER = '61'
    MOD_SMOKEGRENADE = '62'
    MOD_SWAP_PLACES = '63'
    MOD_SWITCHTEAM = '64'
    Suicides = (
     MOD_WATER,
     MOD_SLIME,
     MOD_LAVA,
     MOD_CRUSH,
     MOD_TELEFRAG,
     MOD_FALLING,
     MOD_SUICIDE,
     MOD_TARGET_LASER,
     MOD_TRIGGER_HURT,
     MOD_LANDMINE,
     MOD_TRIPMINE)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.bot("TIP: Make sure b_privatemessages isn't set to `0` in your game server config file or B3 won't be able to send private messages to players.")
        b_privatemessages = self.getCvar('b_privatemessages').getString()
        if b_privatemessages == '0':
            self.warning('Current b_privatemessages value: %s' % b_privatemessages)
        else:
            self.info('Current b_privatemessages value: %s' % b_privatemessages)
        self.clients.newClient('-1', guid='WORLD', name='World', hide=True, pbid='WORLD')
        mapname = self.getMap()
        if mapname:
            self.game.mapName = mapname
            self.info('map is: %s' % self.game.mapName)
        self.debug('Forcing server cvar g_logsync to %s' % self._logSync)
        self.setCvar('g_logsync', self._logSync)
        self._eventMap['warmup'] = self.getEventID('EVT_GAME_WARMUP')
        self._eventMap['restartgame'] = self.getEventID('EVT_GAME_ROUND_END')

    def getLineParts(self, line):
        """
        Parse a log line returning extracted tokens.
        :param line: The line to be parsed
        """
        m = None
        line = re.sub(self._lineClear, '', line, 1)
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
        data = {}
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
            client = self.clients.getByCID(bclient['cid'])
            if client:
                for k, v in bclient.iteritems():
                    setattr(client, k, v)

            else:
                if 'cl_guid' in bclient:
                    guid = bclient['cl_guid']
                else:
                    guid = 'unknown'
                if 'name' not in bclient:
                    bclient['name'] = self._empty_name_default
                if 'ip' not in bclient and guid == 'unknown':
                    self.debug('Client disconnected: ignoring...')
                    return
                nguid = ''
                if self.IpsOnly:
                    nguid = bclient['ip']
                elif self.IpCombi:
                    i = bclient['ip'].split('.')
                    d = len(i[0]) + len(i[1])
                    nguid = guid[:-d] + i[0] + i[1]
                elif guid == 'unknown':
                    nguid = bclient['ip']
                if nguid != '':
                    guid = nguid
                self.clients.newClient(bclient['cid'], name=bclient['name'], ip=bclient['ip'], state=b3.STATE_ALIVE, guid=guid, data={'guid': guid})
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
                self.debug('No damage type, weapon: %s' % weapon)
                return None
            eventkey = 'EVT_CLIENT_KILL'
            if attacker.cid == victim.cid:
                if weapon == self.MOD_SWITCHTEAM:
                    self.verbose('Team change event caught: exiting')
                    return None
                eventkey = 'EVT_CLIENT_SUICIDE'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team:
                eventkey = 'EVT_CLIENT_KILL_TEAM'
            if not hasattr(victim, 'hitloc'):
                victim.hitloc = 'body'
            victim.state = b3.STATE_DEAD
            return self.getEvent(eventkey, (100, weapon, victim.hitloc, damagetype), attacker, victim)

    def OnClientbegin(self, action, data, match=None):
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

        self.verbose('...self.console.game.gameType: %s' % self.game.gameType)
        self.game.startRound()
        self.debug('Synchronizing client info')
        self.clients.sync()
        return self.getEvent('EVT_GAME_ROUND_START', self.game)

    def OnQmm(self, action, data, match=None):
        return

    def OnEtpro(self, action, data, match=None):
        try:
            command = match.group('command')
        except:
            self.debug('Etpro info line: %s' % match.group('data'))
            return

        if command == 'privmsg':
            try:
                text = match.group('text')
            except:
                self.verbose('No message entered in privmsg!')
                return

            self.OnPrivMsg(match.group('origin'), match.group('target'), text)
        elif command == 'event':
            self.verbose('event: %s' % match.group('text'))
        else:
            self.verbose('%s: %s' % (command, match.group('text')))
        return

    def OnPrivMsg(self, origin, target, text):
        client = self.clients.getByExactName(origin)
        tclient = self.clients.getClientLikeName(target)
        if not client:
            return
        else:
            if not tclient:
                client.message("Please be more specific providing the target, can't find it with given input!")
                return
            if text and ord(text[:1]) == 21:
                text = text[1:]
            self.verbose('text: %s, client: %s - %s, tclient: %s - %s' % (text, client.name, client.id, tclient.name, tclient.id))
            self.queueEvent(self.getEvent('EVT_CLIENT_PRIVATE_SAY', text, client, tclient))
            return

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
        Translate the gametype to a readable format (also for teamkill plugin!)
        """
        gametype = str(gametype_int)
        if gametype_int == '0':
            gametype = 'sp'
        elif gametype_int == '1':
            gametype = 'cp'
        elif gametype_int == '2':
            gametype = 'smo'
        elif gametype_int == '3':
            gametype = 'sw'
        elif gametype_int == '4':
            gametype = 'ca'
        elif gametype_int == '5':
            gametype = 'lms'
        return gametype

    def message(self, client, text):
        """
        Send a private message to a client.
        :param client: The client to who send the message.
        :param text: The message to be sent.
        """
        if client is None:
            self.say(text)
            return
        else:
            lines = []
            message = prefixText([self.msgPrefix, self.pmPrefix], text)
            message = message.strip()
            for line in self.getWrap(message):
                lines.append(self.getCommand('message', name=client.name, message=line))

            self.writelines(lines)
            return

    def sayDead(self, text):
        """
        Send a private message to all the dead clients.
        :param text: The message to be sent.
        """
        lines = []
        message = prefixText([self.msgPrefix, self.deadPrefix], text)
        message = message.strip()
        wrapped = self.getWrap(message)
        for client in self.clients.getClientsByState(b3.STATE_DEAD):
            if client.cid:
                for line in wrapped:
                    lines.append(self.getCommand('message', name=client.name, message=line))

        self.writelines(lines)

    def getMaps(self):
        return [
         'Command not supported!']

    def getNextMap(self):
        return 'Command not supported!'

    def sync(self):
        """
        For all connected players returned by self.get_player_list(), get the matching Client
        object from self.clients (with self.clients.get_by_cid(cid) or similar methods) and
        look for inconsistencies. If required call the client.disconnect() method to remove
        a client from self.clients.
        """
        plist = self.getPlayerList()
        mlist = {}
        for cid, c in plist.iteritems():
            client = self.clients.getByCID(cid)
            if client:
                if client.guid and 'guid' in c:
                    if client.guid == c['guid']:
                        self.debug('in-sync %s == %s (cid: %s - slotid: %s)', client.guid, c['guid'], client.cid, c['cid'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s (disconnecting %s from slot %s)', client.guid, c['guid'], client.name, client.cid)
                        client.disconnect()
                elif client.ip and 'ip' in c:
                    if client.ip == c['ip']:
                        self.debug('in-sync %s == %s (cid: %s == slotid: %s)', client.ip, c['ip'], client.cid, c['cid'])
                        mlist[str(cid)] = client
                    else:
                        self.debug('no-sync %s <> %s (disconnecting %s from slot %s)', client.ip, c['ip'], client.name, client.cid)
                        client.disconnect()
                else:
                    self.debug('no-sync: no guid or ip found')

        return mlist
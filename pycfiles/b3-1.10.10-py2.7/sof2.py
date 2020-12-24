# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\sof2.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'xlr8or, ~cGs*Pr3z, ~cGs*AQUARIUS'
__version__ = '1.6'
import b3, b3.events, b3.parsers.punkbuster, re, string
from b3.parsers.q3a.abstractParser import AbstractParser
from b3.functions import prefixText

class Sof2Parser(AbstractParser):
    gameName = 'sof2'
    privateMsg = False
    PunkBuster = None
    IpsOnly = False
    IpCombi = False
    _clientConnectID = None
    _clientConnectGuid = None
    _clientConnectIp = None
    _logSync = 0
    _empty_name_default = 'EmptyNameDefault'
    _line_length = 65
    _line_color_prefix = ''
    _commands = {'ban': 'addip %(cid)s', 
       'kick': 'clientkick %(cid)s', 
       'message': 'say %(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'tempban': 'clientkick %(cid)s'}
    _eventMap = {}
    _lineClear = re.compile('^(?:[0-9:]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<acid>[0-9]+)\\s(?P<cid>[0-9]+)\\s(?P<aweap>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[\\w]+):\\s(?P<data>(?P<acid>[\\d]+)\\s(?P<cid>[\\d]+)\\s(?P<hitloc>[-\\d]+)\\s(?P<damage>[\\d]+)\\s(?P<aweap>[\\d]+):\\s+(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>say):\\s*(?P<data>(?P<name>[^:]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s(?P<data>(?P<cid>[0-9]+)\\s-\\s(?P<ip>[0-9.]+):(?P<port>[-0-9]+)\\s\\[(?P<cl_guid>[0-9A-Z]{32})\\])$', re.IGNORECASE),
     re.compile('^(?P<action>ClientConnect):\\s*(?P<data>(?P<bcid>[0-9]+)\\s-\\s\\s\\[\\])$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>.*)$', re.IGNORECASE))
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\\s+(?P<qport>[0-9]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _reColor = re.compile('(\\^.)|[\\x00-\\x20]|[\\x7E-\\xff]')
    MOD_UNKNOWN = '0'
    MOD_KNIFE = '1'
    MOD_M1911A1_PISTOL = '2'
    MOD_USSOCOM_PISTOL = '3'
    MOD_SILVER_TALON = '4'
    MOD_M590_SHOTGUN = '5'
    MOD_MICRO_UZI_SUBMACHINEGUN = '6'
    MOD_M3A1_SUBMACHINEGUN = '7'
    MOD_MP5 = '8'
    MOD_USAS_12_SHOTGUN = '9'
    MOD_M4_ASSAULT_RIFLE = '10'
    MOD_AK74_ASSAULT_RIFLE = '11'
    MOD_SIG551 = '12'
    MOD_MSG90A1_SNIPER_RIFLE = '13'
    MOD_M60_MACHINEGUN = '14'
    MOD_MM1_GRENADE_LAUNCHER = '15'
    MOD_RPG7_LAUNCHER = '16'
    MOD_M84_GRENADE = '17'
    MOD_SMOHG92_GRENADE = '18'
    MOD_ANM14_GRENADE = '19'
    MOD_M15_GRENADE = '20'
    MOD_WATER = '21'
    MOD_CRUSH = '22'
    MOD_TELEFRAG = '23'
    MOD_FALLING = '24'
    MOD_SUICIDE = '25'
    MOD_TEAMCHANGE = '26'
    MOD_TARGET_LASER = '27'
    MOD_TRIGGER_HURT = '28'
    MOD_TRIGGER_HURT_NOSUICIDE = '29'
    MOD_ADMIN_STRIKE = '30'
    MOD_ADMIN_SLAP = '31'
    MOD_ADMIN_FRY = '32'
    MOD_ADMIN_EXPLODE = '33'
    MOD_ADMIN_TELEFRAG = '34'
    MOD_KNIFE_ALT = '35'
    MOD_M1911A1_PISTOL_ALT = '36'
    MOD_USSOCOM_PISTOL_ALT = '37'
    MOD_SILVER_TALON_ALT = '38'
    MOD_M590_SHOTGUN_ALT = '39'
    MOD_M4_ASSAULT_RIFLE_ALT = '40'
    MOD_AK74_ASSAULT_RIFLE_ALT = '41'
    MOD_M84_GRENADE_ALT = '42'
    MOD_SMOHG92_GRENADE_ALT = '43'
    MOD_ANM14_GRENADE_ALT = '44'
    MOD_M15_GRENADE_ALT = '45'

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.clients.newClient('-1', guid='WORLD', name='World', hide=True, pbid='WORLD')
        if self.privateMsg:
            self.warning('SoF2 will need a mod to enable private messaging!')
        self._eventMap['warmup'] = self.getEventID('EVT_GAME_WARMUP')
        self._eventMap['shutdowngame'] = self.getEventID('EVT_GAME_ROUND_END')
        if not self.config.has_option('server', 'punkbuster') or self.config.getboolean('server', 'punkbuster'):
            self.PunkBuster = b3.parsers.punkbuster.PunkBuster(self)
        self.debug('Forcing server cvar g_logsync to %s' % self._logSync)
        self.setCvar('g_logsync', self._logSync)
        mapname = self.getMap()
        if mapname:
            self.game.mapName = mapname
            self.info('map is: %s' % self.game.mapName)
        plist = self.getPlayerList()
        for cid, c in plist.iteritems():
            userinfostring = self.queryClientUserInfoByName(cid, c['name'])
            if userinfostring:
                self.OnClientuserinfo(None, userinfostring)

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
        self.verbose('Client connected - cid: %s, guid: %s, ip: %s' % (self._clientConnectID,
         self._clientConnectGuid,
         self._clientConnectIp))
        return

    def OnClientuserinfo(self, action, data, match=None):
        bot = False
        bclient = self.parseUserInfo(data)
        if 'name' in bclient:
            bclient['name'] = bclient['name'].replace(' ', '')
        if 'ip' in bclient:
            if bclient['ip'] == 'bot':
                self.bot('Bot connected!')
                bclient['ip'] = '0.0.0.0'
                bclient['cl_guid'] = 'BOT' + str(bclient['cid'])
                bot = True
            else:
                ip_port_data = string.split(bclient['ip'], ':', 1)
                bclient['ip'] = ip_port_data[0]
                if len(ip_port_data) > 1:
                    bclient['port'] = ip_port_data[1]
        if 'team' in bclient:
            bclient['team'] = self.getTeam(bclient['team'])
        if 'cl_guid' in bclient and 'pbid' not in bclient and self.PunkBuster:
            bclient['pbid'] = bclient['cl_guid']
        self.verbose('Parsed user info: %s' % bclient)
        if bclient:
            client = self.clients.getByCID(bclient['cid'])
            if client:
                for k, v in bclient.iteritems():
                    setattr(client, k, v)

            else:
                if self.PunkBuster:
                    guid = None
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
                self.clients.newClient(bclient['cid'], name=bclient['name'], ip=bclient['ip'], state=b3.STATE_ALIVE, guid=guid, bot=bot, data={'guid': guid})
        return

    def OnClientuserinfochanged(self, action, data, match=None):
        client_id = None
        client = None
        if self._clientConnectID is not None:
            client_id = self._clientConnectID
        self._clientConnectID = None
        bclient = self.parseUserInfo(data)
        self.verbose('Parsed user info: %s' % bclient)
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
                client = self.clients.newClient(bclient['cid'], name=bclient['name'], ip=bclient['ip'], state=b3.STATE_ALIVE, guid=bclient['cl_guid'], data={'guid': bclient['cl_guid']})
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

        self.verbose('Current gametype: %s' % self.game.gameType)
        self.game.startRound()
        return self.getEvent('EVT_GAME_ROUND_START', self.game)

    def OnSay(self, action, data, match=None):
        msg = string.split(data, ': ', 1)
        if not len(msg) == 2:
            return
        else:
            client = self.clients.getByExactName(msg[0])
            if client:
                self.verbose('OnSay: client found: %s' % client.name)
                return self.getEvent('EVT_CLIENT_SAY', msg[1], client)
            self.verbose('OnSay: no client found!')
            return
            return

    def OnSayteam(self, action, data, match=None):
        msg = string.split(data, ': ', 1)
        if not len(msg) == 2:
            return
        else:
            client = self.clients.getByExactName(msg[0])
            if client:
                self.verbose('OnSayTeam: client found: %s' % client.name)
                return self.getEvent('EVT_CLIENT_TEAM_SAY', msg[1], client, client.team)
            self.verbose('OnSayTeam: no client found!')
            return
            return

    def OnHit(self, action, data, match=None):
        victim = self.clients.getByCID(match.group('cid'))
        if not victim:
            self.debug('No victim')
            return None
        else:
            attacker = self.clients.getByCID(match.group('acid'))
            if not attacker:
                self.debug('No attacker')
                return None
            eventkey = 'EVT_CLIENT_DAMAGE'
            if attacker.cid == victim.cid:
                eventkey = 'EVT_CLIENT_DAMAGE_SELF'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team:
                eventkey = 'EVT_CLIENT_DAMAGE_TEAM'
            victim.hitloc = match.group('hitloc')
            return self.getEvent(eventkey, (match.group('damage'), match.group('aweap'), victim.hitloc), attacker, victim)

    def OnKill(self, action, data, match=None):
        """
        0:      MOD_UNKNOWN, UNKNOWN
        1:      MOD_KNIFE, Killed by KNIFE
        2:      MOD_M1911A1_PISTOL, Killed by M1911A1_PISTOL
        3:      MOD_USSOCOM_PISTOL, Killed by USSOCOM_PISTOL
        4:      MOD_SILVER_TALON, Killed by SILVER_TALON
        5:      MOD_M590_SHOTGUN, Killed by M590_SHOTGUN
        6:      MOD_MICRO_UZI_SUBMACHINEGUN, Killed by MICRO_UZI_SUBMACHINEGUN
        7:      MOD_M3A1_SUBMACHINEGUN, Killed by M3A1_SUBMACHINEGUN
        8:      MOD_MP5, Killed by MP5
        9:      MOD_USAS_12_SHOTGUN, Killed by USAS_12_SHOTGUN
        10:     MOD_M4_ASSAULT_RIFLE, Killed by M4_ASSAULT_RIFLE
        11:     MOD_AK74_ASSAULT_RIFLE, Killed by AK74_ASSAULT_RIFLE
        12:     MOD_SIG551, Killed by SIG551
        13:     MOD_MSG90A1_SNIPER_RIFLE, Killed by MSG90A1_SNIPER_RIFLE
        14:     MOD_M60_MACHINEGUN, Killed by M60_MACHINEGUN
        15:     MOD_MM1_GRENADE_LAUNCHER, Killed by MM1_GRENADE_LAUNCHER
        16:     MOD_RPG7_LAUNCHER, Killed by RPG7_LAUNCHER
        17:     MOD_M84_GRENADE, Killed by M84_GRENADE
        18:     MOD_SMOHG92_GRENADE, Killed by SMOHG92_GRENADE
        19:     MOD_ANM14_GRENADE, Killed by ANM14_GRENADE
        20:     MOD_M15_GRENADE, Killed by M15_GRENADE
        21:     MOD_WATER, Killed by WATER
        22:     MOD_CRUSH, Killed by Mover
        23:     MOD_TELEFRAG, Killed by TELEFRAG
        24:     MOD_FALLING, Killed by FALLING
        25:     MOD_SUICIDE, Killed by SUICIDE
        26:     MOD_TEAMCHANGE, Killed by TEAMCHANGE
        27:     MOD_TARGET_LASER, Killed by TARGET_LASER
        28:     MOD_TRIGGER_HURT, Killed by TRIGGER_HURT
        29:     MOD_TRIGGER_HURT_NOSUICIDE, Killed by TRIGGER_HURT_NOSUICIDE
        30:     MOD_ADMIN_STRIKE, Killed by ADMIN_STRIKE
        31:     MOD_ADMIN_SLAP, Killed by ADMIN_SLAP
        32:     MOD_ADMIN_FRY, Killed by ADMIN_FRY
        33:     MOD_ADMIN_EXPLODE, Killed by ADMIN_EXPLODE
        34:     MOD_ADMIN_TELEFRAG, Killed by ADMIN_TELEFRAG
        35:     MOD_KNIFE_ALT, Killed by KNIFE_ALT
        36:     MOD_M1911A1_PISTOL_ALT, Killed by M1911A1_PISTOL_ALT
        37:     MOD_USSOCOM_PISTOL_ALT, Killed by USSOCOM_PISTOL_ALT
        38:     MOD_SILVER_TALON_ALT, Killed by SILVER_TALON_ALT
        39:     MOD_M590_SHOTGUN_ALT, Killed by M590_SHOTGUN_ALT
        40:     MOD_M4_ASSAULT_RIFLE_ALT, Killed by M4_ASSAULT_RIFLE_ALT
        41:     MOD_AK74_ASSAULT_RIFLE, Killed by AK74_ASSAULT_RIFLE
        42:     MOD_M84_GRENADE_ALT, Killed by M84_GRENADE_ALT
        43:     MOD_SMOHG92_GRENADE_ALT, Killed by SMOHG92_GRENADE_ALT
        44:     MOD_ANM14_GRENADE_ALT, Killed by ANM14_GRENADE_ALT
        45:     MOD_M15_GRENADE_ALT, Killed by M15_GRENADE_ALT
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
            if match.group('aweap') in (
             self.MOD_MM1_GRENADE_LAUNCHER, self.MOD_RPG7_LAUNCHER, self.MOD_M84_GRENADE, self.MOD_SMOHG92_GRENADE,
             self.MOD_ANM14_GRENADE, self.MOD_M15_GRENADE, self.MOD_WATER, self.MOD_FALLING, self.MOD_SUICIDE,
             self.MOD_TRIGGER_HURT, self.MOD_M4_ASSAULT_RIFLE_ALT, self.MOD_M84_GRENADE_ALT,
             self.MOD_SMOHG92_GRENADE_ALT, self.MOD_ANM14_GRENADE_ALT, self.MOD_M15_GRENADE_ALT):
                self.debug('OnKill: mm1_grenade_launcher/rpg7_launcher/m84_grenade/smohg92_grenade/anm14/m15_grenade/water/suicide/trigger_hurt/m4_assault_rifle_alt/m84_grenade_alt/smohg92_grenade_alt/anm14_alt/m15_grenade_alt should be suicides')
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
                if weapon == self.MOD_TEAMCHANGE:
                    self.verbose('team change event caught: exiting...')
                    return None
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

    def getNextMap(self):
        pass

    def message(self, client, text):
        """
        Need to override message format.
        Game does not support PM's
        """
        lines = []
        message = prefixText([self.msgPrefix, '^7[^3%s^7]:' % client.name], text)
        message = message.strip()
        for line in self.getWrap(message):
            lines.append(self.getCommand('message', message=line))

        self.writelines(lines)

    def defineGameType(self, gametype_int):
        """
        Translate the gametype to a readable format.
        """
        gametype = str(gametype_int)
        if gametype_int == '0':
            gametype = 'ass'
        elif gametype_int == '1':
            gametype = 'cnh'
        elif gametype_int == '2':
            gametype = 'ctb'
        elif gametype_int == '3':
            gametype = 'cctf'
        elif gametype_int == '4':
            gametype = 'ctf'
        elif gametype_int == '5':
            gametype = 'dem'
        elif gametype_int == '6':
            gametype = 'dm'
        elif gametype_int == '7':
            gametype = 'dom'
        elif gametype_int == '8':
            gametype = 'elim'
        elif gametype_int == '9':
            gametype = 'gold'
        elif gametype_int == '10':
            gametype = 'inf'
        elif gametype_int == '11':
            gametype = 'knockback'
        elif gametype_int == '12':
            gametype = 'lms'
        elif gametype_int == '13':
            gametype = 'rctf'
        elif gametype_int == '14':
            gametype = 'stq'
        elif gametype_int == '15':
            gametype = 'tctb'
        elif gametype_int == '16':
            gametype = 'tdm'
        elif gametype_int == '17':
            gametype = 'tstq'
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
                self.queueEvent(self.getEvent('EVT_CLIENT_JOIN', client=client))

        return

    def queryClientUserInfoByName(self, cid, name):
        r"""
        ]\dumpuser xlr8or
        Player xlr8or is not on the server

        ]\dumpuser xlr8or
        userinfo
        --------
        ip                  145.99.135.000:-12892
        cl_guid             XXXXD914662572D3649B94B1EA5F921
        cl_punkbuster       0
        details             5
        name                xlr8or
        rate                9000
        snaps               20
        identity            NPC_Sam/sam_gladstone
        cl_anonymous        0
        cg_predictItems     1
        cg_antiLag          1
        cg_autoReload       1
        cg_smoothClients    0
        team_identity       shopguard1
        outfitting          GACAA
        """
        data = self.write('dumpuser %s' % name)
        if not data:
            return None
        else:
            if data.split('\n')[0] != 'userinfo':
                self.debug('Dumpuser %s returned : %s' % (name, data))
                self.debug('Client probably disconnected but its character is still hanging in game...')
                return None
            datatransformed = '%s ' % cid
            for line in data.split('\n'):
                if line.strip() == 'userinfo' or line.strip() == '--------':
                    continue
                var = line[:20].strip()
                val = line[20:].strip()
                datatransformed += '\\%s\\%s' % (var, val)

            return datatransformed

    def getByNameOrJoinPlayer(self, name):
        client = self.clients.getByExactName(name)
        if client:
            return client
        else:
            userinfostring = self.queryClientUserInfoByName('-1', name)
            if userinfostring:
                self.OnClientuserinfo(None, userinfostring)
            return self.clients.getByExactName(name)
            return
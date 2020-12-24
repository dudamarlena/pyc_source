# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\q3a\abstractParser.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'ThorN, xlr8or'
__version__ = '1.8.1'
import re, string, time, new, b3, b3.events, b3.clients, b3.functions, b3.parser, b3.cvar
from b3.parsers.q3a import rcon
from b3.parsers.punkbuster import PunkBuster
from b3.functions import prefixText

class AbstractParser(b3.parser.Parser):
    """
    An abstract base class to help with developing q3a parsers.
    """
    gameName = None
    privateMsg = True
    rconTest = True
    OutputClass = rcon.Rcon
    PunkBuster = None
    _clientConnectID = None
    _logSync = 2
    _commands = {'ban': 'banid %(cid)s %(reason)s', 
       'kick': 'clientkick %(cid)s %(reason)s', 
       'kickbyfullname': 'kick %(name)s', 
       'message': 'tell %(cid)s %(message)s', 
       'moveToTeam': 'forceteam %(cid)s %(team)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'tempban': 'clientkick %(cid)s %(reason)s'}
    _eventMap = {}
    _lineTime = re.compile('^(?P<minutes>[0-9]+):(?P<seconds>[0-9]+).*')
    _lineClear = re.compile('^(?:[0-9:]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<pbid>[0-9A-Z]{32}):\\s*(?P<name>[^:]+):\\s*(?P<num1>[0-9]+):\\s*(?P<num2>[0-9]+):\\s*(?P<ip>[0-9.]+):(?P<port>[0-9]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<name>.+):\\s+(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+)\\s(?P<acid>[0-9]+)\\s(?P<aweap>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+):\\s*(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>(?P<cid>[0-9]+)\\s(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+):\\s*(?P<data>.*)$', re.IGNORECASE))
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<guid>[0-9a-zA-Z]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\\s+(?P<qport>[0-9]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _regPlayerShort = re.compile('\\s+(?P<slot>[0-9]+)\\s+(?P<score>[0-9]+)\\s+(?P<ping>[0-9]+)\\s+(?P<name>.*)\\^7\\s+', re.IGNORECASE)
    _reColor = re.compile('(\\^[0-9a-z])|[\\x80-\\xff]')
    _reCvarName = re.compile('^[a-z0-9_.]+$', re.IGNORECASE)
    _reCvar = (
     re.compile('^"(?P<cvar>[a-z0-9_.]+)"\\s+is:\\s*"(?P<value>.*?)(\\^7)?"\\s+default:\\s*"(?P<default>.*?)(\\^7)?"$', re.IGNORECASE | re.MULTILINE),
     re.compile('^"(?P<cvar>[a-z0-9_.]+)"\\s+is:\\s*"(?P<default>(?P<value>.*?))(\\^7)?",\\s+the\\sdefault$', re.IGNORECASE | re.MULTILINE),
     re.compile('^"(?P<cvar>[a-z0-9_.]+)"\\s+is:\\s*"(?P<value>.*?)(\\^7)?"$', re.IGNORECASE | re.MULTILINE))
    _reMapNameFromStatus = re.compile('^map:\\s+(?P<map>.+)$', re.IGNORECASE)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        if not self.config.has_option('server', 'game_log'):
            self.critical("Your main config file is missing the 'game_log' setting in section 'server'")
            raise SystemExit(220)
        self.clients.newClient('1022', guid='WORLD', name='World', hide=True, pbid='WORLD')
        if self.config.has_option('server', 'punkbuster') and self.config.getboolean('server', 'punkbuster'):
            self.PunkBuster = PunkBuster(self)
        self._eventMap['warmup'] = self.getEventID('EVT_GAME_WARMUP')
        self._eventMap['shutdowngame'] = self.getEventID('EVT_GAME_ROUND_END')
        self.debug('Forcing server cvar g_logsync to %s' % self._logSync)
        self.setCvar('g_logsync', self._logSync)

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
                self.verbose('Line did not match format: %s' % line)
            return

    def parseLine(self, line):
        """
        Parse a log line creating necessary events.
        :param line: The log line to be parsed
        """
        m = self.getLineParts(line)
        if not m:
            return False
        match, action, data, client, target = m
        func = 'On%s' % string.capwords(action).replace(' ', '')
        if hasattr(self, func):
            func = getattr(self, func)
            event = func(action, data, match)
            if event:
                self.queueEvent(event)
        elif action in self._eventMap:
            self.queueEvent(self.getEvent(self._eventMap[action], data=data, client=client, target=target))
        else:
            data = str(action) + ': ' + str(data)
            self.queueEvent(self.getEvent('EVT_UNKNOWN', data=data, client=client, target=target))

    def parseUserInfo(self, info):
        """
        Parse an infostring.
        :param info: The infostring to be parsed.
        """
        cid, info = string.split(info, ' ', 1)
        if info[:1] != '\\':
            info = '\\' + info
        options = re.findall('\\\\([^\\\\]+)\\\\([^\\\\]+)', info)
        data = {}
        for o in options:
            data[o[0]] = o[1]

        if 'n' in data:
            data['name'] = data['n']
        t = None
        if 'team' in data:
            t = data['team']
        elif 't' in data:
            t = data['t']
        data['team'] = self.getTeam(t)
        if 'cl_guid' in data and 'pbid' not in data:
            data['pbid'] = data['cl_guid']
        return data

    def OnSay(self, action, data, match=None):
        msg = string.split(data, ': ', 1)
        if not len(msg) == 2:
            return None
        else:
            client = self.clients.getByExactName(msg[0])
            return self.getEvent('EVT_CLIENT_SAY', msg[1], client)

    def OnShutdowngame(self, action, data, match=None):
        return self.getEvent('EVT_GAME_ROUND_END', data)

    def OnClientdisconnect(self, action, data, match=None):
        client = self.getClient(match)
        if client:
            client.disconnect()
        return

    def OnSayteam(self, action, data, match=None):
        msg = string.split(data, ': ', 1)
        if not len(msg) == 2:
            return
        else:
            client = self.clients.getByName(msg[0])
            if client:
                return self.getEvent('EVT_CLIENT_TEAM_SAY', msg[1], client, client.team)
            return

    def OnExit(self, action, data, match=None):
        self.game.mapEnd()
        return self.getEvent('EVT_GAME_EXIT', None)

    def OnItem(self, action, data, match=None):
        client = self.getClient(match)
        if client:
            return self.getEvent('EVT_CLIENT_ITEM_PICKUP', match.group('text'), client)
        else:
            return

    def OnClientbegin(self, action, data, match=None):
        self._clientConnectID = data
        return

    def OnClientconnect(self, action, data, match=None):
        self._clientConnectID = data
        return

    def OnClientuserinfo(self, action, data, match=None):
        bclient = self.parseUserInfo(data)
        self.verbose('Parsed user info: %s' % bclient)
        if bclient:
            client = self.clients.getByCID(bclient['cid'])
            if client:
                for k, v in bclient.iteritems():
                    setattr(client, k, v)

            else:
                self.clients.newClient(bclient['cid'], **bclient)
        return

    def OnClientuserinfochanged(self, action, data, match=None):
        return self.OnClientuserinfo(action, data, match)

    def OnUserinfo(self, action, data, match=None):
        _id = self._clientConnectID
        self._clientConnectID = None
        if not _id:
            self.error('OnUserinfo called without a ClientConnect ID')
            return
        else:
            return self.OnClientuserinfo(action, '%s %s' % (_id, data), match)

    def OnKill(self, action, data, match=None):
        attacker = self.getClient(attacker=match)
        if not attacker:
            self.bot('No attacker')
            return
        else:
            victim = self.getClient(victim=match)
            if not victim:
                self.bot('No victim')
                return
            return self.getEvent('EVT_CLIENT_KILL', (100, match.group('aweap'), None), attacker, victim)

    def OnInitgame(self, action, data, match=None):
        options = re.findall('\\\\([^\\\\]+)\\\\([^\\\\]+)', data)
        for o in options:
            if o[0] == 'mapname':
                self.game.mapName = o[1]
            elif o[0] == 'g_gametype':
                self.game.gameType = o[1]
            elif o[0] == 'fs_game':
                self.game.modName = o[1]
            else:
                setattr(self.game, o[0], o[1])

        self.game.startRound()
        return self.getEvent('EVT_GAME_ROUND_START', self.game)

    def getClient(self, match=None, attacker=None, victim=None):
        """
        Get a client object using the best availible data.
        :param match: The match group extracted from the log line parsing
        :param attacker: The attacker group extracted from the log line parsing
        :param victim: The victim group extracted from the log line parsing
        """
        if attacker:
            return self.clients.getByCID(attacker.group('acid'))
        if victim:
            return self.clients.getByCID(victim.group('cid'))
        if match:
            return self.clients.getByCID(match.group('cid'))

    def getTeam(self, team):
        """
        Return a B3 team given the team value.
        :param team: The team value
        """
        team = str(team).lower()
        if team == 'free' or team == '0':
            return b3.TEAM_FREE
        if team == 'red' or team == '1':
            return b3.TEAM_RED
        if team == 'blue' or team == '2':
            return b3.TEAM_BLUE
        if team == 'spectator' or team == '3':
            return b3.TEAM_SPEC
        return b3.TEAM_UNKNOWN

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
            if client.cid is None:
                return
            lines = []
            message = prefixText([self.msgPrefix, self.pmPrefix], text)
            message = message.strip()
            for line in self.getWrap(message):
                lines.append(self.getCommand('message', cid=client.cid, message=line))

            self.writelines(lines)
            return

    def say(self, text):
        """
        Broadcast a message to all players.
        :param text: The message to be broadcasted
        """
        lines = []
        message = prefixText([self.msgPrefix], text)
        message = message.strip()
        for line in self.getWrap(message):
            lines.append(self.getCommand('say', message=line))

        self.writelines(lines)

    def saybig(self, text):
        """
        Broadcast a message to all players in a way that will catch their attention.
        :param text: The message to be broadcasted
        """
        for c in range(1, 6):
            self.say('^%i%s' % (c, text))

    def smartSay(self, client, text):
        """
        Send a message to the game chat area with visibility regulated by the client dead state.
        :param client: The client whose state will regulate the message visibility.
        :param text: The message to be sent.
        """
        if client and (client.state == b3.STATE_DEAD or client.team == b3.TEAM_SPEC):
            self.verbose('Say dead state: %s, team %s', client.state, client.team)
            self.sayDead(text)
        else:
            self.verbose('Say all')
            self.say(text)

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
                    lines.append(self.getCommand('message', cid=client.cid, message=line))

        self.writelines(lines)

    def kick(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Kick a given client.
        :param client: The client to kick
        :param reason: The reason for this kick
        :param admin: The admin who performed the kick
        :param silent: Whether or not to announce this kick
        """
        if isinstance(client, basestring) and re.match('^[0-9]+$', client):
            self.write(self.getCommand('kick', cid=client, reason=reason))
            return
        if self.PunkBuster:
            self.PunkBuster.kick(client, 0.5, reason)
        else:
            self.write(self.getCommand('kick', cid=client.cid, reason=reason))
        if admin:
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
            fullreason = self.getMessage('kicked_by', variables)
        else:
            variables = self.getMessageVariables(client=client, reason=reason)
            fullreason = self.getMessage('kicked', variables)
        if not silent and fullreason != '':
            self.say(fullreason)
        self.queueEvent(self.getEvent('EVT_CLIENT_KICK', {'reason': reason, 'admin': admin}, client))
        client.disconnect()

    def kickbyfullname(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Kick the client matching the given name.
        We get here if a name was given, and the name was not found as
        a client: this will allow the kicking of non autenticated players
        :param client: The client name
        :param reason: The reason for this kick
        :param admin: The admin who performed the kick
        :param silent: Whether or not to announce this kick
        """
        if 'kickbyfullname' in self._commands.keys():
            self.debug('Trying kick by full name: %s for %s' % (client, reason))
            result = self.write(self.getCommand('kickbyfullname', name=client))
            if result.endswith('is not on the server\n'):
                admin.message('^7You need to use the full exact name to kick this player')
            elif result.endswith('was kicked.\n'):
                admin.message('^7Player kicked using full exact name')

    def ban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Ban a given client.
        :param client: The client to ban
        :param reason: The reason for this ban
        :param admin: The admin who performed the ban
        :param silent: Whether or not to announce this ban
        """
        if isinstance(client, b3.clients.Client) and not client.guid:
            return self.kick(client, reason, admin, silent)
        if isinstance(client, str) and re.match('^[0-9]+$', client):
            self.write(self.getCommand('ban', cid=client, reason=reason))
            return
        if not client.id:
            self.error('Q3AParser.ban(): no client id, database must be down, doing tempban')
            return self.tempban(client, reason, 1440, admin, silent)
        if self.PunkBuster:
            self.PunkBuster.ban(client, reason)
        else:
            self.write(self.getCommand('ban', cid=client.cid, reason=reason))
        if admin:
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
            fullreason = self.getMessage('banned_by', variables)
        else:
            variables = self.getMessageVariables(client=client, reason=reason)
            fullreason = self.getMessage('banned', variables)
        if not silent and fullreason != '':
            self.say(fullreason)
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN', {'reason': reason, 'admin': admin}, client))
        client.disconnect()

    def unban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Unban a client.
        :param client: The client to unban
        :param reason: The reason for the unban
        :param admin: The admin who unbanned this client
        :param silent: Whether or not to announce this unban
        """
        if self.PunkBuster:
            if client.pbid:
                result = self.PunkBuster.unBanGUID(client)
                if result:
                    admin.message('^3Unbanned^7: %s^7: %s' % (client.exactName, result))
                if admin:
                    variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
                    fullreason = self.getMessage('unbanned_by', variables)
                else:
                    variables = self.getMessageVariables(client=client, reason=reason)
                    fullreason = self.getMessage('unbanned', variables)
                if not silent and fullreason != '':
                    self.say(fullreason)
            elif admin:
                admin.message('%s^7 unbanned but has no punkbuster id' % client.exactName)
        elif admin:
            admin.message("^3Unbanned^7: %s^7. You may need to manually remove the user from the game's ban file." % client.exactName)

    def tempban(self, client, reason='', duration=2, admin=None, silent=False, *kwargs):
        """
        Tempban a client.
        :param client: The client to tempban
        :param reason: The reason for this tempban
        :param duration: The duration of the tempban
        :param admin: The admin who performed the tempban
        :param silent: Whether or not to announce this tempban
        """
        duration = b3.functions.time2minutes(duration)
        if isinstance(client, b3.clients.Client) and not client.guid:
            return self.kick(client, reason, admin, silent)
        if isinstance(client, str) and re.match('^[0-9]+$', client):
            self.write(self.getCommand('tempban', cid=client, reason=reason))
            return
        if admin:
            banduration = b3.functions.minutesStr(duration)
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin, banduration=banduration)
            fullreason = self.getMessage('temp_banned_by', variables)
        else:
            banduration = b3.functions.minutesStr(duration)
            variables = self.getMessageVariables(client=client, reason=reason, banduration=banduration)
            fullreason = self.getMessage('temp_banned', variables)
        if self.PunkBuster:
            if duration > 1440:
                duration = 1440
            self.PunkBuster.kick(client, duration, reason)
        else:
            self.write(self.getCommand('tempban', cid=client.cid, reason=reason))
        if not silent and fullreason != '':
            self.say(fullreason)
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN_TEMP', {'reason': reason, 'duration': duration, 
           'admin': admin}, client))
        client.disconnect()

    def rotateMap(self):
        """
        Load the next map/level.
        """
        self.say('^7Changing map to next map')
        time.sleep(1)
        self.write('map_rotate 0')

    def changeMap(self, mapname):
        """
        Load a given map/level.
        """
        self.say('^7Changing map to %s' % mapname)
        time.sleep(1)
        self.write('map %s' % mapname)

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
            m = re.match(self._regPlayerShort, line)
            if not m:
                m = re.match(self._regPlayer, line.strip())
            if m:
                players[str(m.group('slot'))] = int(m.group('ping'))

        return players

    def getPlayerScores(self):
        """
        Returns a dict having players' id for keys and players' scores for values.
        """
        data = self.write('status')
        if not data:
            return {}
        players = {}
        for line in data.split('\n'):
            m = re.match(self._regPlayerShort, line)
            if not m:
                m = re.match(self._regPlayer, line.strip())
            if m:
                players[str(m.group('slot'))] = int(m.group('score'))

        return players

    def getPlayerList(self, maxRetries=None):
        """
        Query the game server for connected players.
        Return a dict having players' id for keys and players' data as another dict for values.
        """
        if self.PunkBuster:
            return self.PunkBuster.getPlayerList()
        else:
            data = self.write('status', maxRetries=maxRetries)
            if not data:
                return {}
            players = {}
            lastslot = -1
            for line in data.split('\n')[3:]:
                m = re.match(self._regPlayer, line.strip())
                if m:
                    d = m.groupdict()
                    if int(m.group('slot')) > lastslot:
                        lastslot = int(m.group('slot'))
                        d['pbid'] = None
                        players[str(m.group('slot'))] = d
                    else:
                        self.debug('Duplicate or incorrect slot number - client ignored %s last slot %s' % (
                         m.group('slot'), lastslot))

            return players

    def getCvar(self, cvar_name):
        """
        Return a CVAR from the server.
        :param cvar_name: The CVAR name.
        """
        if self._reCvarName.match(cvar_name):
            val = self.write(cvar_name)
            self.debug('Get cvar %s = [%s]', cvar_name, val)
            m = None
            for f in self._reCvar:
                m = re.match(f, val)
                if m:
                    break

            if m:
                if m.group('cvar').lower() == cvar_name.lower():
                    try:
                        default_value = m.group('default')
                    except IndexError:
                        default_value = None

                    return b3.cvar.Cvar(m.group('cvar'), value=m.group('value'), default=default_value)
            else:
                return
        return

    def setCvar(self, cvar_name, value):
        """
        Set a CVAR on the server.
        :param cvar_name: The CVAR name
        :param value: The CVAR value
        """
        if re.match('^[a-z0-9_.]+$', cvar_name, re.IGNORECASE):
            self.debug('Set cvar %s = [%s]', cvar_name, value)
            self.write(self.getCommand('set', name=cvar_name, value=value))
        else:
            self.error('%s is not a valid cvar name', cvar_name)

    def set(self, cvar_name, value):
        """
        Set a CVAR on the server.
        :param cvar_name: The CVAR name
        :param value: The CVAR value
        """
        self.warning('Use of deprecated method: set(): please use: setCvar()')
        self.setCvar(cvar_name, value)

    def getMap(self):
        """
        Return the current map/level name.
        """
        data = self.write('status')
        if not data:
            return
        else:
            line = data.split('\n')[0]
            m = re.match(self._reMapNameFromStatus, line.strip())
            if m:
                return str(m.group('map'))
            return

    def getMaps(self):
        pass

    def getNextMap(self):
        pass

    def sync(self):
        """
        For all connected players returned by self.get_player_list(), get the matching Client
        object from self.clients (with self.clients.get_by_cid(cid) or similar methods) and
        look for inconsistencies. If required call the client.disconnect() method to remove
        a client from self.clients.
        This is mainly useful for games where clients are identified by the slot number they
        occupy. On map change, a player A on slot 1 can leave making room for player B who
        connects on slot 1.
        """
        plist = self.getPlayerList()
        mlist = {}
        for cid, c in plist.iteritems():
            client = self.clients.getByCID(cid)
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

    def authorizeClients(self):
        """
        For all connected players, fill the client object with properties allowing to find
        the user in the database (usualy guid, or punkbuster id, ip) and call the
        Client.auth() method.
        """
        players = self.getPlayerList(maxRetries=4)
        self.verbose('authorizeClients() = %s' % players)
        for cid, p in players.iteritems():
            sp = self.clients.getByCID(cid)
            if sp:
                sp.ip = p.get('ip', sp.ip)
                sp.pbid = p.get('pbid', sp.pbid)
                sp.guid = p.get('guid', sp.guid)
                sp.data = p
                sp.auth()

    def patch_b3_admin_plugin(self):
        """
        Monkey patches the admin plugin
        """

        def new_cmd_kick(this, data, client=None, cmd=None):
            """
            <name> [<reason>] - kick a player
            <fullexactname> [<reason>] - kick an incompletely authed player
            """
            m = this.parseUserCmd(data)
            if not m:
                client.message('^7Invalid parameters')
                return False
            cid, keyword = m
            reason = this.getReason(keyword)
            if not reason and client.maxLevel < this._noreason_level:
                client.message('^1ERROR: ^7You must supply a reason')
                return False
            sclient = this.findClientPrompt(cid, client)
            if sclient:
                if sclient.cid == client.cid:
                    this.console.say(self.getMessage('kick_self', client.exactName))
                    return True
                else:
                    if sclient.maxLevel >= client.maxLevel:
                        if sclient.maskGroup:
                            client.message("^7%s ^7is a masked higher level player, can't kick" % sclient.exactName)
                        else:
                            message = this.getMessage('kick_denied', sclient.exactName, client.exactName, sclient.exactName)
                            this.console.say(message)
                        return True
                    sclient.kick(reason, keyword, client)
                    return True

            elif re.match('^[0-9]+$', cid):
                this.console.kick(cid, reason, client)
            else:
                this.console.kickbyfullname(cid, reason, client)

        admin_plugin = self.getPlugin('admin')
        command = admin_plugin._commands['kick']
        command.func = new.instancemethod(new_cmd_kick, admin_plugin)
        command.help = new_cmd_kick.__doc__.strip()
        return
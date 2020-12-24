# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\cod.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'ThorN, xlr8or'
__version__ = '1.5.3'
import b3, b3.events, b3.parsers.punkbuster, re, string
from b3.parsers.q3a.abstractParser import AbstractParser
from threading import Timer

class CodParser(AbstractParser):
    gameName = 'cod'
    PunkBuster = None
    IpsOnly = False
    _guidLength = 6
    _reMap = re.compile('map ([a-z0-9_-]+)', re.IGNORECASE)
    _pbRegExp = re.compile('^[0-9a-f]{32}$', re.IGNORECASE)
    _logSync = 3
    _counter = {}
    _line_length = 65
    _line_color_prefix = ''
    _commands = {'message': 'tell %(cid)s %(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s', 
       'ban': 'banclient %(cid)s', 
       'unban': 'unbanuser %(name)s', 
       'tempban': 'clientkick %(cid)s'}
    _eventMap = {}
    _lineClear = re.compile('^(?:[0-9:]+\\s?)?')
    _lineFormats = (
     re.compile('^(?P<action>[a-z]+):\\s?(?P<data>.*)$', re.IGNORECASE),
     re.compile('^(?P<action>[A-Z]);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9-]{1,2});(?P<team>[a-z]+);(?P<name>[^;]+);(?P<aguid>[^;]*);(?P<acid>-1);(?P<ateam>world);(?P<aname>[^;]*);(?P<aweap>[a-z0-9_-]+);(?P<damage>[0-9.]+);(?P<dtype>[A-Z_]+);(?P<dlocation>[a-z_]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[A-Z]);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<team>[a-z]*);(?P<name>[^;]+);(?P<aguid>[^;]+);(?P<acid>[0-9]{1,2});(?P<ateam>[a-z]*);(?P<aname>[^;]+);(?P<aweap>[a-z0-9_-]+);(?P<damage>[0-9.]+);(?P<dtype>[A-Z_]+);(?P<dlocation>[a-z_]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[A-Z]);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<team>[a-z]*);(?P<name>[^;]+);(?P<aguid>[^;]*);(?P<acid>-1);(?P<ateam>[a-z]*);(?P<aname>[^;]+);(?P<aweap>[a-z0-9_-]+);(?P<damage>[0-9.]+);(?P<dtype>[A-Z_]+);(?P<dlocation>[a-z_]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[A-Z]);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<team>[a-z]*);(?P<name>[^;]+);(?P<aguid>[^;]*);(?P<acid>[0-9]{1,2});(?P<ateam>[a-z]*);(?P<aname>[^;]+);(?P<aweap>[a-z0-9_-]+);(?P<damage>[0-9.]+);(?P<dtype>[A-Z_]+);(?P<dlocation>[a-z_]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[A-Z]);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<team>[a-z]*);(?P<name>[^;]+);(?P<aguid>[^;]*);(?P<acid>[0-9]{1,2});(?P<aname>world);(?P<ateam>[a-z]*);(?P<aweap>none);(?P<damage>[0-9.]+);(?P<dtype>[A-Z_]+);(?P<dlocation>[a-z_]+))$', re.IGNORECASE),
     re.compile('^(?P<action>[A-Z]);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<team>[a-z]+);(?P<name>[^;]+);(?P<type>[a-z_]+))$', re.IGNORECASE),
     re.compile('^(?P<action>JT);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<team>[a-z]+);(?P<name>[^;]+);)$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<name>[^;]+);(?P<aguid>[^;]+);(?P<acid>[0-9]{1,2});(?P<aname>[^;]+);(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[a-z]+);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<name>[^;]+);(?P<text>.*))$', re.IGNORECASE),
     re.compile('^(?P<action>[A-Z]);(?P<data>(?P<guid>[^;]+);(?P<cid>[0-9]{1,2});(?P<name>[^;]+))$', re.IGNORECASE))
    _regPlayer = re.compile('^\\s*(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<guid>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+?)\\s*(?P<ip>(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])):?(?P<port>-?[0-9]{1,5})\\s*(?P<qport>-?[0-9]{1,5})\\s+(?P<rate>[0-9]+)$', re.IGNORECASE | re.VERBOSE)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        if not self.config.has_option('server', 'game_log'):
            self.critical("Your main config file is missing the 'game_log' setting in section 'server'")
            raise SystemExit(220)
        if self.IpsOnly:
            self.debug('Authentication method: Using IP instead of GUID!')
        self.clients.newClient('-1', guid='WORLD', name='World', hide=True, pbid='WORLD')
        if not self.config.has_option('server', 'punkbuster') or self.config.getboolean('server', 'punkbuster'):
            result = self.write('PB_SV_Ver')
            if result != '' and result[:7] != 'Unknown':
                self.info('punkbuster active: %s' % result)
                self.PunkBuster = b3.parsers.punkbuster.PunkBuster(self)
            else:
                self.warning('Punkbuster test failed: check your game server setup and B3 config!')
                self.debug('Disabling punkbuster support!')
        self._eventMap['warmup'] = self.getEventID('EVT_GAME_WARMUP')
        self._eventMap['restartgame'] = self.getEventID('EVT_GAME_ROUND_END')
        mapname = self.getMap()
        if mapname:
            self.game.mapName = mapname
            self.info('map is: %s' % self.game.mapName)
        self.debug('Forcing server cvar g_logsync to %s' % self._logSync)
        self.setCvar('g_logsync', self._logSync)
        try:
            self.game.fs_game = self.getCvar('fs_game').getString()
        except:
            self.game.fs_game = None
            self.warning('Could not query server for fs_game')

        try:
            self.game.fs_basepath = self.getCvar('fs_basepath').getString().rstrip('/')
            self.debug('fs_basepath: %s' % self.game.fs_basepath)
        except:
            self.game.fs_basepath = None
            self.warning('could not query server for fs_basepath')

        try:
            self.game.fs_homepath = self.getCvar('fs_homepath').getString().rstrip('/')
            self.debug('fs_homepath: %s' % self.game.fs_homepath)
        except:
            self.game.fs_homepath = None
            self.warning('could not query server for fs_homepath')

        try:
            self.game.shortversion = self.getCvar('shortversion').getString()
            self.debug('shortversion: %s' % self.game.shortversion)
        except:
            self.game.shortversion = None
            self.warning('Could not query server for shortversion')

        self.setVersionExceptions()
        self.debug('Parser started')
        return

    def OnK(self, action, data, match=None):
        victim = self.getClient(victim=match)
        if not victim:
            self.debug('No victim')
            self.OnJ(action, data, match)
            return None
        else:
            attacker = self.getClient(attacker=match)
            if not attacker:
                self.debug('No attacker')
                return None
            attacker.team = self.getTeam(match.group('ateam'))
            attacker.name = match.group('aname')
            victim.team = self.getTeam(match.group('team'))
            victim.name = match.group('name')
            event_key = 'EVT_CLIENT_KILL'
            if attacker.cid == victim.cid:
                event_key = 'EVT_CLIENT_SUICIDE'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team:
                event_key = 'EVT_CLIENT_KILL_TEAM'
            victim.state = b3.STATE_DEAD
            data = (float(match.group('damage')), match.group('aweap'), match.group('dlocation'), match.group('dtype'))
            return self.getEvent(event_key, data=data, client=attacker, target=victim)

    def OnD(self, action, data, match=None):
        victim = self.getClient(victim=match)
        if not victim:
            self.debug('No victim - attempt join')
            self.OnJ(action, data, match)
            return None
        else:
            attacker = self.getClient(attacker=match)
            if not attacker:
                self.debug('No attacker')
                return None
            attacker.team = self.getTeam(match.group('ateam'))
            attacker.name = match.group('aname')
            victim.team = self.getTeam(match.group('team'))
            victim.name = match.group('name')
            eventkey = 'EVT_CLIENT_DAMAGE'
            if attacker.cid == victim.cid:
                eventkey = 'EVT_CLIENT_DAMAGE_SELF'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team == victim.team:
                eventkey = 'EVT_CLIENT_DAMAGE_TEAM'
            data = (float(match.group('damage')), match.group('aweap'), match.group('dlocation'), match.group('dtype'))
            return self.getEvent(eventkey, data=data, client=attacker, target=victim)

    def OnQ(self, action, data, match=None):
        client = self.getClient(match)
        if client:
            client.disconnect()
        elif match.group('cid') in self._counter:
            cid = match.group('cid')
            self._counter[cid] = 'Disconnected'
            self.debug('Slot %s has disconnected or was forwarded to our http download location: removing from authentication queue...' % cid)
        return

    def OnJ(self, action, data, match=None):
        codguid = match.group('guid')
        cid = match.group('cid')
        name = match.group('name')
        if len(codguid) < self._guidLength:
            self.verbose2('Invalid GUID: %s. GUID length set to %s' % (codguid, self._guidLength))
            codguid = None
        client = self.getClient(match)
        if client:
            self.verbose2('Client object already exists')
            if not self.PunkBuster:
                if self.IpsOnly:
                    if name != client.name:
                        self.debug('This is not the correct client (%s <> %s): disconnecting..' % (name, client.name))
                        client.disconnect()
                        return
                    self.verbose2('client.name in sync: %s == %s' % (name, client.name))
                else:
                    if codguid != client.guid:
                        self.debug('This is not the correct client (%s <> %s): disconnecting...' % (codguid, client.guid))
                        client.disconnect()
                        return
                    self.verbose2('client.guid in sync: %s == %s' % (codguid, client.guid))
            client.state = b3.STATE_ALIVE
            client.name = name
            return self.getEvent('EVT_CLIENT_JOIN', client=client)
        else:
            if self._counter.get(cid) and self._counter.get(cid) != 'Disconnected':
                self.verbose('cid: %s already in authentication queue: aborting join' % cid)
                return
            self._counter[cid] = 1
            t = Timer(2, self.newPlayer, (cid, codguid, name))
            t.start()
            self.debug('%s connected: waiting for authentication...' % name)
            self.debug('Our authentication queue: %s' % self._counter)
            return

    def OnA(self, action, data, match=None):
        client = self.getClient(match)
        if not client:
            self.debug('No client - attempt join')
            self.OnJ(action, data, match)
            client = self.getClient(match)
            if not client:
                return None
        client.name = match.group('name')
        actiontype = match.group('type')
        self.verbose('On action: %s: %s' % (client.name, actiontype))
        return self.getEvent('EVT_CLIENT_ACTION', data=actiontype, client=client)

    def OnSay(self, action, data, match=None):
        client = self.getClient(match)
        if not client:
            self.debug('No client - attempt join')
            self.OnJ(action, data, match)
            client = self.getClient(match)
            if not client:
                return None
        data = match.group('text')
        if data and ord(data[:1]) == 21:
            data = data[1:]
        if self.encoding:
            try:
                data = data.decode(self.encoding)
            except Exception as msg:
                self.warning('ERROR: decoding data: %r', msg)

        if client.name != match.group('name'):
            client.name = match.group('name')
        return self.getEvent('EVT_CLIENT_SAY', data=data, client=client)

    def OnSayteam(self, action, data, match=None):
        client = self.getClient(match)
        if not client:
            self.debug('No client - attempt join')
            self.OnJ(action, data, match)
            client = self.getClient(match)
            if not client:
                return None
        data = match.group('text')
        if data and ord(data[:1]) == 21:
            data = data[1:]
        if self.encoding:
            try:
                data = data.decode(self.encoding)
            except Exception as msg:
                self.warning('ERROR: decoding data: %r', msg)

        if client.name != match.group('name'):
            client.name = match.group('name')
        return self.getEvent('EVT_CLIENT_TEAM_SAY', data=data, client=client)

    def OnTell(self, action, data, match=None):
        client = self.getClient(match)
        tclient = self.getClient(attacker=match)
        if not client:
            self.debug('No client - attempt join')
            self.OnJ(action, data, match)
            client = self.getClient(match)
            if not client:
                return None
        data = match.group('text')
        if data and ord(data[:1]) == 21:
            data = data[1:]
        if self.encoding:
            try:
                data = data.decode(self.encoding)
            except Exception as msg:
                self.warning('ERROR: decoding data: %r', msg)

        client.name = match.group('name')
        return self.getEvent('EVT_CLIENT_PRIVATE_SAY', data=data, client=client, target=tclient)

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

        self.verbose('...self.console.game.gameType: %s' % self.game.gameType)
        self.game.startRound()
        return self.getEvent('EVT_GAME_ROUND_START', data=self.game)

    def OnExitlevel(self, action, data, match=None):
        t = Timer(60, self.clients.sync)
        t.start()
        self.game.mapEnd()
        return self.getEvent('EVT_GAME_EXIT', data=data)

    def OnItem(self, action, data, match=None):
        guid, cid, name, item = string.split(data, ';', 3)
        client = self.clients.getByCID(cid)
        if client:
            return self.getEvent('EVT_CLIENT_ITEM_PICKUP', data=item, client=client)
        else:
            return

    def setVersionExceptions(self):
        """
        Dummy to enable shortversionexceptions for cod2.
        Use this function in inheriting parsers to override certain vars based on ie. shortversion.
        """
        pass

    def getTeam(self, team):
        """
        Return a B3 team given the team value.
        :param team: The team value
        """
        if team == 'allies':
            return b3.TEAM_BLUE
        else:
            if team == 'axis':
                return b3.TEAM_RED
            return b3.TEAM_UNKNOWN

    def connectClient(self, ccid):
        """
        Return the client matchign the given slot number.
        :param ccid: The client slot number
        """
        players = self.getPlayerList()
        self.verbose('connectClient() = %s' % players)
        for cid, p in players.iteritems():
            if int(cid) == int(ccid):
                self.debug('%s found in status/playerList' % p['name'])
                return p

    def newPlayer(self, cid, codguid, name):
        """
        Build a new client using data in the authentication queue.
        :param cid: The client slot number
        :param codguid: The client GUID
        :param name: The client name
        """
        if not self._counter.get(cid):
            self.verbose('newPlayer thread no longer needed: key no longer available')
            return
        else:
            if self._counter.get(cid) == 'Disconnected':
                self.debug('%s disconnected: removing from authentication queue' % name)
                self._counter.pop(cid)
                return
            self.debug('newClient: %s, %s, %s' % (cid, codguid, name))
            sp = self.connectClient(cid)
            if sp and self.PunkBuster:
                self.debug('sp: %s' % sp)
                if not re.match(self._pbRegExp, sp['pbid']):
                    self.debug('PB-id is not valid: giving it another try')
                    self._counter[cid] += 1
                    t = Timer(4, self.newPlayer, (cid, codguid, name))
                    t.start()
                    return
                if self.IpsOnly:
                    guid = sp['ip']
                    pbid = sp['pbid']
                else:
                    guid = sp['pbid']
                    pbid = guid
                ip = sp['ip']
                if self._counter.get(cid):
                    self._counter.pop(cid)
                else:
                    return
            elif sp:
                if self.IpsOnly:
                    codguid = sp['ip']
                if not codguid:
                    self.warning('Missing or wrong CodGuid and PunkBuster is disabled: cannot authenticate!')
                    if self._counter.get(cid):
                        self._counter.pop(cid)
                    return
                guid = codguid
                pbid = ''
                ip = sp['ip']
                if self._counter.get(cid):
                    self._counter.pop(cid)
                else:
                    return
            else:
                if self._counter.get(cid) > 10:
                    self.debug('Could not auth %s: giving up...' % name)
                    if self._counter.get(cid):
                        self._counter.pop(cid)
                    return
                if self._counter.get(cid):
                    self.debug('%s not yet fully connected: retrying...#:%s' % (name, self._counter.get(cid)))
                    self._counter[cid] += 1
                    t = Timer(4, self.newPlayer, (cid, codguid, name))
                    t.start()
                else:
                    self.warning('All authentication attempts failed')
                return
            client = self.clients.newClient(cid, name=name, ip=ip, state=b3.STATE_ALIVE, guid=guid, pbid=pbid, data={'codguid': codguid})
            self.queueEvent(self.getEvent('EVT_CLIENT_JOIN', client=client))
            return

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
                admin.message('%s ^7unbanned but has no punkbuster id' % client.exactName)
        else:
            name = self.stripColors(client.exactName)
            result = self.write(self.getCommand('unban', name=name, reason=reason))
            if admin:
                admin.message(result)

    def getMaps(self):
        """
        Return the available maps/levels name
        """
        maps = self.getCvar('sv_mapRotation')
        nmaps = []
        if maps:
            maps = re.findall(self._reMap, maps[0])
            for m in maps:
                if m[:3] == 'mp_':
                    m = m[3:]
                nmaps.append(m.title())

        return nmaps

    def getNextMap(self):
        """
        Return the next map/level name to be played.
        """
        if not self.game.mapName:
            return
        else:
            maps = self.getCvar('sv_mapRotation')
            if maps:
                maps = re.findall(self._reMap, maps[0])
                gmap = self.game.mapName.strip().lower()
                found = False
                nmap = ''
                for nmap in maps:
                    nmap = nmap.strip().lower()
                    if found:
                        found = nmap
                        break
                    elif nmap == gmap:
                        found = True

                if found is True:
                    nmap = maps[0].strip().lower()
                if found:
                    if nmap[:3] == 'mp_':
                        nmap = nmap[3:]
                    return nmap.title()
                return
            return
            return

    def sync(self):
        """
        For all connected players returned by self.get_player_list(), get the matching Client
        object from self.clients (with self.clients.get_by_cid(cid) or similar methods) and
        look for inconsistencies. If required call the client.disconnect() method to remove
        a client from self.clients.
        """
        self.debug('synchronising clients...')
        plist = self.getPlayerList(maxRetries=4)
        mlist = {}
        for cid, c in plist.iteritems():
            client = self.clients.getByCID(cid)
            if client:
                if client.guid and 'guid' in c and not self.IpsOnly:
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
                if self.IpsOnly:
                    sp.guid = p.get('ip', sp.guid)
                else:
                    sp.guid = p.get('guid', sp.guid)
                sp.data = p
                sp.auth()
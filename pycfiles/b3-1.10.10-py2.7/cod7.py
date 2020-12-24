# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\cod7.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'Freelander, Courgette, Just a baka, Bravo17'
__version__ = '1.3.2'
import os, b3, re, string, b3.parsers.cod5, b3.parsers.q3a.rcon
from threading import Timer

class Cod7Rcon(b3.parsers.q3a.rcon.Rcon):
    rconsendstring = b'\xff\xff\xff\xff\x00%s %s\x00'
    rconreplystring = b'\xff\xff\xff\xff\x01print\n'


class Cod7Parser(b3.parsers.cod5.Cod5Parser):
    gameName = 'cod7'
    IpsOnly = False
    OutputClass = Cod7Rcon
    _guidLength = 5
    _usePreMatchLogic = True
    _preMatch = False
    _elFound = True
    _igBlockFound = False
    _sgFound = False
    _logTimer = 0
    _logTimerOld = 0
    _cod7httpplugin = None
    _commands = {'message': 'tell %(cid)s %(message)s', 
       'say': 'say %(message)s', 
       'set': 'setadmindvar %(name)s "%(value)s"', 
       'kick': 'clientkick %(cid)s "%(reason)s"', 
       'ban': 'banclient %(cid)s', 
       'unban': 'unbanuser "%(name)s"', 
       'tempban': 'clientkick %(cid)s "%(reason)s"'}
    _actionMap = ('AD', 'VD')
    _regPlayer = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<guid>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)(?P<qportsep>[-\\s]+)(?P<qport>[0-9-]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)
    _regPlayerWithDemoclient = re.compile('^(?P<slot>[0-9]+)\\s+(?P<score>[0-9-]+)\\s+(?P<ping>[0-9]+)\\s+(?P<guid>[0-9]+)\\s+(?P<name>.*?)\\s+(?P<last>[0-9]+)\\s+(?P<ip>[0-9.]+|unknown):?(?P<port>[0-9-]+)?(?P<qportsep>[-\\s]+)(?P<qport>[0-9-]+)\\s+(?P<rate>[0-9]+)$', re.IGNORECASE)

    def startup(self):
        """
        Called after the parser is created before run().
        """
        client = self.clients.newClient('-1', guid='WORLD', name='World', hide=True, pbid='WORLD')
        self._cod7httpplugin = self.getPlugin('cod7http')
        if self._cod7httpplugin is None:
            self.critical('Cannot find cod7http plugin')
            raise SystemExit(220)
        mapname = self.getMap()
        if mapname:
            self.game.mapName = mapname
            self.info('map is: %s' % self.game.mapName)
        if self.config.has_option('server', 'use_prematch_logic'):
            self._usePreMatchLogic = self.config.getboolean('server', 'use_prematch_logic')
        if self._usePreMatchLogic:
            self._regPlayer, self._regPlayerWithDemoclient = self._regPlayerWithDemoclient, self._regPlayer
            playerList = self.getPlayerList()
            self._regPlayer, self._regPlayerWithDemoclient = self._regPlayerWithDemoclient, self._regPlayer
            if len(playerList) >= 4:
                self.verbose('PREMATCH OFF: PlayerCount >=4: not a Pre-Match')
                self._preMatch = False
            elif '0' in playerList and playerList['0']['guid'] == '0':
                self.verbose('PREMATCH OFF: Got a democlient presence: not a Pre-Match')
                self._preMatch = False
            else:
                self.verbose('PREMATCH ON: PlayerCount < 4, got no democlient presence: defaulting to a pre-match.')
                self._preMatch = True
        else:
            self._preMatch = False
        self.debug('Forcing server cvar g_logsync to %s and turning UNIX timestamp log timers off' % self._logSync)
        self.write('g_logsync %s' % self._logSync)
        self.write('g_logTimeStampInSeconds 0')
        self.setVersionExceptions()
        self.debug('parser started')
        return

    def plugins_started(self):
        """
        Called after the parser loaded and started all plugins.
        """
        self.debug('Admin plugin not patched')

    def parse_line(self, line):
        """
        Parse a log line creating necessary events.
        :param line: The log line to be parsed
        """
        m = self.getLineParts(line)
        if not m:
            return False
        match, action, data, client, target = m
        func = 'On%s' % string.capwords(action).replace(' ', '')
        t = re.match(self._lineTime, line)
        if t:
            self._logTimerOld = self._logTimer
            self._logTimer = int(t.group('minutes')) * 60 + int(t.group('seconds'))
        if self._preMatch and (func == 'OnD' or func == 'OnK' or func == 'OnAd' or func == 'OnVd'):
            self.verbose('PRE-MATCH: ignoring kill/damage')
            return False
        if func == 'OnInitgame':
            if not self._igBlockFound:
                self._igBlockFound = True
                self.verbose('found 1st InitGame from block')
            elif self._logTimerOld <= self._logTimer:
                self.verbose('found 2nd InitGame from block: ignoring')
                return False
        elif self._usePreMatchLogic and func == 'OnExitlevel':
            self._preMatch = True
            self.debug('PRE-MATCH ON: found ExitLevel')
            self._elFound = True
            self._igBlockFound = False
        elif func == 'OnShutdowngame':
            self._sgFound = True
            self._igBlockFound = False
        if self._preMatch and not self._elFound and self._igBlockFound and self._sgFound and self._logTimerOld <= self._logTimer:
            self._preMatch = False
            self.debug('PRE-MATCH OFF: found a round change')
            self._igBlockFound = False
            self._sgFound = False
        elif self._logTimerOld > self._logTimer:
            self.debug('Old timer: %s / New timer: %s' % (self._logTimerOld, self._logTimer))
            if self._usePreMatchLogic:
                self._preMatch = True
                self.debug('PRE-MATCH ON: Server crash/restart detected')
            else:
                self.debug('Server crash/restart detected')
            self._elFound = False
            self._igBlockFound = False
            self._sgFound = False
            self.write('setadmindvar g_logsync %s' % self._logSync)
            self.write('setadmindvar g_logTimeStampInSeconds 0')
        else:
            self._elFound = False
            self._sgFound = False
        if hasattr(self, func):
            func = getattr(self, func)
            event = func(action, data, match)
            if event:
                self.queueEvent(event)
        elif action in self._eventMap:
            self.queueEvent(self.getEvent(self._eventMap[action], data=data, client=client, target=target))
        elif action in self._actionMap:
            self.translateAction(action, data, match)
        else:
            self.queueEvent(self.getEvent('EVT_UNKNOWN', str(action) + ': ' + str(data), client, target))

    def read(self):
        """
        Read from game server log file.
        """
        filestats = os.fstat(self.input.fileno())
        thread_alive = self._cod7httpplugin.httpThreadalive()
        if not thread_alive:
            self.verbose('Cod7Http Plugin has stopped working: restarting')
            self.restart()
        if self.input.tell() > filestats.st_size:
            self.debug('Parser: game log is suddenly smaller than it was before (%s bytes, now %s), the log was probably either rotated or emptied. B3 will now re-adjust to the new size of the log.' % (
             str(self.input.tell()), str(filestats.st_size)))
            self.input.seek(0, os.SEEK_END)
        return self.input.readlines()

    def OnJ(self, action, data, match=None):
        codguid = match.group('guid')
        cid = match.group('cid')
        name = match.group('name')
        if codguid == '0' and cid == '0' and name == '[3arc]democlient':
            self.verbose('Authentication not required for [3arc]democlient: aborting join...')
            self._preMatch = 0
            return
        else:
            if len(codguid) < self._guidLength:
                self.verbose2('Invalid GUID: %s' % codguid)
                codguid = None
            client = self.getClient(match)
            if client:
                self.verbose2('Client object already exists')
                if not self.PunkBuster:
                    if self.IpsOnly:
                        if name != client.name:
                            self.debug('This is not the correct client (%s <> %s): disconnecting' % (name, client.name))
                            client.disconnect()
                            return
                        self.verbose2('client.name in sync: %s == %s' % (name, client.name))
                    else:
                        if codguid != client.guid:
                            self.debug('This is not the correct client (%s <> %s): disconnecting' % (codguid, client.guid))
                            client.disconnect()
                            return
                        self.verbose2('client.guid in sync: %s == %s' % (codguid, client.guid))
                client.state = b3.STATE_ALIVE
                client.name = name
                return self.getEvent('EVT_CLIENT_JOIN', client=client)
            if self._counter.get(cid) and self._counter.get(cid) != 'Disconnected':
                self.verbose('cid: %s already in authentication queue: aborting join...' % cid)
                return
            self._counter[cid] = 1
            t = Timer(2, self.newPlayer, (cid, codguid, name))
            t.start()
            self.debug('%s connected: waiting for authentication...' % name)
            self.debug('Our authentication queue: %s' % self._counter.__str__())
            return

    def OnK(self, action, data, match=None):
        victim = self.clients.getByGUID(match.group('guid'))
        if not victim:
            self.debug('No victim %s' % match.groupdict())
            self.OnJ(action, data, match)
            return
        else:
            attacker = self.clients.getByGUID(match.group('aguid'))
            if not attacker:
                if match.group('acid') == '-1' or match.group('aname') == 'world':
                    self.verbose('World kill')
                    attacker = self.getClient(attacker=match)
                else:
                    self.debug('No attacker %s' % match.groupdict())
                    return
            if match.group('ateam'):
                attacker.team = self.getTeam(match.group('ateam'))
            if match.group('team'):
                victim.team = self.getTeam(match.group('team'))
            eventkey = 'EVT_CLIENT_KILL'
            if attacker == victim or attacker.cid == '-1':
                self.verbose('Suicide detected: attacker.cid: %s, victim.cid: %s' % (attacker.cid, victim.cid))
                eventkey = 'EVT_CLIENT_SUICIDE'
            elif attacker.team != b3.TEAM_UNKNOWN and attacker.team and victim.team and attacker.team == victim.team:
                self.verbose('Team kill detected: %s team killed %s' % (attacker.name, victim.name))
                eventkey = 'EVT_CLIENT_KILL_TEAM'
            victim.state = b3.STATE_DEAD
            data = (float(match.group('damage')), match.group('aweap'), match.group('dlocation'), match.group('dtype'))
            return self.getEvent(eventkey, data=data, client=attacker, target=victim)


from b3.parser import Parser
originalLoadArbPlugins = Parser.loadArbPlugins

def newLoadArbPlugins(self):
    """
    Call original loadArbPlugin method from the Parser class then
    unload the httpytail plugin then load the cod7http plugin instead.
    """
    print 'running newLoadArbPlugins '
    originalLoadArbPlugins(self)
    if self.config.has_option('server', 'game_log') and self.config.get('server', 'game_log')[0:7] == 'http://':
        if 'httpytail' in self._plugins:
            self.screen.write('Unloading        : http Plugin\n')
            del self._plugins['httpytail']
        p = 'cod7http'
        self.bot('Loading %s', p)
        try:
            pluginModule = self.pluginImport(p)
            self._plugins[p] = getattr(pluginModule, '%sPlugin' % p.title())(self)
            version = getattr(pluginModule, '__version__', 'Unknown Version')
            author = getattr(pluginModule, '__author__', 'Unknown Author')
            self.bot('Plugin %s (%s - %s) loaded', p, version, author)
            self.screen.write('Loading          : COD7 http Plugin\n')
            self.screen.flush()
        except Exception as msg:
            self.critical('Error loading plugin: %s', msg)
            raise SystemExit('ERROR while loading %s' % p)


Parser.loadArbPlugins = newLoadArbPlugins
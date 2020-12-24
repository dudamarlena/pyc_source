# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\gameConfig.py
# Compiled at: 2018-10-26 00:07:21
# Size of source mod 2**32: 31274 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from s2clientprotocol import sc2api_pb2 as sc_pb
from six import iteritems
import glob, json, os, portpicker, random, re, time
from sc2common import types
from sc2gameLobby import dateFormat
from sc2gameLobby import gameConstants as c
from sc2gameLobby import ipAddresses
from sc2gameLobby import runConfigs
from sc2gameLobby import versions
from sc2players import getPlayer, buildPlayer, PlayerRecord, PlayerPreGame
from sc2players import constants as playerConstants
from sc2ladderMgmt.ladders import Ladder

def activeConfigs():
    """identify all configurations which are currently active"""
    return glob.glob(os.path.join(c.FOLDER_ACTIVE_CONFIGS, '*.json'))


def clearConfigs():
    """remove all active configurations, if any"""
    for cfg in activeConfigs():
        os.remove(cfg)


def loadHostConfig(timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        for cfgName in activeConfigs():
            if re.search('^host', cfgName.split(os.sep)[(-1)]):
                cfg = Config()
                cfg.load(cfgName)
                return cfg

    raise c.TimeoutExceeded('could not identify the host config within %d seconds.' % timeout)


def getSlaveConfigs(numConfigs=1, timeout=15):
    ret = set()
    start = time.time()
    while len(ret) < numConfigs:
        if time.time() - start > timeout:
            raise c.TimeoutExceeded('could not identify any slave configswithin %d seconds' % timeout)
        for cfgName in activeConfigs():
            if re.search('^host', cfgName):
                pass
            else:
                cfg = Config(host=True)
                cfg.load(cfgName)
                ret.add(cfg)

    return ret


class Config(object):
    __doc__ = 'the grand collection of information that determines how a Starcraft 2\n    game is setup and intended to behave'

    def __init__(self, load=None, expo=c.DEFAULT_EXPANSION, version=None, ladder=None, players=[], whichPlayer='', mode=None, themap=None, numObservers=0, start=None, trust=True, ipAddress=[], ports=[], host=[], slaves=[], fogDisabled=False, stepSize=0, opponents=[], fullscreen=True, raw=False, score=False, feature=False, render=False, replay=None, debug=False):
        self._gotPorts = False
        if isinstance(players, list):
            pass
        else:
            if hasattr(players, '__iter__'):
                players = list(players)
            else:
                players = [
                 players]
            self.expo = expo
            self.version = version
            self.ladder = ladder
            self.players = players
            self.thePlayer = whichPlayer
            self.mode = mode
            self.themap = themap
            self.numObserve = int(numObservers)
            self.start = start
            self.trustOpps = trust
            self.ipAddress = ipAddress
            self.ports = ports
            self.host = host
            self.slavePorts = slaves
            self.ladderMsg = ''
            self.scenario = {}
            self.fogDisabled = fogDisabled
            self.stepSize = int(stepSize)
            self.opponents = opponents
            self.fullscreen = fullscreen
            self.raw = raw
            self.score = score
            self.feature = feature
            self.render = render
            self.replay = replay
            self.reqFiles = []
            self.debug = debug
            if load:
                self.load(load)
            else:
                self.inflate()
            self.isCustom = bool(self.opponents or self.fogDisabled or self.themap or self.stepSize)
        if self.version == None:
            self.version = self.getVersion()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        name = self.__class__.__name__
        if self.slavePorts:
            ip = [str(x) for x in self.host]
        else:
            ip = [str(x) for x in self.connection]
        ipStr = ' @ %s' % ':'.join(ip) if ip else ''
        return '<%s %s %s%s>' % (name, self.installedApp.name(), self.version, ipStr)

    def __del__(self):
        self.returnPorts()
        try:
            self.disable()
        except IOError:
            pass

    @property
    def attrs(self):
        data = dict(self.__dict__)
        for k, v in sorted(iteritems(data)):
            if re.search('^_', k):
                del data[k]

        return data

    @property
    def agents(self):
        """identify which players are agents (not observers or computers). Errors if flattened."""
        ret = []
        for player in self.players:
            if player.isComputer:
                pass
            else:
                try:
                    if player.observer:
                        continue
                except:
                    pass

                ret.append(player)

        return ret

    @property
    def agentRaces(self):
        """identify the races of the players that are agents. Errors if flattened."""
        return [player.selectedRace for player in self.players if not player.isComputer]

    @property
    def computers(self):
        """identify the players that are Blizzard's built-in bots. Errors if flattened."""
        return [player for player in self.players if player.isComputer]

    @property
    def allLobbySlots(self):
        """the current configuration of the lobby's players, defined before the match starts"""
        if self.debug:
            p = [
             'Lobby Configuration detail:'] + [
             '    %s:%s%s' % (p, ' ' * (12 - len(p.type)), p.name)]
            if self.observers:
                p += ['    observers: %d' % self.observers]
            print(os.linesep.join(p))
        return (
         self.agents, self.computers, self.observers)

    @property
    def connection(self):
        """identify the remote connection parameters"""
        self.getPorts()
        self.getIPaddresses()
        return (self.ipAddress, self.ports)

    @property
    def execPath(self):
        """the executable application's path"""
        vers = self.version.label if self.version else None
        return self.installedApp.exec_path(vers)

    @property
    def is64bit(self):
        """whether the this machine is 64-bit capable or not"""
        return self.installedApp.is64bit

    @property
    def installedApp(self):
        """identify the propery application to launch, given the configuration"""
        try:
            return self._installedApp
        except:
            self._installedApp = runConfigs.get()
            return self._installedApp

    @property
    def interfaces(self):
        return (self.raw, self.score,
         self.feature, self.render)

    @property
    def isHost(self):
        """is the host if it lacks host details"""
        return not bool(self.host) and bool(self.slavePorts)

    @property
    def isMultiplayer(self):
        return self.numGameClients > 1

    @property
    def mapData(self):
        """the raw, binary contents of the Starcraft2 map file"""
        return self.themap.rawData

    @property
    def mapLocalPath(self):
        return self.themap.path

    @property
    def name(self):
        return os.path.join(c.FOLDER_ACTIVE_CONFIGS, '%s_%s.json' % (os.getpid(), dateFormat.now(self.start)))

    @property
    def numAgents(self):
        return len(self.agents)

    @property
    def numBots(self):
        return len(self.computers)

    @property
    def numGameClients(self):
        """the number of game client connections in the match"""
        return self.numAgents + self.numObserve

    @property
    def numPlayers(self):
        return len(self.players)

    @property
    def observers(self):
        """the players who are actually observers"""
        ret = []
        for player in self.players:
            try:
                if player.observer:
                    ret.append(player)
            except:
                pass

        return ret

    @property
    def os(self):
        """the operating system this match is loaded on"""
        return self.installedApp.name()

    @property
    def participants(self):
        """agents + computers (i.e. all non-observers)"""
        ret = []
        for p in self.players:
            try:
                if p.isComputer:
                    ret.append(p)
                if not p.isObserver:
                    ret.append(p)
            except AttributeError:
                pass

        return ret

    @property
    def realtime(self):
        """whether the game progresses in realtime or requires each player to
        summit step requests to advance the game"""
        return not bool(self.stepSize)

    @property
    def teams(self):
        players = self.participants
        div = len(players) / 2.0
        teamSize = int(div)
        if div - teamSize > 0.49:
            teamSize += 1
        return (
         players[:teamSize], players[teamSize:])

    def addPlayer(self, player):
        if not isinstance(player, PlayerPreGame):
            raise ValueError('%s must be a %s' % (player, PlayerPreGame))
        self.players.append(player)

    def clientInitHost(self):
        """extract ipAddress information used by the local client to connect to another SC2 client at this IP address"""
        if self.host:
            return self.host[0]
        else:
            return self.getIPaddresses()[(-1)]

    def clientInitPort(self):
        """extract the port that is used to connect to the locally launched SC2 client"""
        ports = self.getPorts()
        return ports[2]

    def disable(self):
        try:
            os.remove(self.name)
        except:
            pass

    def display(self, header=''):
        print(self)
        h = '[%s]  ' % header.upper() if header else ''
        for k, v in sorted(iteritems(self.attrs)):
            print('%s%16s : %s' % (h, k, v))

    def flatten(self, data=None):
        """reduce all objects into simplified values as a attr dictionary that
        could be transformed back into a full configuration via inflate()"""
        if data == None:
            data = self.attrs
        ret = {}
        for k, v in iteritems(data):
            if not v:
                continue
            else:
                if k == 'expo':
                    v = v.type
                else:
                    if k == 'version':
                        v = v.label
                    else:
                        if k == 'ladder':
                            v = v.name
                        else:
                            if k == 'players':
                                newPs = []
                                for i, p in enumerate(v):
                                    try:
                                        diff = p.difficulty.type
                                    except:
                                        diff = p.difficulty

                                    if isinstance(p, PlayerPreGame):
                                        newPs.append((p.name, p.type.type, p.initCmd, p.initOptions, diff, p.rating, p.selectedRace.type, self.numObserve, p.playerID, p.raceDefault))
                                    else:
                                        newPs.append((p.name, p.type.type, p.initCmd, p.initOptions, diff, p.rating))

                                ret[k] = newPs
                                continue
                            else:
                                if k == 'mode':
                                    if self.mode:
                                        v = v.type
            if k == 'themap':
                if self.themap:
                    v = v.name
            ret[k] = v

        return ret

    def inflate(self, newData={}):
        """ensure all object attribute values are objects"""
        from sc2maptool.functions import selectMap
        from sc2maptool.mapRecord import MapRecord
        self.__dict__.update(newData)
        if self.expo:
            if not isinstance(self.expo, types.ExpansionNames):
                self.expo = types.ExpansionNames(self.expo)
        if self.version:
            if not isinstance(self.version, versions.Version):
                self.version = versions.Version(self.version)
        if self.ladder:
            if not isinstance(self.ladder, Ladder):
                self.ladder = Ladder(self.ladder)
        for i, player in enumerate(self.players):
            if isinstance(player, str):
                self.players[i] = getPlayer(player)
            else:
                if not isinstance(player, PlayerRecord):
                    self.players[i] = buildPlayer(*player)

        if self.mode:
            if not isinstance(self.mode, types.GameModes):
                self.mode = types.GameModes(self.mode)
        if self.themap:
            if not isinstance(self.themap, MapRecord):
                self.themap = selectMap(name=(self.themap))

    def launchApp(self, **kwargs):
        """Launch Starcraft2 process in the background using this configuration.
        WARNING: if the same IP address and port are specified between multiple
                 SC2 process instances, all subsequent processes after the first
                 will fail to initialize and crash.
        """
        app = self.installedApp
        vers = self.getVersion()
        return (app.start)(version=vers, full_screen=self.fullscreen, 
         verbose=self.debug, **kwargs)

    def load(self, cfgFile=None, timeout=None):
        """expect that the data file has already been established"""
        if not cfgFile:
            cfgs = activeConfigs()
            if len(cfgs) > 1:
                raise Exception('found too many configurations (%s); not clear which to load: %s' % (len(cfgs), cfgs))
            else:
                if len(cfgs) < 1:
                    if timeout:
                        startWait = time.time()
                        timeReported = 0
                        while not cfgs:
                            timeWaited = time.time() - startWait
                            if timeWaited > timeout:
                                raise c.TimeoutExceeded('could not join game after %s seconds' % timeout)
                            try:
                                cfgs = activeConfigs()
                            except:
                                if self.debug:
                                    if timeWaited - timeReported >= 1:
                                        timeReported += 1
                                        print('second(s) waited for game to appear:  %d' % timeReported)

                    else:
                        raise Exception('must have a saved configuration to load or allow loading via timeout setting')
            cfgFile = cfgs.pop()
        try:
            with open(cfgFile, 'rb') as (f):
                data = f.read()
        except TypeError as e:
            print('ERROR %s: %s %s' % (e, cfgFile, type(cfgFile)))
            raise

        self.loadJson(data)
        if self.debug:
            print('configuration loaded: %s' % self.name)
            self.display()

    def loadJson(self, data):
        """convert the json data into updating this obj's attrs"""
        if not isinstance(data, dict):
            data = json.loads(data)
        self.__dict__.update(data)
        self.inflate()
        return self

    def toJson(self, data=None, pretty=False):
        """convert the flattened dictionary into json"""
        if data == None:
            data = self.attrs
        data = self.flatten(data)
        ret = json.dumps(data, indent=4, sort_keys=True)
        return ret

    def getVersion(self):
        """the executable application's version"""
        if isinstance(self.version, versions.Version):
            return self.version
        else:
            if self.version:
                version = versions.Version(self.version)
                if version.baseVersion not in self.installedApp.versionMap():
                    raise runConfigs.lib.SC2LaunchError('specified game version %s executable is not available.%s    available:  %s' % (
                     version, os.linesep, '  '.join(self.installedApp.listVersions())))
                self.version = version
            else:
                path = self.installedApp.exec_path()
                vResult = self.installedApp.mostRecentVersion
                self.version = versions.Version(vResult)
            if self.debug:
                print(os.linesep.join([
                 'Game configuration detail:',
                 '    platform:   %s' % self.os,
                 '    app:        %s' % self.execPath,
                 '    version:    %s' % self.version]))
            return self.version

    def getIPaddresses(self):
        """identify the IP addresses where this process client will launch the SC2 client"""
        if not self.ipAddress:
            self.ipAddress = ipAddresses.getAll()
        return self.ipAddress

    def getPorts(self):
        """acquire ports to be used by the SC2 client launched by this process"""
        if self.ports:
            return self.ports
        else:
            if not self._gotPorts:
                self.ports = [portpicker.pick_unused_port(),
                 portpicker.pick_unused_port(),
                 portpicker.pick_unused_port()]
                self._gotPorts = True
            return self.ports

    def requestCreateDetails(self):
        """add configuration to the SC2 protocol create request"""
        createReq = sc_pb.RequestCreateGame(realtime=(self.realtime),
          disable_fog=(self.fogDisabled),
          random_seed=(int(time.time())),
          local_map=sc_pb.LocalMap(map_path=(self.mapLocalPath), map_data=(self.mapData)))
        for player in self.players:
            reqPlayer = createReq.player_setup.add()
            playerObj = PlayerPreGame(player)
            if playerObj.isComputer:
                reqPlayer.difficulty = playerObj.difficulty.gameValue()
            reqPlayer.type = c.types.PlayerControls(playerObj.control).gameValue()
            reqPlayer.race = playerObj.selectedRace.gameValue()

        return createReq

    def requestJoinDetails(self):
        """add configuration information to the SC2 protocol join request
    REQUIREMENTS FOR SUCCESSFUL LAUNCH:
    server game_port must match between all join requests to client (represents the host's port to sync game clients)
    server base_port
    client game_port must be unique between each client (represents ???)
    client base_port
    client shared_port must match between all join requests to client
        """
        raw, score, feature, rendered = self.interfaces
        interface = sc_pb.InterfaceOptions()
        interface.raw = raw
        interface.score = score
        interface.feature_layer.width = 24
        joinReq = sc_pb.RequestJoinGame(options=interface,
          race=(self.whoAmI().selectedRace.gameValue()))
        if self.host:
            hostPorts = self.host[1]
            joinReq.server_ports.game_port = hostPorts[0]
            joinReq.server_ports.base_port = hostPorts[1]
            joinReq.shared_port = hostPorts[2]
            clientPorts = joinReq.client_ports.add()
            clientPorts.game_port = self.ports[0]
            clientPorts.base_port = self.ports[1]
            ret = self.ports[2]
        else:
            if self.isMultiplayer:
                if len(self.ports) < 5:
                    self.ports += [
                     portpicker.pick_unused_port(),
                     portpicker.pick_unused_port()]
                joinReq.server_ports.game_port = self.ports[0]
                joinReq.server_ports.base_port = self.ports[1]
                joinReq.shared_port = self.ports[2]
                clientPorts = joinReq.client_ports.add()
                clientPorts.game_port = self.ports[3]
                clientPorts.base_port = self.ports[4]
        return joinReq

    def returnPorts(self):
        """deallocate specific ports on the current machine"""
        if self._gotPorts:
            map(portpicker.return_port, self.ports)
            self._gotPorts = False
        self.ports = []

    def save(self, filename=None, debug=False):
        """save a data file such that all processes know the game that is running"""
        if not filename:
            filename = self.name
        with open(filename, 'w') as (f):
            f.write(self.toJson(self.attrs))
        if self.debug or debug:
            print('saved configuration %s' % self.name)
            for k, v in sorted(iteritems(self.attrs)):
                print('%15s : %s' % (k, v))

    def updateIDs(self, ginfo, tag=None, debug=False):
        """ensure all player's playerIDs are correct given game's info"""
        thisPlayer = self.whoAmI()
        for pInfo in ginfo.player_info:
            pID = pInfo.player_id
            if pID == thisPlayer.playerID:
                pass
            else:
                pCon = c.types.PlayerControls(pInfo.type)
                rReq = c.types.SelectRaces(pInfo.race_requested)
                for p in self.players:
                    if p.playerID:
                        if p.playerID != pID:
                            continue
                        elif p.control == pCon:
                            if p.selectedRace == rReq:
                                p.playerID = pID
                                if debug:
                                    print('[%s] match contains %s.' % (tag, p))
                                pID = 0
                                break

            if pID:
                raise c.UnknownPlayer('could not match %s %s %s to any existing player of %s' % (
                 pID, pCon, rReq, self.players))

    def whoAmI(self):
        """return the player object that owns this configuration"""
        self.inflate()
        if self.thePlayer:
            for p in self.players:
                if p.name != self.thePlayer:
                    continue
                return p

        else:
            if len(self.players) == 1:
                ret = self.players[0]
                self.thePlayer = ret.name
                return ret
        raise Exception('could not identify which player this is given %s (%s)' % (self.players, self.thePlayer))
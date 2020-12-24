# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\moh.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'Bakes, Courgette'
__version__ = '1.9'
import time, b3.clients, b3.events, b3.functions
from b3.parsers.frostbite.abstractParser import AbstractParser
from b3.parsers.frostbite.util import PlayerInfoBlock
SAY_LINE_MAX_LENGTH = 100

class MohParser(AbstractParser):
    gameName = 'moh'
    _gameServerVars = ('serverName', 'gamePassword', 'punkBuster', 'hardCore', 'ranked',
                       'skillLimit', 'noUnlocks', 'noAmmoPickups', 'realisticHealth',
                       'supportAction', 'preRoundLimit', 'roundStartTimerPlayersLimit',
                       'roundStartTimerDelay', 'tdmScoreCounterMaxScore', 'clanTeams',
                       'friendlyFire', 'currentPlayerLimit', 'maxPlayerLimit', 'playerLimit',
                       'bannerUrl', 'serverDescription', 'noCrosshairs', 'noSpotting',
                       'teamKillCountForKick', 'teamKillValueForKick', 'teamKillValueIncrease',
                       'teamKillValueDecreasePerSecond', 'idleTimeout')

    def startup(self):
        """
        Called after the parser is created before run().
        """
        AbstractParser.startup(self)
        self.clients.newClient('Server', guid='Server', name='Server', hide=True, pbid='Server', team=b3.TEAM_UNKNOWN)

    def pluginsStarted(self):
        """
        Called after the parser loaded and started all plugins.
        Overwrite this in parsers to take actions once plugins are ready
        """
        self.info('Connecting all players...')
        plist = self.getPlayerList()
        for cid, p in plist.iteritems():
            client = self.clients.getByCID(cid)
            if not client:
                name = p['name']
                if 'clanTag' in p and len(p['clanTag']) > 0:
                    name = '[' + p['clanTag'] + '] ' + p['name']
                self.debug('Client %s found on the server' % cid)
                client = self.clients.newClient(cid, guid=p['guid'], name=name, team=p['teamId'], data=p)
                self.queueEvent(self.getEvent('EVT_CLIENT_JOIN', p, client))

    def checkVersion(self):
        version = self.output.write('version')
        self.info('server version: %s' % version)
        if version[0] != 'MOH':
            raise Exception('the moh parser can only work with Medal of Honor')

    def getClient(self, cid, _guid=None):
        """
        Get a connected client from storage or create it
        B3 CID   <--> MoH character name
        B3 GUID  <--> MoH EA_guid
        """
        client = self.clients.getByCID(cid)
        if not client:
            if cid == 'Server':
                return self.clients.newClient('Server', guid='Server', name='Server', hide=True, pbid='Server', team=b3.TEAM_UNKNOWN)
            words = self.write(('admin.listPlayers', 'player', cid))
            pib = PlayerInfoBlock(words)
            if len(pib) == 0:
                self.debug('No such client found')
                return
            p = pib[0]
            cid = p['name']
            name = p['name']
            if p['guid']:
                guid = p['guid']
            elif _guid:
                guid = _guid
            else:
                self.debug('No guid for %s: waiting for next event' % name)
                return
            if 'clanTag' in p and len(p['clanTag']) > 0:
                name = '[' + p['clanTag'] + '] ' + p['name']
            client = self.clients.newClient(cid, guid=guid, name=name, team=self.getTeam(p['teamId']), teamId=int(p['teamId']), data=p)
            self.queueEvent(self.getEvent('EVT_CLIENT_JOIN', p, client))
        return client

    def getHardName(self, mapname):
        """
        Change real name to level name.
        """
        mapname = mapname.lower()
        if mapname.startswith('mazar-i-sharif airfield'):
            return 'levels/mp_01'
        else:
            if mapname.startswith('bagram hanger'):
                return 'levels/mp_01_elimination'
            if mapname.startswith('shah-i-knot mountains'):
                return 'levels/mp_02'
            if mapname.startswith('hindu kush pass'):
                return 'levels/mp_02_koth'
            if mapname.startswith('khyber caves'):
                return 'levels/mp_03'
            if mapname.startswith('helmand valley'):
                return 'levels/mp_04'
            if mapname.startswith('helmand river hill'):
                return 'levels/mp_04_koth'
            if mapname.startswith('kandahar marketplace'):
                return 'levels/mp_05'
            if mapname.startswith('diwagal camp'):
                return 'levels/mp_06'
            if mapname.startswith('korengal outpost'):
                return 'levels/mp_07_koth'
            if mapname.startswith('kunar base'):
                return 'levels/mp_08'
            if mapname.startswith('kabul city ruins'):
                return 'levels/mp_09'
            if mapname.startswith('garmzir town'):
                return 'levels/mp_10'
            self.warning("unknown level name : '%s' : please make sure you have entered a valid mapname" % mapname)
            return mapname

    def getEasyName(self, mapname):
        """
        Change levelname to real name.
        """
        if mapname.startswith('levels/mp_01_elimination'):
            return 'Bagram Hanger'
        else:
            if mapname.startswith('levels/mp_01'):
                return 'Mazar-i-Sharif Airfield'
            if mapname.startswith('levels/mp_02_koth'):
                return 'Hindu Kush Pass'
            if mapname.startswith('levels/mp_02'):
                return 'Shah-i-Knot Mountains'
            if mapname.startswith('levels/mp_03'):
                return 'Khyber Caves'
            if mapname.startswith('levels/mp_04_koth'):
                return 'Helmand River Hill'
            if mapname.startswith('levels/mp_04'):
                return 'Helmand Valley'
            if mapname.startswith('levels/mp_05'):
                return 'Kandahar Marketplace'
            if mapname.startswith('levels/mp_06'):
                return 'Diwagal Camp'
            if mapname.startswith('levels/mp_07_koth'):
                return 'Korengal Outpost'
            if mapname.startswith('levels/mp_08'):
                return 'Kunar Base'
            if mapname.startswith('levels/mp_09'):
                return 'Kabul City Ruins'
            if mapname.startswith('levels/mp_10'):
                return 'Garmzir Town'
            self.warning("unknown level name : '%s' : please report this on B3 forums" % mapname)
            return mapname

    def getServerVars(self):
        """
        Update the game property from server fresh data.
        """
        try:
            self.game.serverName = self.getCvar('serverName').getBoolean()
        except:
            pass

        try:
            self.game.gamePassword = self.getCvar('gamePassword').getBoolean()
        except:
            pass

        try:
            self.game.punkBuster = self.getCvar('punkBuster').getBoolean()
        except:
            pass

        try:
            self.game.hardCore = self.getCvar('hardCore').getBoolean()
        except:
            pass

        try:
            self.game.ranked = self.getCvar('ranked').getBoolean()
        except:
            pass

        try:
            self.game.skillLimit = self.getCvar('skillLimit').getBoolean()
        except:
            pass

        try:
            self.game.noUnlocks = self.getCvar('noUnlocks').getBoolean()
        except:
            pass

        try:
            self.game.noAmmoPickups = self.getCvar('noAmmoPickups').getBoolean()
        except:
            pass

        try:
            self.game.realisticHealth = self.getCvar('realisticHealth').getBoolean()
        except:
            pass

        try:
            self.game.supportAction = self.getCvar('supportAction').getBoolean()
        except:
            pass

        try:
            self.game.preRoundLimit = self.getCvar('preRoundLimit').getBoolean()
        except:
            pass

        try:
            self.game.roundStartTimerPlayersLimit = self.getCvar('roundStartTimerPlayersLimit').getBoolean()
        except:
            pass

        try:
            self.game.roundStartTimerDelay = self.getCvar('roundStartTimerDelay').getBoolean()
        except:
            pass

        try:
            self.game.tdmScoreCounterMaxScore = self.getCvar('tdmScoreCounterMaxScore').getBoolean()
        except:
            pass

        try:
            self.game.clanTeams = self.getCvar('clanTeams').getBoolean()
        except:
            pass

        try:
            self.game.friendlyFire = self.getCvar('friendlyFire').getBoolean()
        except:
            pass

        try:
            self.game.currentPlayerLimit = self.getCvar('currentPlayerLimit').getBoolean()
        except:
            pass

        try:
            self.game.maxPlayerLimit = self.getCvar('maxPlayerLimit').getBoolean()
        except:
            pass

        try:
            self.game.playerLimit = self.getCvar('playerLimit').getBoolean()
        except:
            pass

        try:
            self.game.bannerUrl = self.getCvar('bannerUrl').getBoolean()
        except:
            pass

        try:
            self.game.serverDescription = self.getCvar('serverDescription').getBoolean()
        except:
            pass

        try:
            self.game.noCrosshair = self.getCvar('noCrosshair').getBoolean()
        except:
            pass

        try:
            self.game.noSpotting = self.getCvar('noSpotting').getBoolean()
        except:
            pass

        try:
            self.game.teamKillCountForKick = self.getCvar('teamKillCountForKick').getBoolean()
        except:
            pass

        try:
            self.game.teamKillValueForKick = self.getCvar('teamKillValueForKick').getBoolean()
        except:
            pass

        try:
            self.game.teamKillValueIncrease = self.getCvar('teamKillValueIncrease').getBoolean()
        except:
            pass

        try:
            self.game.teamKillValueDecreasePerSecond = self.getCvar('teamKillValueDecreasePerSecond').getBoolean()
        except:
            pass

        try:
            self.game.idleTimeout = self.getCvar('idleTimeout').getBoolean()
        except:
            pass

    def getTeam(self, team):
        """
        Convert MOH team numbers to B3 team numbers.
        """
        team = int(team)
        if team == 1:
            return b3.TEAM_RED
        else:
            if team == 2:
                return b3.TEAM_BLUE
            if team == 3:
                return b3.TEAM_SPEC
            return b3.TEAM_UNKNOWN

    def OnPlayerSpawn(self, action, data):
        """
        player.onSpawn <soldier name: string> <kit: string> <weapon: string> <specializations: 3 x string>
        """
        if len(data) < 2:
            return None
        else:
            spawner = self.getClient(data[0])
            kit = data[1]
            weapon = data[2]
            spec1 = data[3]
            spec2 = data[4]
            spec3 = data[5]
            return self.getEvent('EVT_CLIENT_SPAWN', (kit, weapon, spec1, spec2, spec3), spawner)

    def OnPlayerTeamchange(self, action, data):
        """
        player.onTeamChange <soldier name: player name> <team: Team ID>
        Effect: Player might have changed team
        """
        client = self.getClient(data[0])
        if client:
            client.team = self.getTeam(data[1])
            client.teamId = int(data[1])

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
        if isinstance(client, str):
            self.write(self.getCommand('kick', cid=client, reason=reason[:80]))
            return
        if admin:
            banduration = b3.functions.minutesStr(duration)
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin, banduration=banduration)
            fullreason = self.getMessage('temp_banned_by', variables)
        else:
            banduration = b3.functions.minutesStr(duration)
            variables = self.getMessageVariables(client=client, reason=reason, banduration=banduration)
            fullreason = self.getMessage('temp_banned', variables)
        fullreason = self.stripColors(fullreason)
        reason = self.stripColors(reason)
        if self.PunkBuster:
            if duration > 1440:
                duration = 1440
            self.PunkBuster.kick(client, duration, reason)
        self.write(('banList.list', ))
        self.write(self.getCommand('tempban', guid=client.guid, duration=duration * 60, reason=reason[:80]))
        self.write(('banList.list', ))
        self.write(self.getCommand('kick', cid=client.cid, reason=reason[:80]))
        if not silent and fullreason != '':
            self.say(fullreason)
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN_TEMP', {'reason': reason, 'duration': duration, 
           'admin': admin}, client))

    def ban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Ban a given client.
        :param client: The client to ban
        :param reason: The reason for this ban
        :param admin: The admin who performed the ban
        :param silent: Whether or not to announce this ban
        """
        self.debug('BAN : client: %s, reason: %s', client, reason)
        if isinstance(client, b3.clients.Client):
            self.write(self.getCommand('ban', guid=client.guid, reason=reason[:80]))
            try:
                self.write(self.getCommand('kick', cid=client.cid, reason=reason[:80]))
            except:
                pass

            return
        if admin:
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
            reason = self.getMessage('banned_by', variables)
        else:
            variables = self.getMessageVariables(client=client, reason=reason)
            reason = self.getMessage('banned', variables)
        reason = self.stripColors(reason)
        if client.cid is None:
            self.debug('EFFECTIVE BAN : %s', self.getCommand('banByIp', ip=client.ip, reason=reason[:80]))
            self.write(self.getCommand('banByIp', ip=client.ip, reason=reason[:80]))
            if admin:
                admin.message('Banned: %s (@%s). His last ip (%s) has been added to banlist' % (
                 client.exactName, client.id, client.ip))
        else:
            self.debug('EFFECTIVE BAN : %s', self.getCommand('ban', guid=client.guid, reason=reason[:80]))
            self.write(('banList.list', ))
            self.write(self.getCommand('ban', cid=client.cid, reason=reason[:80]))
            self.write(('banList.list', ))
            self.write(self.getCommand('kick', cid=client.cid, reason=reason[:80]))
            if admin:
                admin.message('Banned: %s (@%s) has been added to banlist' % (client.exactName, client.id))
        if self.PunkBuster:
            self.PunkBuster.banGUID(client, reason)
        if not silent:
            self.say(reason)
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN', {'reason': reason, 'admin': admin}, client))
        return

    def rotateMap(self):
        """
        Load the next map (not level). If the current game mod plays each level twice
        to get teams the chance to play both sides, then this rotate a second
        time to really switch to the next map.
        """
        nextIndex = self.getNextMapIndex()
        if nextIndex == -1:
            self.write(('admin.runNextRound', ))
        else:
            self.write(('mapList.nextLevelIndex', nextIndex))
            self.write(('admin.runNextRound', ))

    def changeMap(self, mapname):
        """
        Change to the given map
        
        1) determine the level name
            If map is of the form 'mp_001' and 'Kaboul' is a supported
            level for the current game mod, then this level is loaded.
            
            In other cases, this method assumes it is given a 'easy map name' (like
            'Port Valdez') and it will do its best to find the level name that seems
            to be for 'Port Valdez' within the supported levels.
        
            If no match is found, then instead of loading the map, this method 
            returns a list of candidate map names
            
        2) if we got a level name
            if the level is not in the current rotation list, then add it to 
            the map list and load it
        """
        supportedMaps = self.getSupportedMaps()
        if 'levels/%s' % mapname in supportedMaps:
            mapname = 'levels/%s' % mapname
        if mapname not in supportedMaps:
            match = self.getMapsSoundingLike(mapname)
            if len(match) == 1:
                mapname = match[0]
            else:
                return match
        if mapname in supportedMaps:
            levelnames = self.write(('mapList.list', ))
            if mapname not in levelnames:
                nextIndex = self.getNextMapIndex()
                if nextIndex == -1:
                    self.write(('mapList.append', mapname))
                    nextIndex = 0
                else:
                    if nextIndex == 0:
                        nextIndex = 1
                    self.write(('mapList.insert', nextIndex, mapname))
            else:
                nextIndex = 0
                while nextIndex < len(levelnames) and levelnames[nextIndex] != mapname:
                    nextIndex += 1

            self.say('Changing map to %s' % mapname)
            time.sleep(1)
            self.write(('mapList.nextLevelIndex', nextIndex))
            self.write(('admin.runNextRound', ))

    def saybig(self, msg):
        """
        Broadcast a message to all players.
        :param msg: The message to be broadcasted
        """
        self.say(msg)
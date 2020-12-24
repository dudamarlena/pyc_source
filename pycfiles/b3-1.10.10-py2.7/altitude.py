# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\altitude.py
# Compiled at: 2016-03-08 18:42:09
import b3, b3.clients, b3.functions, re, json, time
from b3.events import Event
from b3.parser import Parser
__author__ = 'Courgette'
__version__ = '1.6'

class AltitudeParser(Parser):
    """
    B3 parser for the Altitude game. See http://altitudegame.com.
    """
    gameName = 'altitude'
    _lineTime = re.compile('^{"port":[0-9]+, "time":(?P<seconds>[0-9]+),.*')
    _eventMap = {}
    _last_ping_report = {}
    _last_endround_report = {}

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self._initialize_rcon()
        self.clients.newClient(-1, name='WORLD', hide=True)
        self._eventMap['serverStart'] = self.getEventID('EVT_CUSTOM')
        self._eventMap['mapLoading'] = self.getEventID('EVT_CUSTOM')
        self.Events.createEvent('EVT_CLIENT_CONSOLE_COMMAND', 'Client exec a console command')
        self.Events.createEvent('EVT_CLIENT_CALL_VOTE', 'Client call vote')
        self.Events.createEvent('EVT_CLIENT_VOTE', 'Client vote')
        self.registerHandler('EVT_CLIENT_CALL_VOTE', self._OnClientCallVote)

    def _initialize_rcon(self):
        """
        We need a way to send rcon commands to the gale server.
        In Altitude, this is done by writing commands to be run on a new line
        of the command.txt file
        """
        if not self.config.has_option('server', 'command_file'):
            self.critical('the B3 config file for Altitude must provide the location of the command file')
            self.die()
        commandfile_name = self.config.getpath('server', 'command_file')
        self.output = AltitudeRcon(console=self, commandfile=commandfile_name)

    def parseLine(self, line):
        """
        Method call for each line of the game log file that must return a B3 event
        """
        altitude_event = json.loads(line)
        if altitude_event['port'] != self._port:
            return
        else:
            event_type = altitude_event['type']
            method_name = 'OnAltitude%s%s' % (event_type[:1].upper(), event_type[1:])
            event = None
            if not hasattr(self, method_name):
                if event_type in self._eventMap:
                    event = b3.events.Event(self._eventMap[event_type], data=altitude_event)
                else:
                    self.verbose2('create method %s to handle event %r', method_name, altitude_event)
                    event = self.getEvent('EVT_UNKNOWN', data=altitude_event)
            else:
                func = getattr(self, method_name)
                event = func(altitude_event)
            if event:
                self.verbose2('event fired : %s', event)
                self.queueEvent(event)
            return

    def OnAltitudeServerInit(self, altitude_event):
        """
        Handle log lines of type serverInit
        Example :
        {'maxPlayerCount': 14, 
        'type': 'serverInit', 'port': 27276, 
        'name': u'Courgette test Server', 'time': 493}
        """
        self.game.sv_hostname = altitude_event['name']
        self.game.sv_maxclients = int(altitude_event['maxPlayerCount'])

    def OnAltitudeClientAdd(self, altitude_event):
        """
        Handle log lines of type clientAdd
        Example :
        {"port":27276,"demo":false,"time":12108767,"level":9,"player":2,"nickname":"Courgette","aceRank":0,
        "vaporId":"a8654321-123a-414e-c71a-123123123131","type":"clientAdd","ip":"192.168.10.1:27272"}
        """
        vaporId = altitude_event['vaporId']
        if vaporId == '00000000-0000-0000-0000-000000000000':
            vaporId = None
        client = self.newClient(altitude_event['player'], guid=vaporId, name=altitude_event['nickname'], team=b3.TEAM_UNKNOWN, ip=altitude_event['ip'].split(':')[0])
        client.data = {'level': altitude_event['level'], 
           'aceRank': altitude_event['aceRank']}
        return

    def OnAltitudeClientRemove(self, altitude_event):
        """
        Handle log lines of type clientRemove
        Example :
            {"port":27276, "message":"left", "time":17317434, 
            "player":2, "reason":"Client left.", 
            "nickname":"Courgette", "vaporId":"d6545616-17a3-4044-a74b-121231321321",
            "type":"clientRemove", "ip":"192.168.10.1:27272"}
            
            {"port":27276, "message":"banned for 2 minutes", "time":3300620,
            "player":2, "reason":"Kicked by vote.", "nickname":"Courgette",
            "vaporId":"d6545616-17a3-4044-a74b-121231321321", "type":"clientRemove",
            "ip":"192.168.10.1:27272"}
        """
        c = self.clients.getByGUID(altitude_event['vaporId'])
        if c:
            if altitude_event['reason'] == 'Client left.':
                pass
            elif altitude_event['reason'] == 'Kicked by vote.':
                if c.maxLevel > 2:
                    self.write('removeBan %(vaporId)s' % {'vaporId': c.guid})
            else:
                self.verbose2('unknown clientRemove reason : %s', altitude_event['reason'])
            c.disconnect()

    def OnAltitudeChat(self, altitude_event):
        """
        Handle log lines of type clientRemove
        Example :
        {"port":27276,"message":"test","time":326172,"player":2,"server":false,"type":"chat"}

        Unfortunately, there is no distinction between a normal chat and team chat
        {"port":27276,"message":"test team chat","time":1167491,"player":3,"server":false,"type":"chat"}
        """
        c = self.clients.getByCID(altitude_event['player'])
        if c:
            if altitude_event['server'] is False:
                return self.getEvent('EVT_CLIENT_SAY', data=altitude_event['message'], client=c)
            else:
                return self.getEvent('EVT_CUSTOM', data=altitude_event, client=c)

    def OnAltitudeKill(self, altitude_event):
        """
        Handle log lines of type kill
        Example :
        {u'streak': 0, u'multi': 0, u'player': -1, u'source': u'plane', u'victim': 0, u'time': 3571497, u'xp': 10,
        u'type': u'kill', u'port': 27276}
        """
        attacker = self.clients.getByCID(altitude_event['player'])
        if not attacker:
            self.debug('No attacker')
            return
        else:
            if 'xp' in altitude_event:
                attacker.currentXP = int(altitude_event['xp'])
            if 'currentStreak' in altitude_event:
                attacker.currentStreak = altitude_event['currentStreak']
            victim = self.clients.getByCID(altitude_event['victim'])
            if not victim:
                self.debug('No victim')
                return
            weapon = altitude_event['source']
            if not weapon:
                self.debug('No weapon')
                return
            event = 'EVT_CLIENT_KILL'
            if attacker == victim:
                event = 'EVT_CLIENT_SUICIDE'
            return self.getEvent(event, (100, weapon, None), attacker, victim)

    def OnAltitudeAssist(self, altitude_event):
        """
        Handle log lines of type assist
        example :
        {u'player': 2, u'victim': 1, u'time': 10836645, u'xp': 8, u'type': u'assist', u'port': 27276}
        """
        attacker = self.clients.getByCID(altitude_event['player'])
        if not attacker:
            self.debug('No attacker')
            return
        if 'xp' in altitude_event:
            attacker.currentXP = int(altitude_event['xp'])
        victim = self.clients.getByCID(altitude_event['victim'])
        if not victim:
            self.debug('No victim')
            return
        return self.getEvent('EVT_CLIENT_ACTION', data='assist', client=attacker, target=victim)

    def OnAltitudeTeamChange(self, altitude_event):
        """
        Handle log lines of type teamChange
        Example :
        {"port":27276,"time":4768143,"player":2,"team":2,"type":"teamChange"}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if client:
            client.team = self.getTeam(altitude_event['team'])

    def OnAltitudeSpawn(self, altitude_event):
        """
        Handle log lines of type spawn
        Example :
        {u'perkBlue': u'Reverse Thrust', u'team': 8, u'perkGreen': u'Heavy Armor', u'player': 1, u'plane': u'Biplane',
        u'perkRed': u'Heavy Cannon', u'time': 4454401, u'skin': u'No Skin', u'type': u'spawn', u'port': 27276}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if not client:
            client = self.newClient(altitude_event['player'])
        if client:
            client.data = {'perkBlue': altitude_event['perkBlue'], 'perkGreen': altitude_event['perkGreen'], 
               'perkRed': altitude_event['perkRed'], 
               'plane': altitude_event['plane'], 
               'skin': altitude_event['skin']}
            client.team = self.getTeam(altitude_event['team'])
            return self.getEvent('EVT_CLIENT_JOIN', data=altitude_event, client=client)

    def OnAltitudeRoundEnd(self, altitude_event):
        """
        Handle log lines of type roundEnd
        Example :
        {"port":27276,"time":4833834,"participantStatsByName":{"Crashes":[2,4,0,0,0],"Goals Scored":[0,0,0,0,0],
        "Kills":[22,12,2,0,31],"Damage Received":[1680,4090,100,2570,1540],"Assists":[8,0,1,1,4],"Multikill":[2,0,0,0,2],
        "Ball Possession Time":[0,0,0,0,0],"Experience":[267,190,24,12,346],"Longest Life":[207,46,61,41,307],
        "Goals Assisted":[0,0,0,0,0],"Damage Dealt to Enemy Buildings":[0,0,0,0,0],"Deaths":[8,35,0,24,6],
        "Damage Dealt":[1950,1170,80,250,2540],"Kill Streak":[14,3,2,0,21]},"winnerByAward":{"Best Multikill":0,
        "Longest Life":10,"Best Kill Streak":10,"Most Deadly":10,"Most Helpful":0},"type":"roundEnd",
        "participants":[0,1,2,7,10]}
        """
        self._last_endround_report = {'time': altitude_event['time'], 
           'participantStatsByName': altitude_event['participantStatsByName'], 
           'winnerByAward': altitude_event['participantStatsByName'], 
           'participants': altitude_event['participants']}
        stats = altitude_event['participantStatsByName']
        for i in range(len(altitude_event['participants'])):
            cid = altitude_event['participants'][i]
            client = self.clients.getByCID(cid)
            if not client:
                continue
            client.lastStats = {}
            for statname in stats:
                client.lastStats[statname] = stats[statname][i]

            client.kills = client.lastStats['Kills']

        return self.getEvent('EVT_GAME_ROUND_END', data=altitude_event)

    def OnAltitudeMapChange(self, altitude_event):
        """
        Handle log lines of type mapChange
        Example :
        {"port":27276,"time":4847790,"map":"ball_grotto","type":"mapChange","mode":"ball"}
        """
        self.game.mapName = altitude_event['map']
        self.game.mapType = altitude_event['mode']
        return self.getEvent('EVT_GAME_WARMUP', data=altitude_event)

    def OnAltitudePowerupPickup(self, altitude_event):
        """
        Handle log lines of type powerupPickup
        Example :
        {"port":27276,"time":4549268,"powerup":"Homing Missile","player":10,"positionX":3572.41,"positionY":639.57,
        "type":"powerupPickup"}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if client:
            client.lastPosition = (
             altitude_event['positionX'], altitude_event['positionY'])
            return self.getEvent('EVT_CLIENT_ITEM_PICKUP', data=altitude_event['powerup'], client=client)

    def OnAltitudePowerupAutoUse(self, altitude_event):
        """
        Handle log lines of type powerupAutoUse
        Example :
        {"port":27276,"time":4551678,"powerup":"Health","player":10,"positionX":2898,"positionY":285,"type":"powerupAutoUse"}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if client:
            client.lastPosition = (
             altitude_event['positionX'], altitude_event['positionY'])
            return self.getEvent('EVT_CLIENT_ITEM_PICKUP', data=altitude_event['powerup'], client=client)

    def OnAltitudePowerupUse(self, altitude_event):
        """
        Handle log lines of type powerupUse
        Example :
        {"port":27276,"velocityX":-8.62,"time":5166541,"powerup":"Homing Missile","player":0,"positionX":2060.43,
        "velocityY":0.75,"positionY":726.69,"type":"powerupUse"}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if client:
            client.lastPosition = (
             altitude_event['positionX'], altitude_event['positionY'])
            return self.getEvent('EVT_CUSTOM', data=altitude_event, client=client)

    def OnAltitudePowerupDefuse(self, altitude_event):
        """
        Handle log lines of type powerupDefuse
        Example :
        {u'positionX': 1416.9, u'powerup': u'Bomb', u'player': 2, u'positionY': 522.83, u'time': 12243874, u'xp': 10,
        u'type': u'powerupDefuse', u'port': 27276}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if client:
            client.lastPosition = (
             altitude_event['positionX'], altitude_event['positionY'])
            if 'xp' in altitude_event:
                client.currentXP = int(altitude_event['xp'])
            return self.getEvent('EVT_CLIENT_ACTION', data='defuse', client=client)

    def OnAltitudeGoal(self, altitude_event):
        """
        Handle log lines of type goal
        Example :
        {"port":27276,"time":4927227,"player":1,"xp":50,"type":"goal","assister":-1}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if client:
            if 'xp' in altitude_event:
                client.currentXP = int(altitude_event['xp'])
            return self.getEvent('EVT_CLIENT_ACTION', data='goal', client=client)

    def OnAltitudeStructureDamage(self, altitude_event):
        """
        Handle log lines of type structureDamage
        example :
        {u'target': u'base', u'player': 3, u'time': 11048551, u'xp': 31, u'type': u'structureDamage', u'port': 27276}
        """
        attacker = self.clients.getByCID(altitude_event['player'])
        if not attacker:
            self.debug('No attacker')
            return
        if 'xp' in altitude_event:
            attacker.currentXP = int(altitude_event['xp'])
        return self.getEvent('EVT_CLIENT_ACTION', data='structureDamage', client=attacker, target=altitude_event['target'])

    def OnAltitudeStructureDestroy(self, altitude_event):
        """
        Handle log lines of type structureDestroy
        Example :
        {u'target': u'turret', u'player': 3, u'time': 13534409, u'xp': 10, u'type': u'structureDestroy', u'port': 27276}
        """
        client = self.clients.getByCID(altitude_event['player'])
        if client:
            if 'xp' in altitude_event:
                client.currentXP = int(altitude_event['xp'])
            return self.getEvent('EVT_CLIENT_ACTION', data='structureDestroy', client=client, target=altitude_event['target'])

    def OnAltitudePingSummary(self, altitude_event):
        """
        Handle log lines of type pingSummary
        example :
        {u'pingByPlayer': {u'10': 138, u'7': 153, u'6': 0}, u'type': u'pingSummary', u'port': 27276, u'time': 4188098}
        """
        self._last_ping_report = altitude_event['pingByPlayer']

    def OnAltitudeConsoleCommandExecute(self, altitude_event):
        """
        Handle log lines of type consoleCommandExecute
        Example :
            {"port":27276, "time":3250286, "arguments":["kick","Courgette"],
            "source":"c0aaf37d-e56d-4431-aa1e-69d5e18be5e6", "command":"vote",
            "group":"Anonymous", "type":"consoleCommandExecute"}
        """
        if altitude_event['source'] == '00000000-0000-0000-0000-000000000000':
            return
        client = self.clients.getByGUID(altitude_event['source'])
        if not client:
            self.debug('client not found for %s' % altitude_event['source'])
            return
        command = altitude_event['command']
        method_name = 'OnAltitudeCommand%s%s' % (command[:1].upper(), command[1:])
        if not hasattr(self, method_name):
            self.verbose2('create method %s to handle command %r', method_name, altitude_event)
            event = self.getEvent('EVT_CLIENT_CONSOLE_COMMAND', data=altitude_event, client=client)
        else:
            func = getattr(self, method_name)
            event = func(altitude_event)
        return event

    def OnAltitudeCommandVote(self, altitude_event):
        """
        Handle vote console commands
        Example :
            {"port":27276, "time":3250286, "arguments":["kick","Courgette"],
            "source":"c0aaf37d-e56d-4431-aa1e-69d5e18be5e6", "command":"vote",
            "group":"Anonymous", "type":"consoleCommandExecute"}
        """
        c = self.clients.getByGUID(altitude_event['vaporId'])
        return self.getEvent('EVT_CLIENT_CALL_VOTE', data=altitude_event, client=c)

    def OnAltitudeCommandCastBallot(self, altitude_event):
        """
        Handle castBallot console commands
        Example :
            {"port":27276,"time":3252183, "arguments":["1"],
            "source":"86e487de-0190-43ff-8e9e-70a14a1751a2",
            "command":"castBallot", "group":"Anonymous",
            "type":"consoleCommandExecute"}
        """
        c = self.clients.getByGUID(altitude_event['source'])
        return self.getEvent('EVT_CLIENT_VOTE', data=altitude_event, client=c)

    def getPlayerList(self):
        """
        Query the game server for connected players.
        return a dict having players' id for keys and players' data as another dict for values
        """
        players = {}
        for cid in self._last_ping_report.keys():
            client = self.clients.getByCID(cid)
            if client:
                players[cid] = client

        return players

    def authorizeClients(self):
        """
        For all connected players, fill the client object with properties allowing to find 
        the user in the database (usualy guid, or punkbuster id, ip) and call the 
        Client.auth() method 
        """
        pass

    def sync(self):
        """
        For all connected players returned by self.getPlayerList(), get the matching Client
        object from self.clients (with self.clients.getByCID(cid) or similar methods) and
        look for inconsistencies. If required call the client.disconnect() method to remove
        a client from self.clients.
        This is mainly useful for games where clients are identified by the slot number they
        occupy. On map change, a player A on slot 1 can leave making room for player B who
        connects on slot 1.
        """
        connected_clients = self.getPlayerList()
        for c in self.clients.getList():
            if c.cid not in connected_clients:
                c.disconnect()

        return connected_clients

    def say(self, msg, *args):
        """
        Broadcast a message to all players.
        :param msg: The message to be broadcasted
        """
        self.write('serverMessage %s' % self.stripColors(msg % args))

    def saybig(self, msg, *args):
        """
        Broadcast a message to all players in a way that will catch their attention.
        :param msg: The message to be broadcasted
        """
        self.say(msg % args)

    def message(self, client, msg, *args):
        """
        Display a message to a given client
        :param client: The client to who send the message
        :param msg: The message to be sent
        """
        self.write('serverWhisper %s %s' % (client.name, self.stripColors(msg % args)))

    def kick(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Kick a given client.
        :param client: The client to kick
        :param reason: The reason for this kick
        :param admin: The admin who performed the kick
        :param silent: Whether or not to announce this kick
        """
        if not isinstance(client, b3.clients.Client):
            return
        if admin:
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
            fullreason = self.getMessage('kicked_by', variables)
        else:
            variables = self.getMessageVariables(client=client, reason=reason)
            fullreason = self.getMessage('kicked', variables)
        fullreason = self.stripColors(fullreason)
        reason = self.stripColors(reason)
        if not silent and fullreason != '':
            self.say(fullreason)
        self.write('kick %s' % client.name)
        self.queueEvent(self.getEvent(self.getEventID('EVT_CLIENT_KICK'), {'reason': reason, 'admin': admin}, client))

    def ban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Ban a given client.
        :param client: The client to ban
        :param reason: The reason for this ban
        :param admin: The admin who performed the ban
        :param silent: Whether or not to announce this ban
        """
        if admin:
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
            fullreason = self.getMessage('banned_by', variables)
        else:
            variables = self.getMessageVariables(client=client, reason=reason)
            fullreason = self.getMessage('banned', variables)
        fullreason = self.stripColors(fullreason)
        reason = self.stripColors(reason)
        if not silent and fullreason != '':
            self.say(fullreason)
        self.write('addBan %(vaporId)s %(duration)s %(timeunit)s %(reason)s' % {'vaporId': client.guid, 
           'duration': 1, 
           'timeunit': 'forever', 
           'reason': reason})
        self.write('kick %s' % client.name)
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN', data={'reason': reason, 'admin': admin}, client=client))

    def unban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Unban a client.
        :param client: The client to unban
        :param reason: The reason for the unban
        :param admin: The admin who unbanned this client
        :param silent: Whether or not to announce this unban
        """
        self.write('removeBan %(vaporId)s' % {'vaporId': client.guid})
        if admin:
            admin.message('Unbanned: removed %s from banlist' % client.name)
        self.queueEvent(self.getEvent('EVT_CLIENT_UNBAN', data=reason, client=client))

    def tempban(self, client, reason='', duration=2, admin=None, silent=False, *kwargs):
        """
        Tempban a client.
        :param client: The client to tempban
        :param reason: The reason for this tempban
        :param duration: The duration of the tempban
        :param admin: The admin who performed the tempban
        :param silent: Whether or not to announce this tempban
        """
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
        if not silent and fullreason != '':
            self.say(fullreason)
        self.write('addBan %(vaporId)s %(duration)s %(timeunit)s %(reason)s' % {'vaporId': client.guid, 
           'duration': int(duration), 
           'timeunit': 'minute', 
           'reason': reason})
        self.write('kick %s' % client.name)
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN_TEMP', data={'reason': reason, 'duration': duration, 
           'admin': admin}, client=client))

    def getNextMap(self):
        pass

    def getMap(self):
        pass

    def getMaps(self):
        pass

    def rotateMap(self):
        pass

    def changeMap(self, mapname):
        """
        Load a given map/level
        Return a list of suggested map names in cases it fails to recognize the map that was provided
        """
        self.write('changeMap %s' % mapname)

    def getPlayerPings(self, filter_client_ids=None):
        """
        Returns a dict having players' id for keys and players' ping for values
        """
        return self._last_ping_report

    def getPlayerScores(self):
        """
        Returns a dict having players' id for keys and players' scores for values
        """
        scores = {}
        for cid, client in self.getPlayerList().items():
            scores[cid] = client.kills

        return scores

    def inflictCustomPenalty(self, penalty_type, client, reason=None, duration=None, admin=None, data=None):
        r"""
        Called if b3.admin.penalizeClient() does not know a given penalty type. 
        Overwrite this to add customized penalties for your game like 'slap', 'nuke', 
        'mute' or anything you want.
        /!\ This method must return True if the penalty was inflicted.
        """
        pass

    def _OnClientCallVote(self, b3event):
        """
        This game allows anyone to call a kick vote agains an admin.
        Here we keep an eye on every kick vote and if we found someone calling
        a kick vote on a player of higher level, then we kick him """
        altitude_event = b3event.data
        kick_target = self.clients.getByName(altitude_event['arguments'][1])
        vote_caller = b3event.client
        if vote_caller and kick_target:
            if kick_target.maxLevel > vote_caller.maxLevel:
                vote_caller.message('Do not call kick vote against admins')
                time.sleep(2)
                vote_caller.tempban(duration='2m', reason='call vote against higher level admin', data=altitude_event)

    def shutdown(self):
        """
        Shutdown B3.
        """
        try:
            try:
                self.output.clear()
            except Exception as e:
                self.error(e)

        finally:
            Parser.shutdown(self)

    def getTeam(self, teamAltitudeId):
        """
        Convert an Altitude team ID into a B3 team ID
        doc: http://altitudegame.com/forums/showpost.php?p=82191&postcount=30
        """
        if teamAltitudeId == 2:
            return b3.TEAM_SPEC
        else:
            if teamAltitudeId == 3:
                return b3.TEAM_FREE
            if teamAltitudeId == 4:
                return b3.TEAM_FREE
            if teamAltitudeId == 5:
                return b3.TEAM_FREE
            if teamAltitudeId == 6:
                return b3.TEAM_FREE
            if teamAltitudeId == 7:
                return b3.TEAM_FREE
            if teamAltitudeId == 8:
                return b3.TEAM_FREE
            if teamAltitudeId == 9:
                return b3.TEAM_FREE
            if teamAltitudeId == 10:
                return b3.TEAM_FREE
            if teamAltitudeId == 11:
                return b3.TEAM_FREE
            return b3.TEAM_UNKNOWN

    def newClient(self, cid, **kwargs):
        """
        Create a new client and initialize some Altitude specific attributes
        """
        client = self.clients.newClient(cid, **kwargs)
        client.data = {}
        client.lastPosition = None
        client.kills = None
        client.currentXP = None
        client.currentStreak = None
        client.lastStats = None
        return client


class AltitudeRcon():
    """
    Object that opens the Altitude command file and allows B3 to write commands in it
    """

    def __init__(self, console, commandfile):
        self.console = console
        self._commandfile_name = commandfile
        self._fh = open(commandfile, 'a')

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def write(self, cmd, *args, **kwargs):
        """
        To send a command to the server, the format to respect is :
        [server port],[command type],[data]
        """
        self.console.verbose('RCON :\t %s' % cmd)
        self._fh.write('%s,console,%s\n' % (self.console._port, cmd))

    def flush(self):
        try:
            self._fh.flush()
        except Exception:
            pass

    def close(self):
        self._fh.close()

    def _get_encoding(self):
        return self._fh.encoding

    encoding = property(_get_encoding)

    def clear(self):
        """
        Delete all content off the command file
        """
        self.close()
        self._fh = open(self._commandfile_name, 'w')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\insurgency.py
# Compiled at: 2016-03-08 18:42:10
import re, time, new
from b3 import TEAM_UNKNOWN
from b3 import TEAM_BLUE
from b3 import TEAM_RED
from b3 import TEAM_SPEC
from b3.clients import Client
from b3.clients import Clients
from b3.cvar import Cvar
from b3.decorators import GameEventRouter
from b3.functions import minutesStr
from b3.functions import prefixText
from b3.functions import time2minutes
from b3.functions import getStuffSoundingLike
from b3.parser import Parser
from b3.parsers.source.rcon import Rcon
__author__ = 'Courgette'
__version__ = '0.17'
Clients.authorizeClients = lambda *args, **kwargs: None
RE_HL_LOG_LINE = '^L [01]\\d/[0-3]\\d/\\d+ - [0-2]\\d:[0-5]\\d:[0-5]\\d:\\s*(?P<data>.*)'
RE_HL_LOG_PROPERTY = re.compile('\\((?P<key>[^\\s\\(\\)]+)(?P<data>| "(?P<value>[^"]*)")\\)')
RE_CVAR = re.compile('^"(?P<cvar>\\S+?)" = "(?P<value>.*?)" \\( def. "(?P<default>.*?)".*$', re.MULTILINE)
ger = GameEventRouter()

def parseProperties(properties):
    """
    Parse HL log properties as described at https://developer.valvesoftware.com/wiki/HL_Log_Standard#Notes
    :param properties: string representing HL log properties
    :return: a dict representing all the property key:value parsed
    """
    rv = {}
    if properties:
        for match in re.finditer(RE_HL_LOG_PROPERTY, properties):
            if match.group('data') == '':
                rv[match.group('key')] = True
            else:
                rv[match.group('key')] = match.group('value')

    return rv


class InsurgencyParser(Parser):
    """
    The Insurgency B3 parser class
    """
    gameName = 'insurgency'
    privateMsg = True
    OutputClass = Rcon
    PunkBuster = None
    sm_plugins = None
    last_killlocation_properties = None
    map_cycles = {}
    map_cycle_no = 0
    _lineTime = re.compile('^L [01]\\d/[0-3]\\d/\\d+ - [0-2]\\d:(?P<minutes>[0-5]\\d):(?P<seconds>[0-5]\\d):\\s*')
    _reColor = re.compile('(\\^[0-9])')
    _line_length = 120
    _line_color_prefix = ''
    _use_color_codes = False

    def __new__(cls, *args, **kwargs):
        return Parser.__new__(cls)

    def patch_b3_admin_plugin(self):
        """
        Monkey patches the admin plugin
        """

        def parse_map_parameters(this, data, client):
            """
            Method that parses a command parameters to extract map and gamemode.
            Expecting one or two parameters separated by a space.
            <map> <gamemode>
            """
            parts = data.split()
            if len(parts) < 2:
                gamemode_data = ''
            else:
                gamemode_data = parts[1]
            map_data = parts[0]
            return (
             map_data, gamemode_data)

        def new_cmd_map(this, data, client, cmd=None):
            """
            <map> <gamemode> - switch current map. Specify a gamemode by separating
            them from the map name with a space
            """
            if not data:
                allavailablemaps = this.console.getAllAvailableMaps()
                maplist = ''
                for m in allavailablemaps:
                    maplist = maplist + ', ' + m

                client.message('Full list of maps on the server' + maplist)
                client.message('PVP Gametypes are: ambush, firefight, flashpoint, infiltrate, occupy, push, skirmish, strike')
                client.message('Coop Gametypes are: checkpoint, outpost, hunt, survival')
                client.message('For more help, type !help map')
                return
            parsed_data = this.parse_map_parameters(data, client)
            map_id, gamemode_id = parsed_data
            suggestions = this.console.changeMap(map_id, gamemode_id)
            if type(suggestions) == list:
                client.message('do you mean : %s ?' % (', ').join(suggestions))

        adminPlugin = self.getPlugin('admin')
        adminPlugin.parse_map_parameters = new.instancemethod(parse_map_parameters, adminPlugin)
        command = adminPlugin._commands['map']
        command.func = new.instancemethod(new_cmd_map, adminPlugin)
        command.help = new_cmd_map.__doc__.strip()
        return

    def startup(self):
        """
        Called after the parser is created before run().
        """
        self.bot("TIP: In order to have a consistent name for the game log file, you need to start the game server with '-condebug' as a command line parameter. The game server log file can then be found in the insurgency folder under the name 'console.log'.")
        self.bot('TIP: Make sure to avoid conflicts with in-game commands between B3 and SourceMod by choosing different command prefixes. See PublicChatTrigger and SilentChatTrigger in addons/sourcemod/configs/core.cfg')
        self.bot('TIP: If you have the SourceMod plugin `B3 Say` installed then the messages sent by B3 will better displayed on screen. http://forum.bigbrotherbot.net/counter-strike-global-offensive/sourcemod-plugins-for-b3/')
        if not self.is_sourcemod_installed():
            self.critical('You need to have SourceMod installed on your game server')
            raise SystemExit(220)
        self.createEvent('EVT_SUPERLOGS_WEAPONSTATS', 'SourceMod SuperLogs weaponstats')
        self.createEvent('EVT_SUPERLOGS_WEAPONSTATS2', 'SourceMod SuperLogs weaponstats2')
        self.createEvent('EVT_SERVER_REQUIRES_RESTART', 'Source server requires restart')
        self.clients.newClient('Server', guid='Server', name='Server', hide=True, pbid='Server', team=TEAM_UNKNOWN)
        self.game.cvar = {}
        self.queryServerInfo()
        self.game.mapName = self.getMap()
        if self.game.mapName == None:
            self.game.mapName = ''
        self.verbose2('Current map name is %s' % self.game.mapName)
        self.sm_plugins = self.get_loaded_sm_plugins()
        self.last_killlocation_properties = None
        return

    def pluginsStarted(self):
        """
        Called once all plugins were started.
        Handy if some of them must be monkey-patched.
        """
        self.patch_b3_admin_plugin()
        self.info('Admin plugin patched')

    @ger.gameEvent('^//', '^server cvars start', '^server cvars end', '^\\[basechat\\.smx\\] .*', '^\\[META\\] Loaded \\d+ plugins \\(\\d+ already loaded\\)$', '^\\[META\\] Loaded \\d+ plugin.$', '^Log file started.*$', '^Log file closed.*$', '^\\s*path_goal .*', '^Vote succeeded.*', '^".+" STEAM USERID validated$', '^Dropped .+ from server (Disconnected\\.)$')
    def ignored_line(self):
        print 'ignored'

    @ger.gameEvent('^"(?P<a_name>.+)<(?P<a_cid>\\d+)><(?P<a_guid>.+)><(?P<a_team>.*)>" killed "(?P<v_name>.+)<(?P<v_cid>\\d+)><(?P<v_guid>.+)><(?P<v_team>.*)>" with "(?P<weapon>\\S*)"(?P<properties>.*)$', '^"(?P<a_name>.+)<(?P<a_cid>\\d+)><(?P<a_guid>.+)><(?P<a_team>.*)>" \\[-?\\d+ -?\\d+ -?\\d+\\] killed "(?P<v_name>.+)<(?P<v_cid>\\d+)><(?P<v_guid>.+)><(?P<v_team>.*)>" \\[-?\\d+ -?\\d+ -?\\d+\\] with "(?P<weapon>\\S*)"(?P<properties>.*)$')
    def on_kill(self, a_name, a_cid, a_guid, a_team, v_name, v_cid, v_guid, v_team, weapon, properties):
        attacker = self.getClientOrCreate(a_cid, a_guid, a_name, a_team)
        victim = self.getClientOrCreate(v_cid, v_guid, v_name, v_team)
        props = parseProperties(properties)
        headshot = props.get('headshot', False)
        eventkey = 'EVT_CLIENT_KILL'
        if attacker.cid == victim.cid:
            eventkey = 'EVT_CLIENT_SUICIDE'
        elif attacker.team in (TEAM_BLUE, TEAM_RED) and attacker.team == victim.team:
            eventkey = 'EVT_CLIENT_KILL_TEAM'
        damage_pct = 100
        damage_type = None
        hit_location = 'head' if headshot else 'body'
        data = [damage_pct, weapon, hit_location, damage_type]
        if self.last_killlocation_properties:
            data.append(parseProperties(self.last_killlocation_properties))
            self.last_killlocation_properties = None
        return self.getEvent(eventkey, client=attacker, target=victim, data=tuple(data))

    @ger.gameEvent('^"(?P<a_name>.+)<(?P<a_cid>\\d+)><(?P<a_guid>.+)><(?P<a_team>.*)>" assisted killing "(?P<v_name>.+)<(?P<v_cid>\\d+)><(?P<v_guid>.+)><(?P<v_team>.*)>"(?P<properties>.*)$')
    def on_assisted_killing(self, a_name, a_cid, a_guid, a_team, v_name, v_cid, v_guid, v_team, properties):
        attacker = self.getClientOrCreate(a_cid, a_guid, a_name, a_team)
        victim = self.getClientOrCreate(v_cid, v_guid, v_name, v_team)
        return self.getEvent('EVT_CLIENT_ACTION', client=attacker, target=victim, data='assisted killing')

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>"(?: \\[-?\\d+ -?\\d+ -?\\d+\\])? committed suicide with "(?P<weapon>\\S*)"$')
    def on_suicide(self, name, cid, guid, team, weapon):
        client = self.getClientOrCreate(cid, guid, name, team)
        damage_pct = 100
        damage_type = None
        return self.getEvent('EVT_CLIENT_SUICIDE', client=client, target=client, data=(damage_pct, weapon, 'body',
         damage_type))

    @ger.gameEvent('^"(?P<cvar_name>\\S+)" = "(?P<cvar_value>.*)"$', '^server_cvar: "(?P<cvar_name>\\S+)" "(?P<cvar_value>.*)"$')
    def on_cvar(self, cvar_name, cvar_value):
        self.game.cvar[cvar_name] = cvar_value

    @ger.gameEvent('^-------- Mapchange to (?P<new_map>\\S+) --------$')
    def on_map_change(self, new_map):
        self.game.mapName = new_map

    @ger.gameEvent('^Loading map "(?P<new_map>\\S+)"$')
    def on_started_map(self, new_map):
        self.game.mapName = new_map

    @ger.gameEvent('^Started map "(?P<new_map>\\S+)" \\(CRC "-?\\d+"\\)$')
    def on_started_map(self, new_map):
        self.game.mapName = new_map
        self.game.startMap()

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>\\S*)><(?P<team>\\S*)>" STEAM USERID validated$')
    def on_userid_validated(self, name, cid, guid, team):
        self.getClientOrCreate(cid, guid, name, team)

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>" connected, address "(?P<ip>.+)"$')
    def on_client_connected(self, name, cid, guid, team, ip):
        client = self.getClientOrCreate(cid, guid, name, team)
        if ip != 'none' and client.ip != ip:
            client.ip = ip
            client.save()

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>" disconnected \\(reason "(?P<reason>.*)"\\)$')
    def on_client_disconnected(self, name, cid, guid, team, reason):
        client = self.getClient(cid, guid)
        event = None
        if client:
            if reason == 'Kicked by Console':
                event = self.getEvent('EVT_CLIENT_KICK', client=client, data={'reason': reason, 'admin': None})
            client.disconnect()
        if event:
            return event
        else:
            return

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>" entered the game$')
    def on_client_entered(self, name, cid, guid, team):
        client = self.getClientOrCreate(cid, guid, name, team)
        return self.getEvent('EVT_CLIENT_JOIN', client=client)

    @ger.gameEvent('^"(?P<old_name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>" changed name to "(?P<new_name>.+)"$')
    def on_client_changed_name(self, old_name, cid, guid, team, new_name):
        client = self.getClientOrCreate(cid, guid, old_name, team)
        client.name = new_name

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<old_team>\\S+)>" joined team "(?P<new_team>\\S+)"$', '^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)>" switched from team <(?P<old_team>\\S+)> to <(?P<new_team>\\S+)>$')
    def on_client_join_team(self, name, cid, guid, old_team, new_team):
        if new_team == 'Unassigned':
            client = self.getClient(cid, guid)
        else:
            client = self.getClientOrCreate(cid, guid, name, old_team)
        if client:
            client.team = self.getTeam(new_team)

    @ger.gameEvent("^Gamerules: entering state '(?P<gamerule_state>.+)'")
    def on_gamerule_state(self, gamerule_state):
        if gamerule_state == 'GR_STATE_PREGAME':
            return self.getEvent('EVT_GAME_WARMUP')
        if gamerule_state == 'GR_STATE_STARTGAME':
            self.game.startRound()
            self.sync()
            clients = self.getPlayerList()
            for cid in clients:
                client = self.clients.getByCID(cid)
                return self.getEvent('EVT_CLIENT_JOIN', client=client)

        else:
            if gamerule_state == 'GR_STATE_RND_RUNNING':
                self.game.startRound()
                return self.getEvent('EVT_GAME_ROUND_START', data=self.game)
            if gamerule_state == 'GR_STATE_POSTROUND':
                return self.getEvent('EVT_GAME_ROUND_END')
            if gamerule_state == 'GR_STATE_GAME_OVER':
                self.game.mapEnd()
                return self.getEvent('EVT_GAME_EXIT')
            if gamerule_state in 'GR_STATE_PREROUND':
                pass
            else:
                self.warning("unexpected GameRule state : '%s' : please report this on the B3 forums" % gamerule_state)

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>" triggered "(?P<event_name>\\S+)"(?P<properties>.*)$')
    def on_player_action(self, name, cid, guid, team, event_name, properties):
        client = self.getClientOrCreate(cid, guid, name, team)
        props = parseProperties(properties)
        if event_name in ('Got_The_Bomb', 'Dropped_The_Bomb', 'Planted_The_Bomb', 'Begin_Bomb_Defuse_Without_Kit',
                          'Begin_Bomb_Defuse_With_Kit', 'Defused_The_Bomb', 'headshot',
                          'round_mvp', 'obj_captured', 'obj_destroyed'):
            return self.getEvent('EVT_CLIENT_ACTION', client=client, data=event_name)
        if event_name == 'clantag':
            client.clantag = props.get('value', '')
        else:
            if event_name == 'weaponstats':
                return self.getEvent('EVT_SUPERLOGS_WEAPONSTATS', client=client, data=props)
            if event_name == 'weaponstats2':
                return self.getEvent('EVT_SUPERLOGS_WEAPONSTATS2', client=client, data=props)
            self.warning("unknown client event : '%s' : please report this on the B3 forums" % event_name)

    @ger.gameEvent('^Team "(?P<team>\\S+)" triggered "(?P<event_name>[^"]+)"(?P<properties>.*)$')
    def on_team_action(self, team, event_name, properties):
        if event_name in ('SFUI_Notice_Target_Saved', 'SFUI_Notice_Target_Bombed',
                          'SFUI_Notice_Terrorists_Win', 'SFUI_Notice_CTs_Win', 'SFUI_Notice_Bomb_Defused',
                          'obj_captured', 'obj_destroyed', 'Round_Win'):
            return self.getEvent('EVT_GAME_ROUND_END', data={'team': self.getTeam(team), 'event_name': event_name, 
               'properties': properties})
        self.warning("unexpected team event : '%s' : please report this on the B3 forums" % event_name)

    @ger.gameEvent('^Team "(?P<team>\\S+)" scored "(?P<points>\\d+)" with "(?P<num_players>\\d+)" players$')
    def on_team_score(self, team, points, num_players):
        pass

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*?)>" say "(?P<text>.*)"$')
    def on_client_say(self, name, cid, guid, team, text):
        if guid == 'Console':
            pass
        else:
            client = self.getClientOrCreate(cid, guid, name, team)
            return self.getEvent('EVT_CLIENT_SAY', client=client, data=text)

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*?)>" say_team "(?P<text>.*)"$')
    def on_client_teamsay(self, name, cid, guid, team, text):
        client = self.getClientOrCreate(cid, guid, name, team)
        return self.getEvent('EVT_CLIENT_TEAM_SAY', client=client, data=text)

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>\\S+)>" purchased "(?P<item>\\S+)"$')
    def on_player_purchased(self, name, cid, guid, team, item):
        client = self.getClientOrCreate(cid, guid, name, team)
        return self.getEvent('EVT_CLIENT_ACTION', client=client, data='purchased "%s"' % item)

    @ger.gameEvent('^"(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>\\S+)>" threw (?P<item>.+?)( \\[-?\\d+ -?\\d+ -?\\d+\\])?$')
    def on_player_threw(self, name, cid, guid, team, item):
        client = self.getClientOrCreate(cid, guid, name, team)
        return self.getEvent('EVT_CLIENT_ACTION', client=client, data='threw "%s"' % item)

    @ger.gameEvent('^rcon from "(?P<ip>.+):(?P<port>\\d+)":\\sBad Password$')
    def on_bad_rcon_password(self, ip, port):
        self.error('Bad RCON password, check your b3.xml file')

    @ger.gameEvent('^Molotov projectile spawned at (?P<coord>-?[\\d.]+ -?[\\d.]+ -?[\\d.]+), velocity (?P<velocity>-?[\\d.]+ -?[\\d.]+ -?[\\d.]+)$')
    def on_molotov_spawed(self, coord, velocity):
        pass

    @ger.gameEvent('^rcon from "(?P<ip>.+):(?P<port>\\d+)": command "(?P<cmd>.*)"$')
    def on_rcon(self, ip, port, cmd):
        pass

    @ger.gameEvent('^Banid: "(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>" was banned "for (?P<duration>.+)" by "(?P<admin>.*)"$')
    def on_banid(self, name, cid, guid, team, duration, admin):
        client = self.storage.getClient(Client(guid=guid))
        if client:
            return self.getEvent('EVT_CLIENT_BAN_TEMP', {'duration': duration, 'admin': admin, 'reason': None}, client)
        else:
            return

    @ger.gameEvent('^\\[basecommands.smx\\] ".+<\\d+><.+><.*>" kicked "(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>.*)>"(?P<properties>.*)$')
    def on_kicked(self, name, cid, guid, team, properties):
        client = self.storage.getClient(Client(guid=guid))
        if client:
            p = parseProperties(properties)
            return self.getEvent('EVT_CLIENT_KICK', {'reason': p.get('reason', ''), 'admin': None}, client)
        else:
            return

    @ger.gameEvent('^server_message: "(?P<msg>.*)"(?P<properties>.*)$')
    def on_server_message(self, msg, properties):
        if msg in ('quit', 'restart'):
            pass
        else:
            self.warning("unexpected server_message : '%s' : please report this on the B3 forums" % msg)

    @ger.gameEvent('^(?P<data>Your server needs to be restarted.*)$', '^(?P<data>Your server is out of date.*)$')
    def on_server_restart_request(self, data):
        return self.getEvent('EVT_SERVER_REQUIRES_RESTART', data)

    @ger.gameEvent('(?x)\n        ^\n            "(?P<name>.+)<(?P<cid>\\d+)><(?P<guid>.+)><(?P<team>\\S+)>"\n            \\ stuck\n            \\ \\(position\\ "(?P<position>.+?)"\\)\n            \\ \\(duration\\ "(?P<duration>.+?)"\\)\n            (\n                \\s+L\\ .+path_goal\n                \\ \\(\\s*"(?P<path_goal>.*?)"\\s*\\)\n            )?\n        $')
    def on_bot_stuck(self, name, cid, guid, team, position, duration, path_goal=None):
        pass

    @ger.gameEvent('^(?P<data>.+)$')
    def on_unknown_line(self, data):
        """
        Catch all lines that were not handled.
        """
        self.warning('unhandled log line : %s : please report this on the B3 forums' % data)

    def getPlayerList(self):
        """
        Query the game server for connected players.
        return a dict having players' id for keys and players' data as another dict for values
        """
        return self.queryServerInfo()

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
        plist = self.getPlayerList()
        for cid, c in plist.iteritems():
            client = self.clients.getByCID(cid)
            if client:
                if client.guid == c.guid:
                    self.debug('in-sync %s == %s', client.guid, c.guid)
                else:
                    self.debug('no-sync, disconnect client %s <> %s', client.guid, c.guid)
                    client.disconnect()
                    self.getClientOrCreate(c.cid, c.guid, c.name)
            else:
                self.getClientOrCreate(c.cid, c.guid, c.name)

        if self.clients:
            client_cid_list = []
            for cl in plist.values():
                client_cid_list.append(cl.cid)

            client_list = self.clients.items()
            for cid, client in client_list:
                self.verbose2('Client in Client list %s' % client.name)
                if client.cid not in client_cid_list:
                    self.debug('Removing %s from list - left server' % client.name)
                    client.disconnect()

    def say(self, msg, *args):
        """
        Broadcast a message to all players.
        :param msg: The message to be broadcasted
        """
        msg = self.stripColors(msg % args)
        if msg and len(msg.strip()):
            template = 'sm_say %s'
            if 'B3 Say' in self.sm_plugins:
                template = 'b3_say %s'
            else:
                msg = prefixText([self.msgPrefix], msg)
            for line in self.getWrap(msg):
                self.output.write(template % line)

    def saybig(self, msg, *args):
        """
        Broadcast a message to all players in a way that will catch their attention.
        :param msg: The message to be broadcasted
        """
        msg = self.stripColors(msg % args)
        if msg and len(msg.strip()):
            template = 'sm_hsay %s'
            if 'B3 Say' in self.sm_plugins:
                template = 'b3_hsay %s'
            else:
                msg = prefixText([self.msgPrefix], msg)
            for line in self.getWrap(msg):
                self.output.write(template % line)

    def message(self, client, msg, *args):
        """
        Display a message to a given client
        :param client: The client to who send the message
        :param msg: The message to be sent
        """
        msg = self.stripColors(msg % args)
        if not client.bot:
            if msg and len(msg.strip()):
                template = 'sm_psay #%(guid)s "%(msg)s"'
                if 'B3 Say' in self.sm_plugins:
                    template = 'b3_psay #%(guid)s "%(msg)s"'
                else:
                    msg = prefixText([self.msgPrefix], msg)
                for line in self.getWrap(msg):
                    self.output.write(template % {'guid': client.guid, 'msg': line})

    def kick(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Kick a given client.
        :param client: The client to kick
        :param reason: The reason for this kick
        :param admin: The admin who performed the kick
        :param silent: Whether or not to announce this kick
        """
        self.debug('kick reason: [%s]' % reason)
        if isinstance(client, basestring):
            clients = self.clients.getByMagic(client)
            if len(clients) != 1:
                return
            client = clients[0]
        if admin:
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
            fullreason = self.getMessage('kicked_by', variables)
        else:
            variables = self.getMessageVariables(client=client, reason=reason)
            fullreason = self.getMessage('kicked', variables)
        fullreason = self.stripColors(fullreason)
        reason = self.stripColors(reason)
        self.do_kick(client, reason)
        if not silent and fullreason != '':
            self.say(fullreason)

    def ban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Ban a given client.
        :param client: The client to ban
        :param reason: The reason for this ban
        :param admin: The admin who performed the ban
        :param silent: Whether or not to announce this ban
        """
        if client.bot:
            return
        self.debug('BAN : client: %s, reason: %s', client, reason)
        if isinstance(client, basestring):
            clients = self.clients.getByMagic(client)
            if len(clients) != 1:
                return
            client = clients[0]
        if admin:
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
            fullreason = self.getMessage('banned_by', variables)
        else:
            variables = self.getMessageVariables(client=client, reason=reason)
            fullreason = self.getMessage('banned', variables)
        fullreason = self.stripColors(fullreason)
        reason = self.stripColors(reason)
        self.do_ban(client, reason)
        if admin:
            admin.message('Banned: %s (@%s) has been added to banlist' % (client.exactName, client.id))
        if not silent and fullreason != '':
            self.say(fullreason)
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN', {'reason': reason, 'admin': admin}, client))

    def unban(self, client, reason='', admin=None, silent=False, *kwargs):
        """
        Unban a client.
        :param client: The client to unban
        :param reason: The reason for the unban
        :param admin: The admin who unbanned this client
        :param silent: Whether or not to announce this unban
        """
        if client.bot:
            return
        self.debug('UNBAN: name: %s - ip: %s - guid: %s' % (client.name, client.ip, client.guid))
        if client.ip:
            self.do_unban_by_ip(client)
            self.verbose('UNBAN: removed ip (%s) from banlist' % client.ip)
            if admin:
                admin.message('Unbanned: %s. His last ip (%s) has been removed from banlist' % (
                 client.exactName, client.ip))
            if admin:
                variables = self.getMessageVariables(client=client, reason=reason, admin=admin)
                fullreason = self.getMessage('unbanned_by', variables)
            else:
                variables = self.getMessageVariables(client=client, reason=reason)
                fullreason = self.getMessage('unbanned', variables)
            if not silent and fullreason != '':
                self.say(fullreason)
        self.do_unban_by_steamid(client)
        self.verbose('UNBAN: removed guid (%s) from banlist' % client.guid)
        if admin:
            admin.message('Unbanned: removed %s guid from banlist' % client.exactName)

    def tempban(self, client, reason='', duration=2, admin=None, silent=False, *kwargs):
        """
        Tempban a client.
        :param client: The client to tempban
        :param reason: The reason for this tempban
        :param duration: The duration of the tempban
        :param admin: The admin who performed the tempban
        :param silent: Whether or not to announce this tempban
        """
        if client.bot:
            return
        self.debug('TEMPBAN : client: %s - duration: %s - reason: %s', client, duration, reason)
        if isinstance(client, basestring):
            clients = self.clients.getByMagic(client)
            if len(clients) != 1:
                return
            client = clients[0]
        if admin:
            banduration = minutesStr(duration)
            variables = self.getMessageVariables(client=client, reason=reason, admin=admin, banduration=banduration)
            fullreason = self.getMessage('temp_banned_by', variables)
        else:
            banduration = minutesStr(duration)
            variables = self.getMessageVariables(client=client, reason=reason, banduration=banduration)
            fullreason = self.getMessage('temp_banned', variables)
        fullreason = self.stripColors(fullreason)
        reason = self.stripColors(reason)
        self.do_tempban(client, duration, reason)
        if not silent and fullreason != '':
            self.say(fullreason)
        data = {'reason': reason, 'duration': duration, 'admin': admin}
        self.queueEvent(self.getEvent('EVT_CLIENT_BAN_TEMP', data=data, client=client))

    def getMap(self):
        """
        Return the current map/level name.
        """
        return self.getCvar('host_map')['value'][0:-4]

    def getMaps(self):
        """
        Return the available maps/levels name.
        """
        mapfile = Cvar.getString(self.getCvar('mapcyclefile'))
        game_log = self.config.getpath('server', 'game_log')
        folder = game_log.rpartition('console.log')
        mapcyclefile = folder[0] + mapfile
        map_rotation = []
        self.map_cycles = {}
        self.map_cycle_no = 0
        f = open(mapcyclefile, 'r')
        for line in f:
            if len(line):
                map_rotation.append(line)

        f.close()
        return map_rotation

    def rotateMap(self):
        """
        Load the next map/level
        """
        next_map = self.getNextMap()
        if next_map:
            self.saybig('Changing to next map : %s' % next_map)
            time.sleep(1)
            self.output.write('map %s' % next_map)

    def changeMap(self, map_name, gamemode_name=''):
        """
        Load a given map/level
        Return a list of suggested map names in cases it fails to recognize the map that was provided.
        """
        map_name = self.getMapsSoundingLike(map_name)
        if not isinstance(map_name, basestring):
            return map_name
        self.saybig('Changing map to: %s - %s' % (map_name, gamemode_name))
        time.sleep(5)
        self.output.write('changelevel %s %s' % (map_name, gamemode_name))

    def checkGameMode(self, map_name, gamemode_name):
        if gamemode_name in ('hunt', ):
            if map_name.find('_hunt') == -1:
                map_name += '_hunt'
        elif gamemode_name in ('checkpoint', 'outpost'):
            if map_name.find('_coop') == -1:
                map_name += '_coop'
        return map_name

    def getPlayerPings(self, filter_client_ids=None):
        """
        Returns a dict having players' id for keys and players' ping for values.
        """
        clients = self.queryServerInfo()
        pings = {}
        for cid, client in clients.iteritems():
            pings[cid] = client.ping

        return pings

    def getPlayerScores(self):
        """
        Returns a dict having players' id for keys and players' scores for values.
        """
        return dict()

    def inflictCustomPenalty(self, penalty_type, client, reason=None, duration=None, admin=None, data=None):
        r"""
        Called if b3.admin.penalizeClient() does not know a given penalty type.
        Overwrite this to add customized penalties for your game like 'slap', 'nuke',
        'mute', 'kill' or anything you want.
        /!\ This method must return True if the penalty was inflicted.
        """
        pass

    def getNextMap(self):
        """
        Return the next map in the map rotation list
        """
        if 'nextmap' in self.sm_plugins:
            next_map = self.getCvar('sm_nextmap')
            return next_map
        else:
            return 'Not available, Source Mod "nextmap" plugin not loaded'

    def parseLine(self, line):
        """
        Parse a single line from the log file.
        """
        if line is None:
            return
        else:
            if line.startswith('mp\x08 \x08\x08 \x08'):
                line = line[8:]
            text = line.decode('UTF-8', 'replace')
            data = None
            m = re.match(RE_HL_LOG_LINE, text)
            if m:
                data = m.group('data')
            elif text.startswith('Gamerules: entering state '):
                data = text
            if data is not None:
                hfunc, param_dict = ger.getHandler(data)
                if hfunc:
                    self.verbose2('calling %s%r' % (hfunc.func_name, param_dict))
                    event = hfunc(self, **param_dict)
                    if event:
                        self.queueEvent(event)
            return

    def getClient(self, cid, guid):
        """
        Return an already connected client by searching the clients cid index.
        May return None
        """
        if guid == 'BOT':
            guid = self.botGUID(cid, guid)
        client = self.clients.getByCID(cid)
        if client:
            if client.guid != guid:
                client.disconnect()
                self.sync()
                return
            else:
                return client

        return

    def getClientOrCreate(self, cid, guid, name, team=None):
        """
        Return an already connected client by searching the clients cid index or create a new client.
        May return None
        """
        bot = False
        hide = False
        if guid == 'BOT':
            guid = self.botGUID(cid, guid)
            bot = True
            hide = True
        client = self.clients.getByGUID(guid)
        if client and client.cid != cid:
            self.sync()
        client = self.clients.getByCID(cid)
        if client and client.guid != guid:
            self.sync()
        client = self.clients.getByCID(cid)
        if client is None:
            client = self.clients.newClient(cid, guid=guid, name=name, bot=bot, hide=hide, team=TEAM_UNKNOWN)
            client.last_update_time = time.time()
        elif name:
            client.name = name
        if team:
            parsed_team = self.getTeam(team)
            if parsed_team is not None:
                client.team = parsed_team
        return client

    def getTeam(self, team):
        """
        Convert Insurgency team id to B3 team numbers
        """
        if not team:
            return
        else:
            if team == '#Team_Unassigned':
                return TEAM_UNKNOWN
            else:
                if team == '#Team_Insurgent':
                    return TEAM_BLUE
                if team == '#Team_Security':
                    return TEAM_RED
                if team == 'Spectator':
                    return TEAM_SPEC
                self.warning('unexpected team id: %r. Please report this on the B3 forums' % team)
                return

            return

    def queryServerInfo(self):
        """
        Query the server for its status and refresh local data :
          self.game.sv_hostname
          self.game.mapName
        furthermore, discover connected players, refresh their ping and ip info
        finally return a dict of <cid, client>
        """
        current_clients = dict()
        rv = self.output.write('status')
        self.verbose2('Querying Server Status')
        if rv:
            self.verbose2('Status: %s' % rv)
            re_player = re.compile('^#\\s*(?P<cid>\\d+) (?:\\d+) "(?P<name>.+)" (?P<guid>\\S+) (?P<duration>\\d+:\\d+) (?P<ping>\\d+) (?P<loss>\\S+) (?P<state>\\S+) (?P<rate>\\d+) (?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+):(?P<port>\\d+)$')
            for line in rv.split('\n'):
                if not line or line.startswith('L '):
                    continue
                if line.startswith('hostname:'):
                    self.game.sv_hostname = line[10:]
                elif line.startswith('map     :'):
                    self.game.mapName = line[10:]
                else:
                    m = re.match(re_player, line)
                    if m:
                        client = self.getClientOrCreate(m.group('cid'), m.group('guid'), m.group('name'))
                        client.ping = m.group('ping')
                        client.ip = m.group('ip')
                        current_clients[client.cid] = client

            self.verbose2('Current Client List: %s' % current_clients)
            return current_clients

    def getAllAvailableMaps(self):
        """
        Return the available maps for the server, even if not in the map rotation list
        This returns ALL maps on the server
        """
        re_maps = re.compile('^PENDING:\\s+\\(fs\\)\\s+(?P<map_name>.+)\\.bsp$')
        response = []
        for line in self.output.write('maps *').split('\n'):
            m = re.match(re_maps, line)
            if m:
                response.append(m.group('map_name'))

        return response

    def getCvar(self, cvarName):
        """
        Return a CVAR from the game server.
        :param cvarName: The CVAR name
        """
        if not cvarName:
            self.warning('trying to query empty cvar %r' % cvarName)
            return
        else:
            rv = self.output.write(cvarName)
            m = re.search(RE_CVAR, rv)
            if m:
                return Cvar(cvarName, value=m.group('value'), default=m.group('default'))
            return
            return

    def setCvar(self, cvarName, value):
        """
        Set a CVAR on the game server.
        :param cvarName: The CVAR name
        :param value: The CVAR value
        """
        if re.match('^[a-z0-9_.]+$', cvarName, re.I):
            self.debug('Set cvar %s = [%s]', cvarName, value)
            self.write(self.getCommand('set', name=cvarName, value=value))
        else:
            self.error('%s is not a valid cvar name', cvarName)

    def do_kick(self, client, reason=None):
        """
        Kick a client.
        :param client: The client to kick
        :param reason: The reason for the kick
        """
        if not client.cid:
            self.warning('trying to kick %s which has no slot id' % client)
        else:
            if reason:
                self.output.write('sm_kick #%s %s' % (client.cid, reason))
            else:
                self.output.write('sm_kick #%s' % client.cid)
            client.disconnect()

    def do_ban(self, client, reason=None):
        """
        Ban a client.
        :param client: The client to ban
        :param reason: The reason for the ban
        """
        if reason:
            self.output.write('sm_addban %s "%s" %s' % (0, client.guid, reason))
        else:
            self.output.write('sm_addban %s "%s"' % (0, client.guid))
        self.do_kick(client, reason)

    def do_tempban(self, client, duration=2, reason=None):
        """
        Tempban a client.
        :param client: The client to tempban
        :param duration: The tempban duration
        :param reason: The reason for the tempban
        """
        if reason:
            self.output.write('sm_addban %s "%s" %s' % (int(time2minutes(duration)), client.guid, reason))
        else:
            self.output.write('sm_addban %s "%s"' % (int(time2minutes(duration)), client.guid))
        self.do_kick(client, reason)

    def do_unban_by_steamid(self, client):
        """
        Unban a client using his GUID.
        :param client: The client to unban
        """
        self.output.write('sm_unban "%s"' % client.guid)

    def do_unban_by_ip(self, client):
        """
        Unban a client using his IP address.
        :param client: The client to unban
        """
        self.output.write('sm_unban %s' % client.ip)

    def is_sourcemod_installed(self):
        """
        Return a True if Source Mod is installed on the game server
        """
        data = self.output.write('sm version')
        if data:
            if data.startswith('Unknown command'):
                return False
            for m in data.splitlines():
                self.info(m.strip())

            return True
        return False

    def get_loaded_sm_plugins(self):
        """
        Return a dict with SourceMod plugins' name as keys and value is a tuple (index, version, author)
        """
        re_sm_plugin = re.compile('^(?P<index>.+) "(?P<name>.+)" \\((?P<version>.+)\\) by (?P<author>.+)$', re.MULTILINE)
        response = dict()
        data = self.output.write('sm plugins list')
        if data:
            for m in re.finditer(re_sm_plugin, data):
                response[m.group('name')] = (
                 m.group('index'), m.group('version'), m.group('author'))

        return response

    def getMapsSoundingLike(self, mapname):
        """
        Return a valid mapname.
        If no exact match is found, then return close candidates as a list
        """
        supported_maps = [ m.lower() for m in self.getAllAvailableMaps() ]
        wanted_map = mapname.lower()
        if wanted_map in supported_maps:
            return wanted_map
        else:
            matches = getStuffSoundingLike(wanted_map, supported_maps)
            if len(matches) == 1:
                return matches[0]
            return matches

    def botGUID(self, cid, guid):
        """
        Return a unique guid for a bot
        Otherwise all bots g=have guid = BOT
        """
        botguid = guid + str(cid)
        self.verbose2('BOT guid is %s' % botguid)
        return botguid
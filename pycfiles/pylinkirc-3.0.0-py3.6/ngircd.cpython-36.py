# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/ngircd.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 24970 bytes
"""
ngircd.py: PyLink protocol module for ngIRCd.
"""
import re, time
from pylinkirc import __version__, conf, utils
from pylinkirc.classes import *
from pylinkirc.log import log
from pylinkirc.protocols.ircs2s_common import *

class NgIRCdProtocol(IRCS2SProtocol):

    def __init__(self, irc):
        super().__init__(irc)
        self.conf_keys -= {'sid', 'sidrange'}
        self.casemapping = 'ascii'
        self.hook_map = {'NJOIN': 'JOIN'}
        self.has_eob = False
        self._caps = {}
        self._use_builtin_005_handling = True
        self.protocol_caps.discard('has-ts')
        self.protocol_caps |= {'slash-in-hosts', 'underscore-in-hosts'}

    def post_connect(self):
        self.send('PASS %s 0210-IRC+ PyLink|%s:CHLMoX' % (self.serverdata['sendpass'], __version__))
        self.send('SERVER %s 1 :%s' % (self.serverdata['hostname'],
         self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']))
        self._uidgen = PUIDGenerator('PUID')
        self._sidgen = PUIDGenerator('PSID', start=1)
        self.sid = self._sidgen.next_sid(prefix=(self.serverdata['hostname']))
        self._caps.clear()
        self.cmodes.update({'banexception':'e', 
         'invex':'I', 
         'noinvite':'V', 
         'nokick':'Q', 
         'nonick':'N', 
         'operonly':'O', 
         'permanent':'P', 
         'registered':'r', 
         'regmoderated':'M', 
         'regonly':'R', 
         'sslonly':'z'})
        self.umodes.update({'away':'a', 
         'bot':'B', 
         'cloak':'x', 
         'deaf_commonchan':'C', 
         'floodexempt':'F', 
         'hidechans':'I', 
         'privdeaf':'b', 
         'registered':'R', 
         'restricted':'r', 
         'servprotect':'q', 
         'sno_clientconnections':'c'})

    def spawn_client(self, nick, ident='null', host='null', realhost=None, modes=set(), server=None, ip='0.0.0.0', realname=None, ts=None, opertype='IRC Operator', manipulatable=False):
        """
        Spawns a new client with the given options.

        Note: No nick collision / valid nickname checks are done here; it is
        up to plugins to make sure they don't introduce anything invalid.

        Note 2: IP and realhost are ignored because ngIRCd does not send them.
        """
        server = server or self.sid
        assert '@' in server, 'Need PSID for spawn_client, not pure server name!'
        if not self.is_internal_server(server):
            raise ValueError('Server %r is not a PyLink server!' % server)
        realname = realname or conf.conf['pylink']['realname']
        uid = self._uidgen.next_uid(prefix=nick)
        userobj = self.users[uid] = User(self, nick, (ts or int(time.time())), uid, server, ident=ident,
          host=host,
          realname=realname,
          manipulatable=manipulatable,
          opertype=opertype,
          realhost=host)
        self.apply_modes(uid, modes)
        self.servers[server].users.add(uid)
        server_token = server.rsplit('@')[(-1)]
        self._send_with_prefix(server, 'NICK %s %s %s %s %s %s :%s' % (nick, self.servers[server].hopcount,
         ident, host, server_token, self.join_modes(modes), realname))
        return userobj

    def spawn_server(self, name, sid=None, uplink=None, desc=None):
        """
        Spawns a server off a PyLink server.

        * desc (server description) defaults to the one in the config.
        * uplink defaults to the main PyLink server.
        * SID is set equal to the server name for ngIRCd, as server UIDs are not used.
        """
        uplink = uplink or self.sid
        assert uplink in self.servers, 'Unknown uplink %r?' % uplink
        name = name.lower()
        sid = self._sidgen.next_sid(prefix=name)
        desc = desc or self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']
        if sid in self.servers:
            raise ValueError('A server named %r already exists!' % sid)
        if not self.is_internal_server(uplink):
            raise ValueError('Server %r is not a PyLink server!' % uplink)
        if not self.is_server_name(name):
            raise ValueError('Invalid server name %r' % name)
        server_token = sid.rsplit('@')[(-1)]
        self.servers[sid] = Server(self, uplink, name, internal=True, desc=desc)
        self._send_with_prefix(uplink, 'SERVER %s %s %s :%s' % (name, self.servers[sid].hopcount, server_token, desc))
        return sid

    def away(self, source, text):
        """Sends an AWAY message from a PyLink client. If the text is empty, away status is unset."""
        if not self.is_internal_client(source):
            raise LookupError('No such PyLink client exists.')
        else:
            modes = self.users[source].modes
            if text:
                if ('a', None) not in modes:
                    self.mode(source, source, [('+a', None)])
            if ('a', None) in modes:
                self.mode(source, source, [('-a', None)])
        self.users[source].away = text

    def join(self, client, channel):
        if not self.is_internal_client(client):
            raise LookupError('No such PyLink client exists.')
        self._send_with_prefix(client, 'JOIN %s' % channel)
        self._channels[channel].users.add(client)
        self.users[client].channels.add(channel)

    def kill(self, source, target, reason):
        """Sends a kill from a PyLink client/server."""
        if not self.is_internal_client(source):
            if not self.is_internal_server(source):
                raise LookupError('No such PyLink client/server exists.')
        self._send_with_prefix(source, 'KILL %s :KILLed by %s: %s' % (self._expandPUID(target),
         self.get_friendly_name(source), reason))
        if self.is_internal_client(target):
            self._remove_client(target)

    def knock(self, numeric, target, text):
        raise NotImplementedError('KNOCK is not supported on ngIRCd.')

    def mode(self, source, target, modes, ts=None):
        """Sends mode changes from a PyLink client/server. The TS option is not used on ngIRCd."""
        if not self.is_internal_client(source):
            if not self.is_internal_server(source):
                raise LookupError('No such PyLink client/server %r exists' % source)
        else:
            self.apply_modes(target, modes)
            modes = list(modes)
            if self.is_channel(target):
                msgprefix = ':%s MODE %s ' % (self._expandPUID(source), target)
                bufsize = self.S2S_BUFSIZE - len(msgprefix)
                for idx, mode in enumerate(modes):
                    if mode[0][(-1)] in self.prefixmodes:
                        log.debug('(%s) mode: expanding PUID of mode %s', self.name, str(mode))
                        modes[idx] = (mode[0], self._expandPUID(mode[1]))

                for modestr in self.wrap_modes(modes, bufsize, max_modes_per_msg=12):
                    self.send(msgprefix + modestr)

            else:
                joinedmodes = self.join_modes(modes)
                self._send_with_prefix(source, 'MODE %s %s' % (self._expandPUID(target), joinedmodes))

    def nick(self, source, newnick):
        """Changes the nick of a PyLink client."""
        if not self.is_internal_client(source):
            raise LookupError('No such PyLink client exists.')
        self._send_with_prefix(source, 'NICK %s' % newnick)
        self.users[source].nick = newnick
        self.users[source].ts = int(time.time())

    def sjoin(self, server, channel, users, ts=None, modes=set()):
        """Sends an SJOIN for a group of users to a channel.

        The sender should always be a Server ID (SID). TS is optional, and defaults
        to the one we've stored in the channel state if not given.
        <users> is a list of (prefix mode, UID) pairs:

        Example uses:
            sjoin('100', '#test', [('', 'user0@0'), ('o', user1@1'), ('v', 'someone@2')])
            sjoin(self.sid, '#test', [('o', self.pseudoclient.uid)])
        """
        server = server or self.sid
        if not server:
            raise LookupError('No such PyLink client exists.')
        log.debug('(%s) sjoin: got %r for users', self.name, users)
        njoin_prefix = ':%s NJOIN %s :' % (self._expandPUID(server), channel)
        nicks_to_send = []
        for userpair in users:
            prefixes, uid = userpair
            if uid not in self.users:
                log.warning('(%s) Trying to NJOIN missing user %s?', self.name, uid)
                continue
            else:
                if uid in self._channels[channel].users:
                    continue
            self._channels[channel].users.add(uid)
            self.users[uid].channels.add(channel)
            self.apply_modes(channel, (('+%s' % prefix, uid) for prefix in userpair[0]))
            nicks_to_send.append(''.join(self.prefixmodes[modechar] for modechar in userpair[0]) + self._expandPUID(userpair[1]))

        if nicks_to_send:
            for message in utils.wrap_arguments(njoin_prefix, nicks_to_send, (self.S2S_BUFSIZE), separator=',', max_args_per_line=13):
                self.send(message)

        if modes:
            log.debug('(%s) sjoin: bursting modes %r for channel %r now', self.name, modes, channel)
            self.mode(server, channel, modes)

    def set_server_ban(self, source, duration, user='*', host='*', reason='User banned'):
        """
        Sets a server ban.
        """
        assert not user == host == '*', 'Refusing to set ridiculous ban on *@*'
        self._send_with_prefix(source, 'GLINE *!%s@%s %s :%s' % (user, host, duration, reason))

    def update_client(self, target, field, text):
        """Updates the ident, host, or realname of any connected client."""
        field = field.upper()
        if field not in ('IDENT', 'HOST', 'REALNAME', 'GECOS'):
            raise NotImplementedError('Changing field %r of a client is unsupported by this protocol.' % field)
        real_target = self._expandPUID(target)
        if field == 'IDENT':
            self.users[target].ident = text
            self._send_with_prefix(self.sid, 'METADATA %s user :%s' % (real_target, text))
            if not self.is_internal_client(target):
                self.call_hooks([self.sid, 'CHGIDENT', {'target':target,  'newident':text}])
            elif field == 'HOST':
                self.users[target].host = text
                if self.is_internal_client(target):
                    self._send_with_prefix(self.sid, 'METADATA %s host :%s' % (real_target, text))
                else:
                    self._send_with_prefix(self.sid, 'METADATA %s cloakhost :%s' % (real_target, text))
                    if ('x', None) not in self.users[target].modes:
                        log.debug('(%s) Forcing umode +x on %r as part of cloak setting', self.name, target)
                        self.mode(self.sid, target, [('+x', None)])
            else:
                self.call_hooks([self.sid, 'CHGHOST', {'target':target,  'newhost':text}])
        elif field in ('REALNAME', 'GECOS'):
            self.users[target].realname = text
            self._send_with_prefix(self.sid, 'METADATA %s info :%s' % (real_target, text))
            if not self.is_internal_client(target):
                self.call_hooks([self.sid, 'CHGNAME', {'target':target,  'newgecos':text}])

    def handle_376(self, source, command, args):

        def f(numeric, msg):
            self._send_with_prefix(self.sid, '%s %s %s' % (numeric, self.uplink, msg))

        f('005', 'NETWORK=%s :is my network name' % self.get_full_network_name())
        f('005', 'RFC2812 IRCD=PyLink CHARSET=UTF-8 CASEMAPPING=%s PREFIX=%s CHANTYPES=# CHANMODES=%s,%s,%s,%s :are supported on this server' % (
         self.casemapping, self._caps['PREFIX'],
         self.cmodes['*A'], self.cmodes['*B'], self.cmodes['*C'], self.cmodes['*D']))
        f('005', 'CHANNELLEN NICKLEN=%s EXCEPTS=E INVEX=I :are supported on this server' % self.maxnicklen)
        f('376', ":End of server negotiation, happy PyLink'ing!")

    def handle_chaninfo(self, source, command, args):
        channel = args[0]
        modes = self.parse_modes(channel, args[1].replace('l', '').replace('k', ''))
        if len(args) >= 3:
            topic = args[(-1)]
            if topic:
                log.debug('(%s) handle_chaninfo: setting topic for %s to %r', self.name, channel, topic)
                self._channels[channel].topic = topic
                self._channels[channel].topicset = True
        if len(args) >= 5:
            key = args[2]
            limit = args[3]
            if key != '*':
                modes.append(('+k', key))
            if limit != '0':
                modes.append(('+l', limit))
        self.apply_modes(channel, modes)

    def handle_join(self, source, command, args):
        for chanpair in args[0].split(','):
            try:
                channel, status = chanpair.split('\x07', 1)
                if status in 'ov':
                    self.apply_modes(channel, [('+' + status, source)])
            except ValueError:
                channel = chanpair

            c = self._channels[channel]
            self.users[source].channels.add(channel)
            self._channels[channel].users.add(source)
            self.call_hooks([source, command, {'channel':channel,  'users':[source],  'modes':c.modes}])

    def handle_kill(self, source, command, args):
        killed = self._get_UID(args[0])
        if self.is_internal_client(killed):
            return super().handle_kill(source, command, args)
        log.debug("(%s) Ignoring KILL to %r as it isn't meant for us; we should see a QUIT soon", self.name, killed)

    def _check_cloak_change(self, target):
        u = self.users[target]
        old_host = u.host
        if ('x', None) in u.modes:
            if u.cloaked_host:
                u.host = u.cloaked_host
        if u.realhost:
            u.host = u.realhost
        if old_host != u.host:
            self.call_hooks([target, 'CHGHOST', {'target':target,  'newhost':u.host}])

    def handle_metadata(self, source, command, args):
        """Handles various user metadata for ngIRCd (cloaked host, account name, etc.)"""
        target = self._get_UID(args[0])
        if target not in self.users:
            log.warning('(%s) Ignoring METADATA to missing user %r?', self.name, target)
            return
        datatype = args[1]
        u = self.users[target]
        if datatype == 'cloakhost':
            u.cloaked_host = args[(-1)]
            self._check_cloak_change(target)
        else:
            if datatype == 'host':
                u.realhost = args[(-1)]
                self._check_cloak_change(target)
            else:
                if datatype == 'user':
                    u.ident = args[(-1)]
                    self.call_hooks([target, 'CHGIDENT', {'target':target,  'newident':args[-1]}])
                else:
                    if datatype == 'info':
                        u.realname = args[(-1)]
                        self.call_hooks([target, 'CHGNAME', {'target':target,  'newgecos':args[-1]}])
                    elif datatype == 'accountname':
                        self.call_hooks([target, 'CLIENT_SERVICES_LOGIN', {'text': args[(-1)]}])

    def handle_nick(self, source, command, args):
        """
        Handles the NICK command, used for server introductions and nick changes.
        """
        if len(args) >= 2:
            nick = args[0]
            assert source in self.servers, "Server %r tried to introduce nick %r but isn't in the servers index?" % (source, nick)
            self._check_nick_collision(nick)
            ident = args[2]
            host = args[3]
            uid = self._uidgen.next_uid(prefix=nick)
            realname = args[(-1)]
            ts = int(time.time())
            self.users[uid] = User(self, nick, ts, uid, source, ident=ident, host=host, realname=realname,
              realhost=host)
            parsedmodes = self.parse_modes(uid, [args[5]])
            self.apply_modes(uid, parsedmodes)
            self.servers[source].users.add(uid)
            self._check_umode_away_change(uid)
            self._check_cloak_change(uid)
            return {'uid':uid, 
             'ts':ts,  'nick':nick,  'realhost':host,  'host':host,  'ident':ident,  'parse_as':'UID', 
             'ip':'0.0.0.0'}
        else:
            oldnick = self.users[source].nick
            newnick = self.users[source].nick = args[0]
            return {'newnick':newnick,  'oldnick':oldnick}

    def handle_njoin--- This code section failed: ---

 L. 497         0  LOAD_FAST                'args'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  STORE_FAST               'channel'

 L. 498         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _channels
               12  LOAD_FAST                'channel'
               14  BINARY_SUBSCR    
               16  LOAD_ATTR                deepcopy
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  STORE_FAST               'chandata'

 L. 499        22  BUILD_LIST_0          0 
               24  STORE_FAST               'namelist'

 L. 502        26  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               28  LOAD_STR                 'NgIRCdProtocol.handle_njoin.<locals>.<dictcomp>'
               30  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                prefixmodes
               36  LOAD_ATTR                items
               38  CALL_FUNCTION_0       0  '0 positional arguments'
               40  GET_ITER         
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  STORE_DEREF              'prefixchars'

 L. 503        46  SETUP_LOOP          206  'to 206'
               48  LOAD_FAST                'args'
               50  LOAD_CONST               1
               52  BINARY_SUBSCR    
               54  LOAD_ATTR                split
               56  LOAD_STR                 ','
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  GET_ITER         
               62  FOR_ITER            204  'to 204'
               64  STORE_FAST               'userpair'

 L. 505        66  LOAD_GLOBAL              re
               68  LOAD_ATTR                search
               70  LOAD_STR                 '([%s]*)(.*)'
               72  LOAD_STR                 ''
               74  LOAD_ATTR                join
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                prefixmodes
               80  LOAD_ATTR                values
               82  CALL_FUNCTION_0       0  '0 positional arguments'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  BINARY_MODULO    
               88  LOAD_FAST                'userpair'
               90  CALL_FUNCTION_2       2  '2 positional arguments'
               92  STORE_FAST               'r'

 L. 506        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _get_UID
               98  LOAD_FAST                'r'
              100  LOAD_ATTR                group
              102  LOAD_CONST               2
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  STORE_DEREF              'user'

 L. 507       110  LOAD_FAST                'r'
              112  LOAD_ATTR                group
              114  LOAD_CONST               1
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  STORE_FAST               'modeprefix'

 L. 509       120  LOAD_FAST                'modeprefix'
              122  POP_JUMP_IF_FALSE   156  'to 156'

 L. 510       124  LOAD_CLOSURE             'prefixchars'
              126  LOAD_CLOSURE             'user'
              128  BUILD_TUPLE_2         2 
              130  LOAD_SETCOMP             '<code_object <setcomp>>'
              132  LOAD_STR                 'NgIRCdProtocol.handle_njoin.<locals>.<setcomp>'
              134  MAKE_FUNCTION_8          'closure'
              136  LOAD_FAST                'modeprefix'
              138  GET_ITER         
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  STORE_FAST               'modes'

 L. 511       144  LOAD_FAST                'self'
              146  LOAD_ATTR                apply_modes
              148  LOAD_FAST                'channel'
              150  LOAD_FAST                'modes'
              152  CALL_FUNCTION_2       2  '2 positional arguments'
              154  POP_TOP          
            156_0  COME_FROM           122  '122'

 L. 512       156  LOAD_FAST                'namelist'
              158  LOAD_ATTR                append
              160  LOAD_DEREF               'user'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  POP_TOP          

 L. 515       166  LOAD_FAST                'self'
              168  LOAD_ATTR                users
              170  LOAD_DEREF               'user'
              172  BINARY_SUBSCR    
              174  LOAD_ATTR                channels
              176  LOAD_ATTR                add
              178  LOAD_FAST                'channel'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  POP_TOP          

 L. 516       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _channels
              188  LOAD_FAST                'channel'
              190  BINARY_SUBSCR    
              192  LOAD_ATTR                users
              194  LOAD_ATTR                add
              196  LOAD_DEREF               'user'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  POP_TOP          
              202  JUMP_BACK            62  'to 62'
              204  POP_BLOCK        
            206_0  COME_FROM_LOOP       46  '46'

 L. 518       206  LOAD_FAST                'channel'
              208  LOAD_FAST                'namelist'
              210  BUILD_LIST_0          0 
              212  LOAD_FAST                'chandata'
              214  LOAD_CONST               ('channel', 'users', 'modes', 'channeldata')
              216  BUILD_CONST_KEY_MAP_4     4 
              218  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 130

    def handle_pass(self, source, command, args):
        """
        Handles phase one of the ngIRCd login process (password auth and version info).
        """
        recvpass = args[0]
        if recvpass != self.serverdata['recvpass']:
            raise ProtocolError('RECVPASS from uplink does not match configuration!')
        if 'IRC+' not in args[1]:
            raise ProtocolError('Linking to non-ngIRCd server using this protocol module is not supported')

    def handle_ping(self, source, command, args):
        """
        Handles incoming PINGs (and implicit end of burst).
        """
        self._send_with_prefix((self.sid), ('PONG %s :%s' % (self._expandPUID(self.sid), args[(-1)])), queue=False)
        if not self.servers[source].has_eob:
            self.servers[source].has_eob = True
            if source == self.uplink:
                self.connected.set()
            return {'parse_as': 'ENDBURST'}

    def handle_server(self, source, command, args):
        """
        Handles the SERVER command.
        """
        servername = args[0].lower()
        serverdesc = args[(-1)]
        self.servers[servername] = Server(self, (source if source != servername else None), servername, desc=serverdesc)
        if self.uplink is None:
            self.uplink = servername
            log.debug('(%s) Got %s as uplink', self.name, servername)
        else:
            return {'name':servername, 
             'sid':None,  'text':serverdesc}


Class = NgIRCdProtocol
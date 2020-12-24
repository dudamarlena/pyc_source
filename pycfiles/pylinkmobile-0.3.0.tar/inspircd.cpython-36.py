# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/inspircd.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 48109 bytes
__doc__ = '\ninspircd.py: InspIRCd 2.0, 3.x protocol module for PyLink.\n'
import threading, time
from pylinkirc import conf, utils
from pylinkirc.classes import *
from pylinkirc.log import log
from pylinkirc.protocols.ts6_common import *

class InspIRCdProtocol(TS6BaseProtocol):
    S2S_BUFSIZE = 0
    SUPPORTED_IRCDS = ['insp20', 'insp3']
    DEFAULT_IRCD = SUPPORTED_IRCDS[0]
    MAX_PROTO_VER = 1205

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.protocol_caps |= {'slash-in-nicks', 'slash-in-hosts', 'underscore-in-hosts'}
        self.casemapping = 'rfc1459'
        self.hook_map = {'FJOIN':'JOIN', 
         'RSQUIT':'SQUIT',  'FMODE':'MODE',  'FTOPIC':'TOPIC', 
         'OPERTYPE':'MODE',  'FHOST':'CHGHOST',  'FIDENT':'CHGIDENT', 
         'FNAME':'CHGNAME',  'SVSTOPIC':'TOPIC',  'SAKICK':'KICK', 
         'IJOIN':'JOIN'}
        ircd_target = self.serverdata.get('target_version', self.DEFAULT_IRCD).lower()
        if ircd_target == 'insp20':
            self.proto_ver = 1202
        else:
            if ircd_target == 'insp3':
                self.proto_ver = 1205
            else:
                raise ProtocolError('Unsupported target_version %r: supported values include %s' % (ircd_target, self.SUPPORTED_IRCDS))
        log.debug('(%s) inspircd: using protocol version %s for target_version %r', self.name, self.proto_ver, ircd_target)
        self._prefix_levels = {}
        self._modsupport = set()
        self._endburst_delay = 0

    def spawn_client(self, nick, ident='null', host='null', realhost=None, modes=set(), server=None, ip='0.0.0.0', realname=None, ts=None, opertype='IRC Operator', manipulatable=False):
        """
        Spawns a new client with the given options.

        Note: No nick collision / valid nickname checks are done here; it is
        up to plugins to make sure they don't introduce anything invalid.
        """
        server = server or self.sid
        if not self.is_internal_server(server):
            raise ValueError('Server %r is not a PyLink server!' % server)
        uid = self.uidgen[server].next_uid()
        ts = ts or int(time.time())
        realname = realname or conf.conf['pylink']['realname']
        realhost = realhost or host
        raw_modes = self.join_modes(modes)
        u = self.users[uid] = User(self, nick, ts, uid, server, ident=ident, host=host, realname=realname,
          realhost=realhost,
          ip=ip,
          manipulatable=manipulatable,
          opertype=opertype)
        self.apply_modes(uid, modes)
        self.servers[server].users.add(uid)
        self._send_with_prefix(server, 'UID {uid} {ts} {nick} {realhost} {host} {ident} {ip} {ts} {modes} + :{realname}'.format(ts=ts,
          host=host,
          nick=nick,
          ident=ident,
          uid=uid,
          modes=raw_modes,
          ip=ip,
          realname=realname,
          realhost=realhost))
        if ('o', None) in modes or ('+o', None) in modes:
            self._oper_up(uid, opertype)
        return u

    def join(self, client, channel):
        """Joins a PyLink client to a channel."""
        server = self.get_server(client)
        if not self.is_internal_server(server):
            log.error('(%s) Error trying to join %r to %r (no such client exists)', self.name, client, channel)
            raise LookupError('No such PyLink client exists.')
        modes = [m for m in self._channels[channel].modes if m[0] not in self.cmodes['*A']]
        self._send_with_prefix(server, 'FJOIN {channel} {ts} {modes} :,{uid}'.format(ts=(self._channels[channel].ts),
          uid=client,
          channel=channel,
          modes=(self.join_modes(modes))))
        self._channels[channel].users.add(client)
        self.users[client].channels.add(channel)

    def sjoin(self, server, channel, users, ts=None, modes=set()):
        """Sends an SJOIN for a group of users to a channel.

        The sender should always be a Server ID (SID). TS is optional, and defaults
        to the one we've stored in the channel state if not given.
        <users> is a list of (prefix mode, UID) pairs:

        Example uses:
            sjoin('100', '#test', [('', '100AAABBC'), ('qo', 100AAABBB'), ('h', '100AAADDD')])
            sjoin(self.sid, '#test', [('o', self.pseudoclient.uid)])
        """
        server = server or self.sid
        assert users, 'sjoin: No users sent?'
        log.debug('(%s) sjoin: got %r for users', self.name, users)
        if not server:
            raise LookupError('No such PyLink client exists.')
        modes = modes or self._channels[channel].modes
        orig_ts = self._channels[channel].ts
        ts = ts or orig_ts
        banmodes = []
        regularmodes = []
        for mode in modes:
            modechar = mode[0][(-1)]
            if modechar in self.cmodes['*A']:
                if (
                 modechar, mode[1]) not in self._channels[channel].modes:
                    banmodes.append(mode)
            else:
                regularmodes.append(mode)

        uids = []
        changedmodes = set(modes)
        namelist = []
        for userpair in users:
            assert len(userpair) == 2, 'Incorrect format of userpair: %r' % userpair
            prefixes, user = userpair
            namelist.append(','.join(userpair))
            uids.append(user)
            for m in prefixes:
                changedmodes.add(('+%s' % m, user))

            try:
                self.users[user].channels.add(channel)
            except KeyError:
                log.debug("(%s) sjoin: KeyError trying to add %r to %r's channel list?", self.name, channel, user)

        namelist = ' '.join(namelist)
        self._send_with_prefix(server, 'FJOIN {channel} {ts} {modes} :{users}'.format(ts=ts,
          users=namelist,
          channel=channel,
          modes=(self.join_modes(modes))))
        self._channels[channel].users.update(uids)
        if banmodes:
            self._send_with_prefix(server, 'FMODE {channel} {ts} {modes} '.format(ts=ts,
              channel=channel,
              modes=(self.join_modes(banmodes))))
        self.updateTS(server, channel, ts, changedmodes)

    def _oper_up(self, target, opertype=None):
        """Opers a client up (internal function specific to InspIRCd).

        This should be called whenever user mode +o is set on anyone, because
        InspIRCd requires a special command (OPERTYPE) to be sent in order to
        recognize ANY non-burst oper ups.

        Plugins don't have to call this function themselves, but they can
        set the opertype attribute of an User object (in self.users),
        and the change will be reflected here."""
        userobj = self.users[target]
        try:
            otype = opertype or userobj.opertype or 'IRC Operator'
        except AttributeError:
            log.debug("(%s) opertype field for %s (%s) isn't filled yet!", self.name, target, userobj.nick)
            otype = 'IRC Operator'

        if not otype:
            raise AssertionError('Tried to send an empty OPERTYPE!')
        else:
            log.debug('(%s) Sending OPERTYPE from %s to oper them up.', self.name, target)
            userobj.opertype = otype
            if self.remote_proto_ver < 1205:
                otype = otype.replace(' ', '_')
            else:
                otype = ':' + otype
        self._send_with_prefix(target, 'OPERTYPE %s' % otype)

    def mode(self, numeric, target, modes, ts=None):
        """Sends mode changes from a PyLink client/server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        else:
            if ('+o', None) in modes:
                if not self.is_channel(target):
                    self._oper_up(target)
            self.apply_modes(target, modes)
            joinedmodes = self.join_modes(modes)
            if self.is_channel(target):
                ts = ts or self._channels[target].ts
                self._send_with_prefix(numeric, 'FMODE %s %s %s' % (target, ts, joinedmodes))
            else:
                self._send_with_prefix(numeric, 'MODE %s %s' % (target, joinedmodes))

    def kill(self, numeric, target, reason):
        """Sends a kill from a PyLink client/server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        else:
            if numeric in self.servers:
                sourcenick = self.servers[numeric].name
            else:
                sourcenick = self.users[numeric].nick
        self._send_with_prefix(numeric, 'KILL %s :Killed (%s (%s))' % (target, sourcenick, reason))
        self._remove_client(target)

    def topic(self, source, target, text):
        if not self.is_internal_client(source):
            raise LookupError('No such PyLink client exists.')
        else:
            if self.proto_ver >= 1205:
                self._send_with_prefix(source, 'FTOPIC %s %s %s :%s' % (target, self._channels[target].ts, int(time.time()), text))
            else:
                return super().topic(source, target, text)

    def topic_burst(self, source, target, text):
        """Sends a topic change from a PyLink server. This is usually used on burst."""
        if not self.is_internal_server(source):
            raise LookupError('No such PyLink server exists.')
        else:
            topic_ts = int(time.time())
            servername = self.servers[source].name
            if self.proto_ver >= 1205:
                self._send_with_prefix(source, 'FTOPIC %s %s %s %s :%s' % (target, self._channels[target].ts, topic_ts, servername, text))
            else:
                self._send_with_prefix(source, 'FTOPIC %s %s %s :%s' % (target, topic_ts, servername, text))
        self._channels[target].topic = text
        self._channels[target].topicset = True

    def knock(self, numeric, target, text):
        """Sends a KNOCK from a PyLink client."""
        if not self.is_internal_client(numeric):
            raise LookupError('No such PyLink client exists.')
        self._send_with_prefix(numeric, 'ENCAP * KNOCK %s :%s' % (target, text))

    def update_client(self, target, field, text):
        """Updates the ident, host, or realname of any connected client."""
        field = field.upper()
        if field not in ('IDENT', 'HOST', 'REALNAME', 'GECOS'):
            raise NotImplementedError('Changing field %r of a client is unsupported by this protocol.' % field)
        if self.is_internal_client(target):
            if field == 'IDENT':
                self.users[target].ident = text
                self._send_with_prefix(target, 'FIDENT %s' % text)
            else:
                if field == 'HOST':
                    self.users[target].host = text
                    self._send_with_prefix(target, 'FHOST %s' % text)
                else:
                    if field in ('REALNAME', 'GECOS'):
                        self.users[target].realname = text
                        self._send_with_prefix(target, 'FNAME :%s' % text)
        else:
            if field == 'IDENT':
                if 'm_chgident.so' not in self._modsupport:
                    raise NotImplementedError('Cannot change idents as m_chgident.so is not loaded')
                self.users[target].ident = text
                self._send_with_prefix(self.sid, 'CHGIDENT %s %s' % (target, text))
                self.call_hooks([self.sid, 'CHGIDENT',
                 {'target':target, 
                  'newident':text}])
            else:
                if field == 'HOST':
                    if 'm_chghost.so' not in self._modsupport:
                        raise NotImplementedError('Cannot change hosts as m_chghost.so is not loaded')
                    self.users[target].host = text
                    self._send_with_prefix(self.sid, 'CHGHOST %s %s' % (target, text))
                    self.call_hooks([self.sid, 'CHGHOST',
                     {'target':target, 
                      'newhost':text}])
                elif field in ('REALNAME', 'GECOS'):
                    if 'm_chgname.so' not in self._modsupport:
                        raise NotImplementedError('Cannot change real names as m_chgname.so is not loaded')
                    self.users[target].realname = text
                    self._send_with_prefix(self.sid, 'CHGNAME %s :%s' % (target, text))
                    self.call_hooks([self.sid, 'CHGNAME',
                     {'target':target, 
                      'newgecos':text}])

    def numeric(self, source, numeric, target, text):
        """Sends raw numerics from a server to a remote client."""
        if self.proto_ver >= 1205:
            self._send('NUM %s %s %s %s' % (source, target, numeric, text))
        else:
            self._send_with_prefix(self.sid, 'PUSH %s ::%s %s %s %s' % (target, source, numeric, target, text))

    def invite(self, source, target, channel):
        """Sends an INVITE from a PyLink client."""
        if not self.is_internal_client(source):
            raise LookupError('No such PyLink client exists.')
        else:
            if self.proto_ver >= 1205:
                self._send_with_prefix(source, 'INVITE %s %s %d' % (target, channel, self._channels[channel].ts))
            else:
                self._send_with_prefix(source, 'INVITE %s %s' % (target, channel))

    def away(self, source, text):
        """Sends an AWAY message from a PyLink client. <text> can be an empty string
        to unset AWAY status."""
        if text:
            self._send_with_prefix(source, 'AWAY %s :%s' % (int(time.time()), text))
        else:
            self._send_with_prefix(source, 'AWAY')
        self.users[source].away = text

    def spawn_server(self, name, sid=None, uplink=None, desc=None):
        """
        Spawns a server off a PyLink server. desc (server description)
        defaults to the one in the config. uplink defaults to the main PyLink
        server, and sid (the server ID) is automatically generated if not
        given.

        Endburst delay can be tweaked by setting the _endburst_delay variable
        to a positive value before calling spawn_server(). This can be used to
        prevent PyLink bursts from filling up snomasks and triggering InspIRCd +j.
        """
        uplink = uplink or self.sid
        name = name.lower()
        desc = desc or self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']
        if sid is None:
            sid = self.sidgen.next_sid()
        elif not len(sid) == 3:
            raise AssertionError('Incorrect SID length')
        if sid in self.servers:
            raise ValueError('A server with SID %r already exists!' % sid)
        for server in self.servers.values():
            if name == server.name:
                raise ValueError('A server named %r already exists!' % name)

        if not self.is_internal_server(uplink):
            raise ValueError('Server %r is not a PyLink server!' % uplink)
        else:
            if not self.is_server_name(name):
                raise ValueError('Invalid server name %r' % name)
            else:
                self.servers[sid] = Server(self, uplink, name, internal=True, desc=desc)
                if self.proto_ver >= 1205:
                    self._send_with_prefix(uplink, 'SERVER %s %s :%s' % (name, sid, desc))
                else:
                    self._send_with_prefix(uplink, 'SERVER %s * %s %s :%s' % (name, self.servers[sid].hopcount, sid, desc))

            def endburstf():
                if self._aborted.wait(self._endburst_delay):
                    log.debug('(%s) stopping endburstf() for %s as aborted was set', self.name, sid)
                    return
                self._send_with_prefix(sid, 'ENDBURST')

            if self._endburst_delay:
                t = threading.Thread(target=endburstf, name=('protocols/inspircd delayed ENDBURST thread for %s@%s' % (sid, self.name)))
                t.daemon = True
                t.start()
            else:
                self._send_with_prefix(sid, 'ENDBURST')
        return sid

    def set_server_ban(self, source, duration, user='*', host='*', reason='User banned'):
        """
        Sets a server ban.
        """
        assert not user == host == '*', 'Refusing to set ridiculous ban on *@*'
        self._send_with_prefix(source, 'ADDLINE G %s@%s %s %s %s :%s' % (user, host, self.get_friendly_name(source)[:64],
         int(time.time()), duration, reason))

    def _post_disconnect(self):
        super()._post_disconnect()
        log.debug('(%s) _post_disconnect: clearing _modsupport entries. Last: %s', self.name, self._modsupport)
        self._modsupport.clear()

    def post_connect(self):
        """Initializes a connection to a server."""
        ts = self.start_ts
        f = self.send
        f('CAPAB START %s' % self.proto_ver)
        f('CAPAB CAPABILITIES :PROTOCOL=%s' % self.proto_ver)
        f('CAPAB END')
        host = self.serverdata['hostname']
        f('SERVER {host} {Pass} 0 {sid} :{sdesc}'.format(host=host, Pass=(self.serverdata['sendpass']),
          sid=(self.sid),
          sdesc=(self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc'])))
        self._send_with_prefix(self.sid, 'BURST %s' % ts)
        if self.proto_ver >= 1205:
            verstr = self.version()
            for version_type in {'version', 'rawversion'}:
                self._send_with_prefix(self.sid, 'SINFO %s :%s' % (version_type, verstr.split(' ', 1)[0]))

            self._send_with_prefix(self.sid, 'SINFO fullversion :%s' % verstr)
        else:
            self._send_with_prefix(self.sid, 'VERSION :%s' % self.version())
        self._send_with_prefix(self.sid, 'ENDBURST')
        self.extbans_acting = {'quiet':'m:', 
         'ban_nonick':'N:',  'ban_blockcolor':'c:',  'ban_partmsgs':'p:', 
         'ban_invites':'A:',  'ban_blockcaps':'B:',  'ban_noctcp':'C:', 
         'ban_nokicks':'Q:',  'ban_stripcolor':'S:',  'ban_nonotice':'T:'}
        self.extbans_matching = {'ban_inchannel':'j:',  'ban_realname':'r:',  'ban_server':'s:',  'ban_certfp':'z:', 
         'ban_opertype':'O:',  'ban_account':'R:',  'ban_unregistered_matching':'U:'}

    def handle_capab--- This code section failed: ---

 L. 498         0  LOAD_FAST                'args'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  LOAD_STR                 'START'
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE   208  'to 208'

 L. 504        12  LOAD_GLOBAL              int
               14  LOAD_FAST                'args'
               16  LOAD_CONST               1
               18  BINARY_SUBSCR    
               20  CALL_FUNCTION_1       1  ''
               22  DUP_TOP          
               24  LOAD_FAST                'self'
               26  STORE_ATTR               remote_proto_ver
               28  STORE_FAST               'protocol_version'

 L. 506        30  LOAD_GLOBAL              log
               32  LOAD_ATTR                debug
               34  LOAD_STR                 '(%s) handle_capab: got remote protocol version %s'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                name
               40  LOAD_FAST                'protocol_version'
               42  CALL_FUNCTION_3       3  ''
               44  POP_TOP          

 L. 507        46  LOAD_FAST                'protocol_version'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                proto_ver
               52  COMPARE_OP               <
               54  POP_JUMP_IF_FALSE    76  'to 76'

 L. 508        56  LOAD_GLOBAL              ProtocolError
               58  LOAD_STR                 'Remote protocol version is too old! At least %s is needed. (got %s)'

 L. 510        60  LOAD_FAST                'self'
               62  LOAD_ATTR                proto_ver
               64  LOAD_FAST                'protocol_version'
               66  BUILD_TUPLE_2         2 
               68  BINARY_MODULO    
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  ''
               74  JUMP_FORWARD        156  'to 156'
               76  ELSE                     '156'

 L. 511        76  LOAD_FAST                'protocol_version'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                MAX_PROTO_VER
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 512        86  LOAD_GLOBAL              log
               88  LOAD_ATTR                warning
               90  LOAD_STR                 '(%s) PyLink support for InspIRCd > 3.x is experimental, and should not be relied upon for anything important.'

 L. 514        92  LOAD_FAST                'self'
               94  LOAD_ATTR                name
               96  CALL_FUNCTION_2       2  ''
               98  POP_TOP          
              100  JUMP_FORWARD        156  'to 156'
              102  ELSE                     '156'

 L. 515       102  LOAD_FAST                'protocol_version'
              104  LOAD_CONST               1205
              106  DUP_TOP          
              108  ROT_THREE        
              110  COMPARE_OP               >=
              112  JUMP_IF_FALSE_OR_POP   122  'to 122'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                proto_ver
              118  COMPARE_OP               >
              120  JUMP_FORWARD        126  'to 126'
            122_0  COME_FROM           112  '112'
              122  ROT_TWO          
              124  POP_TOP          
            126_0  COME_FROM           120  '120'
              126  POP_JUMP_IF_FALSE   156  'to 156'

 L. 516       128  LOAD_GLOBAL              log
              130  LOAD_ATTR                warning
              132  LOAD_STR                 "(%s) PyLink 3.0 introduces native support for InspIRCd 3. You should enable this by setting the 'target_version' option in your InspIRCd server block to 'insp3'. Otherwise, some features will not work correctly!"

 L. 519       134  LOAD_FAST                'self'
              136  LOAD_ATTR                name
              138  CALL_FUNCTION_2       2  ''
              140  POP_TOP          

 L. 520       142  LOAD_GLOBAL              log
              144  LOAD_ATTR                warning
              146  LOAD_STR                 '(%s) Falling back to InspIRCd 2.0 (compatibility) mode.'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                name
              152  CALL_FUNCTION_2       2  ''
              154  POP_TOP          
            156_0  COME_FROM           126  '126'
            156_1  COME_FROM           100  '100'
            156_2  COME_FROM            74  '74'

 L. 522       156  LOAD_FAST                'self'
              158  LOAD_ATTR                proto_ver
              160  LOAD_CONST               1205
              162  COMPARE_OP               >=
              164  POP_JUMP_IF_FALSE   208  'to 208'

 L. 524       166  LOAD_STR                 ''
              168  LOAD_STR                 ''
              170  LOAD_STR                 ''
              172  LOAD_STR                 ''
              174  LOAD_CONST               ('*A', '*B', '*C', '*D')
              176  BUILD_CONST_KEY_MAP_4     4 
              178  LOAD_FAST                'self'
              180  STORE_ATTR               cmodes

 L. 525       182  LOAD_STR                 ''
              184  LOAD_STR                 ''
              186  LOAD_STR                 ''
              188  LOAD_STR                 ''
              190  LOAD_CONST               ('*A', '*B', '*C', '*D')
              192  BUILD_CONST_KEY_MAP_4     4 
              194  LOAD_FAST                'self'
              196  STORE_ATTR               umodes

 L. 526       198  LOAD_FAST                'self'
              200  LOAD_ATTR                prefixmodes
              202  LOAD_ATTR                clear
              204  CALL_FUNCTION_0       0  ''
              206  POP_TOP          
            208_0  COME_FROM           164  '164'
            208_1  COME_FROM            10  '10'

 L. 528       208  LOAD_FAST                'args'
              210  LOAD_CONST               0
              212  BINARY_SUBSCR    
              214  LOAD_CONST               {'CHANMODES', 'USERMODES'}
              216  COMPARE_OP               in
              218  POP_JUMP_IF_FALSE   618  'to 618'

 L. 558       222  LOAD_FAST                'args'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  LOAD_STR                 'CHANMODES'
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   240  'to 240'
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                cmodes
              238  JUMP_FORWARD        244  'to 244'
              240  ELSE                     '244'
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                umodes
            244_0  COME_FROM           238  '238'
              244  STORE_FAST               'mydict'

 L. 563       246  SETUP_LOOP          958  'to 958'
              250  LOAD_FAST                'args'
              252  LOAD_CONST               -1
              254  BINARY_SUBSCR    
              256  LOAD_ATTR                split
              258  CALL_FUNCTION_0       0  ''
              260  GET_ITER         
              262  FOR_ITER            612  'to 612'
              266  STORE_FAST               'modepair'

 L. 564       268  LOAD_FAST                'modepair'
              270  LOAD_ATTR                rsplit
              272  LOAD_STR                 '='
              274  LOAD_CONST               1
              276  CALL_FUNCTION_2       2  ''
              278  UNPACK_SEQUENCE_2     2 
              280  STORE_FAST               'name'
              282  STORE_FAST               'char'

 L. 566       284  LOAD_FAST                'self'
              286  LOAD_ATTR                proto_ver
              288  LOAD_CONST               1205
              290  COMPARE_OP               >=
              292  POP_JUMP_IF_FALSE   512  'to 512'

 L. 568       296  LOAD_FAST                'name'
              298  LOAD_ATTR                split
              300  LOAD_STR                 ':'
              302  CALL_FUNCTION_1       1  ''
              304  STORE_FAST               'parts'

 L. 569       306  LOAD_FAST                'parts'
              308  LOAD_CONST               0
              310  BINARY_SUBSCR    
              312  STORE_FAST               'modetype'

 L. 570       314  LOAD_FAST                'parts'
              316  LOAD_CONST               -1
              318  BINARY_SUBSCR    
              320  STORE_FAST               'name'

 L. 574       322  LOAD_FAST                'modetype'
              324  LOAD_STR                 'simple'
              326  COMPARE_OP               ==
              328  POP_JUMP_IF_FALSE   350  'to 350'

 L. 575       332  LOAD_FAST                'mydict'
              334  LOAD_STR                 '*D'
              336  DUP_TOP_TWO      
              338  BINARY_SUBSCR    
              340  LOAD_FAST                'char'
              342  INPLACE_ADD      
              344  ROT_THREE        
              346  STORE_SUBSCR     
              348  JUMP_FORWARD        512  'to 512'
              350  ELSE                     '512'

 L. 576       350  LOAD_FAST                'modetype'
              352  LOAD_STR                 'param-set'
              354  COMPARE_OP               ==
              356  POP_JUMP_IF_FALSE   378  'to 378'

 L. 577       360  LOAD_FAST                'mydict'
              362  LOAD_STR                 '*C'
              364  DUP_TOP_TWO      
              366  BINARY_SUBSCR    
              368  LOAD_FAST                'char'
              370  INPLACE_ADD      
              372  ROT_THREE        
              374  STORE_SUBSCR     
              376  JUMP_FORWARD        512  'to 512'
              378  ELSE                     '512'

 L. 578       378  LOAD_FAST                'modetype'
              380  LOAD_STR                 'param'
              382  COMPARE_OP               ==
              384  POP_JUMP_IF_FALSE   406  'to 406'

 L. 579       388  LOAD_FAST                'mydict'
              390  LOAD_STR                 '*B'
              392  DUP_TOP_TWO      
              394  BINARY_SUBSCR    
              396  LOAD_FAST                'char'
              398  INPLACE_ADD      
              400  ROT_THREE        
              402  STORE_SUBSCR     
              404  JUMP_FORWARD        512  'to 512'
              406  ELSE                     '512'

 L. 580       406  LOAD_FAST                'modetype'
              408  LOAD_STR                 'list'
              410  COMPARE_OP               ==
              412  POP_JUMP_IF_FALSE   434  'to 434'

 L. 581       416  LOAD_FAST                'mydict'
              418  LOAD_STR                 '*A'
              420  DUP_TOP_TWO      
              422  BINARY_SUBSCR    
              424  LOAD_FAST                'char'
              426  INPLACE_ADD      
              428  ROT_THREE        
              430  STORE_SUBSCR     
              432  JUMP_FORWARD        512  'to 512'
              434  ELSE                     '512'

 L. 582       434  LOAD_FAST                'modetype'
              436  LOAD_STR                 'prefix'
              438  COMPARE_OP               ==
              440  POP_JUMP_IF_FALSE   512  'to 512'

 L. 583       444  LOAD_FAST                'args'
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    
              450  LOAD_STR                 'CHANMODES'
              452  COMPARE_OP               !=
              454  POP_JUMP_IF_FALSE   476  'to 476'

 L. 584       458  LOAD_GLOBAL              log
              460  LOAD_ATTR                warning
              462  LOAD_STR                 '(%s) Possible desync? Got a prefix type modepair %r but not for channel modes'
              464  LOAD_FAST                'self'
              466  LOAD_ATTR                name
              468  LOAD_FAST                'modepair'
              470  CALL_FUNCTION_3       3  ''
              472  POP_TOP          
              474  JUMP_FORWARD        512  'to 512'
              476  ELSE                     '512'

 L. 587       476  LOAD_GLOBAL              int
              478  LOAD_FAST                'parts'
              480  LOAD_CONST               1
              482  BINARY_SUBSCR    
              484  CALL_FUNCTION_1       1  ''
              486  LOAD_FAST                'self'
              488  LOAD_ATTR                _prefix_levels
              490  LOAD_FAST                'name'
              492  STORE_SUBSCR     

 L. 590       494  LOAD_FAST                'char'
              496  LOAD_CONST               0
              498  BINARY_SUBSCR    
              500  LOAD_FAST                'self'
              502  LOAD_ATTR                prefixmodes
              504  LOAD_FAST                'char'
              506  LOAD_CONST               -1
              508  BINARY_SUBSCR    
              510  STORE_SUBSCR     
            512_0  COME_FROM           474  '474'
            512_1  COME_FROM           440  '440'
            512_2  COME_FROM           432  '432'
            512_3  COME_FROM           404  '404'
            512_4  COME_FROM           376  '376'
            512_5  COME_FROM           348  '348'
            512_6  COME_FROM           292  '292'

 L. 593       512  LOAD_FAST                'name'
              514  LOAD_ATTR                startswith
              516  LOAD_CONST               ('c_', 'u_')
              518  CALL_FUNCTION_1       1  ''
              520  POP_JUMP_IF_FALSE   536  'to 536'

 L. 594       524  LOAD_FAST                'name'
              526  LOAD_CONST               2
              528  LOAD_CONST               None
              530  BUILD_SLICE_2         2 
              532  BINARY_SUBSCR    
              534  STORE_FAST               'name'
            536_0  COME_FROM           520  '520'

 L. 596       536  LOAD_FAST                'name'
              538  LOAD_STR                 'reginvite'
              540  COMPARE_OP               ==
              542  POP_JUMP_IF_FALSE   550  'to 550'

 L. 597       546  LOAD_STR                 'regonly'
              548  STORE_FAST               'name'
            550_0  COME_FROM           542  '542'

 L. 599       550  LOAD_FAST                'name'
              552  LOAD_STR                 'antiredirect'
              554  COMPARE_OP               ==
              556  POP_JUMP_IF_FALSE   564  'to 564'

 L. 600       560  LOAD_STR                 'noforward'
              562  STORE_FAST               'name'
            564_0  COME_FROM           556  '556'

 L. 602       564  LOAD_FAST                'name'
              566  LOAD_STR                 'founder'
              568  COMPARE_OP               ==
              570  POP_JUMP_IF_FALSE   578  'to 578'

 L. 605       574  LOAD_STR                 'owner'
              576  STORE_FAST               'name'
            578_0  COME_FROM           570  '570'

 L. 607       578  LOAD_FAST                'name'
              580  LOAD_CONST               ('repeat', 'kicknorejoin')
              582  COMPARE_OP               in
              584  POP_JUMP_IF_FALSE   596  'to 596'

 L. 610       588  LOAD_FAST                'name'
              590  LOAD_STR                 '_insp'
              592  INPLACE_ADD      
              594  STORE_FAST               'name'
            596_0  COME_FROM           584  '584'

 L. 613       596  LOAD_FAST                'char'
              598  LOAD_CONST               -1
              600  BINARY_SUBSCR    
              602  LOAD_FAST                'mydict'
              604  LOAD_FAST                'name'
              606  STORE_SUBSCR     
              608  JUMP_BACK           262  'to 262'
              612  POP_BLOCK        
              614  JUMP_FORWARD        958  'to 958'
              618  ELSE                     '958'

 L. 615       618  LOAD_FAST                'args'
              620  LOAD_CONST               0
              622  BINARY_SUBSCR    
              624  LOAD_STR                 'CAPABILITIES'
              626  COMPARE_OP               ==
              628  POP_JUMP_IF_FALSE   918  'to 918'

 L. 628       632  LOAD_FAST                'self'
              634  LOAD_ATTR                parse_isupport
              636  LOAD_FAST                'args'
              638  LOAD_CONST               -1
              640  BINARY_SUBSCR    
              642  CALL_FUNCTION_1       1  ''
              644  STORE_FAST               'caps'

 L. 629       646  LOAD_GLOBAL              log
              648  LOAD_ATTR                debug
              650  LOAD_STR                 '(%s) handle_capab: capabilities list is %s'
              652  LOAD_FAST                'self'
              654  LOAD_ATTR                name
              656  LOAD_FAST                'caps'
              658  CALL_FUNCTION_3       3  ''
              660  POP_TOP          

 L. 632       662  LOAD_STR                 'NICKMAX'
              664  LOAD_FAST                'caps'
              666  COMPARE_OP               in
              668  POP_JUMP_IF_FALSE   686  'to 686'

 L. 633       672  LOAD_GLOBAL              int
              674  LOAD_FAST                'caps'
              676  LOAD_STR                 'NICKMAX'
              678  BINARY_SUBSCR    
              680  CALL_FUNCTION_1       1  ''
              682  LOAD_FAST                'self'
              684  STORE_ATTR               maxnicklen
            686_0  COME_FROM           668  '668'

 L. 634       686  LOAD_STR                 'CHANMAX'
              688  LOAD_FAST                'caps'
              690  COMPARE_OP               in
              692  POP_JUMP_IF_FALSE   710  'to 710'

 L. 635       696  LOAD_GLOBAL              int
              698  LOAD_FAST                'caps'
              700  LOAD_STR                 'CHANMAX'
              702  BINARY_SUBSCR    
              704  CALL_FUNCTION_1       1  ''
              706  LOAD_FAST                'self'
              708  STORE_ATTR               maxchanlen
            710_0  COME_FROM           692  '692'

 L. 637       710  LOAD_STR                 'CASEMAPPING'
              712  LOAD_FAST                'caps'
              714  COMPARE_OP               in
              716  POP_JUMP_IF_FALSE   748  'to 748'

 L. 638       720  LOAD_FAST                'caps'
              722  LOAD_STR                 'CASEMAPPING'
              724  BINARY_SUBSCR    
              726  LOAD_FAST                'self'
              728  STORE_ATTR               casemapping

 L. 639       730  LOAD_GLOBAL              log
              732  LOAD_ATTR                debug
              734  LOAD_STR                 '(%s) handle_capab: updated casemapping to %s'
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                name
              740  LOAD_FAST                'self'
              742  LOAD_ATTR                casemapping
              744  CALL_FUNCTION_3       3  ''
              746  POP_TOP          
            748_0  COME_FROM           716  '716'

 L. 642       748  LOAD_FAST                'self'
              750  LOAD_ATTR                proto_ver
              752  LOAD_CONST               1205
              754  COMPARE_OP               <
              756  POP_JUMP_IF_FALSE   958  'to 958'

 L. 643       760  LOAD_STR                 'CHANMODES'
              762  LOAD_FAST                'caps'
              764  COMPARE_OP               in
              766  POP_JUMP_IF_FALSE   816  'to 816'

 L. 645       770  LOAD_FAST                'caps'
              772  LOAD_STR                 'CHANMODES'
              774  BINARY_SUBSCR    
              776  LOAD_ATTR                split
              778  LOAD_STR                 ','
              780  CALL_FUNCTION_1       1  ''
              782  UNPACK_SEQUENCE_4     4 
              784  LOAD_FAST                'self'
              786  LOAD_ATTR                cmodes
              788  LOAD_STR                 '*A'
              790  STORE_SUBSCR     
              792  LOAD_FAST                'self'
              794  LOAD_ATTR                cmodes
              796  LOAD_STR                 '*B'
              798  STORE_SUBSCR     
              800  LOAD_FAST                'self'
              802  LOAD_ATTR                cmodes
              804  LOAD_STR                 '*C'
              806  STORE_SUBSCR     
              808  LOAD_FAST                'self'
              810  LOAD_ATTR                cmodes
              812  LOAD_STR                 '*D'
              814  STORE_SUBSCR     
            816_0  COME_FROM           766  '766'

 L. 646       816  LOAD_STR                 'USERMODES'
              818  LOAD_FAST                'caps'
              820  COMPARE_OP               in
              822  POP_JUMP_IF_FALSE   872  'to 872'

 L. 648       826  LOAD_FAST                'caps'
              828  LOAD_STR                 'USERMODES'
              830  BINARY_SUBSCR    
              832  LOAD_ATTR                split
              834  LOAD_STR                 ','
              836  CALL_FUNCTION_1       1  ''
              838  UNPACK_SEQUENCE_4     4 
              840  LOAD_FAST                'self'
              842  LOAD_ATTR                umodes
              844  LOAD_STR                 '*A'
              846  STORE_SUBSCR     
              848  LOAD_FAST                'self'
              850  LOAD_ATTR                umodes
              852  LOAD_STR                 '*B'
              854  STORE_SUBSCR     
              856  LOAD_FAST                'self'
              858  LOAD_ATTR                umodes
              860  LOAD_STR                 '*C'
              862  STORE_SUBSCR     
              864  LOAD_FAST                'self'
              866  LOAD_ATTR                umodes
              868  LOAD_STR                 '*D'
              870  STORE_SUBSCR     
            872_0  COME_FROM           822  '822'

 L. 649       872  LOAD_STR                 'PREFIX'
              874  LOAD_FAST                'caps'
              876  COMPARE_OP               in
              878  POP_JUMP_IF_FALSE   958  'to 958'

 L. 652       882  LOAD_FAST                'self'
              884  LOAD_ATTR                parse_isupport_prefixes
              886  LOAD_FAST                'caps'
              888  LOAD_STR                 'PREFIX'
              890  BINARY_SUBSCR    
              892  CALL_FUNCTION_1       1  ''
              894  LOAD_FAST                'self'
              896  STORE_ATTR               prefixmodes

 L. 653       898  LOAD_GLOBAL              log
              900  LOAD_ATTR                debug
              902  LOAD_STR                 '(%s) handle_capab: self.prefixmodes set to %r'
              904  LOAD_FAST                'self'
              906  LOAD_ATTR                name

 L. 654       908  LOAD_FAST                'self'
              910  LOAD_ATTR                prefixmodes
              912  CALL_FUNCTION_3       3  ''
              914  POP_TOP          
              916  JUMP_FORWARD        958  'to 958'
              918  ELSE                     '958'

 L. 656       918  LOAD_FAST                'args'
              920  LOAD_CONST               0
              922  BINARY_SUBSCR    
              924  LOAD_STR                 'MODSUPPORT'
              926  COMPARE_OP               ==
              928  POP_JUMP_IF_FALSE   958  'to 958'

 L. 658       932  LOAD_FAST                'self'
              934  DUP_TOP          
              936  LOAD_ATTR                _modsupport
              938  LOAD_GLOBAL              set
              940  LOAD_FAST                'args'
              942  LOAD_CONST               -1
              944  BINARY_SUBSCR    
              946  LOAD_ATTR                split
              948  CALL_FUNCTION_0       0  ''
              950  CALL_FUNCTION_1       1  ''
              952  INPLACE_OR       
              954  ROT_TWO          
              956  STORE_ATTR               _modsupport
            958_0  COME_FROM           928  '928'
            958_1  COME_FROM           916  '916'
            958_2  COME_FROM           878  '878'
            958_3  COME_FROM           756  '756'
            958_4  COME_FROM           614  '614'

Parse error at or near `JUMP_FORWARD' instruction at offset 614

    def handle_kick(self, source, command, args):
        if self.proto_ver >= 1205:
            if len(args) > 3:
                del args[2]
        return super().handle_kick(source, command, args)

    def handle_ping(self, source, command, args):
        """Handles incoming PING commands, so we don't time out."""
        if len(args) >= 2:
            self._send_with_prefix((args[1]), ('PONG %s %s' % (args[1], source)), queue=False)
        else:
            self._send_with_prefix((args[0]), ('PONG %s' % source), queue=False)

    def handle_fjoin(self, servernumeric, command, args):
        """Handles incoming FJOIN commands (InspIRCd equivalent of JOIN/SJOIN)."""
        channel = args[0]
        chandata = self._channels[channel].deepcopy()
        userlist = args[(-1)].split()
        modestring = args[2:-1] or args[2]
        parsedmodes = self.parse_modes(channel, modestring)
        namelist = []
        changedmodes = set(parsedmodes)
        for user in userlist:
            modeprefix, user = user.split(',', 1)
            if self.proto_ver >= 1205:
                user = user.split(':', 1)[0]
            if user not in self.users:
                log.debug('(%s) handle_fjoin: tried to introduce user %s not in our user list, ignoring...', self.name, user)
            else:
                namelist.append(user)
                self.users[user].channels.add(channel)
                changedmodes |= {('+%s' % mode, user) for mode in modeprefix}
                self._channels[channel].users.add(user)

        their_ts = int(''.join(char for char in args[1] if char.isdigit()))
        our_ts = self._channels[channel].ts
        self.updateTS(servernumeric, channel, their_ts, changedmodes)
        return {'channel':channel, 
         'users':namelist,  'modes':parsedmodes,  'ts':their_ts,  'channeldata':chandata}

    def handle_ijoin(self, source, command, args):
        """Handles InspIRCd 3 joins with membership ID."""
        channel = args[0]
        self.users[source].channels.add(channel)
        self._channels[channel].users.add(source)
        if len(args) >= 4:
            if int(args[2]) <= self._channels[channel].ts:
                self.apply_modes(source, {('+%s' % mode, source) for mode in args[3]})
        return {'channel':channel,  'users':[source],  'modes':self._channels[channel].modes}

    def handle_uid(self, numeric, command, args):
        """Handles incoming UID commands (user introduction)."""
        uid, ts, nick, realhost, host, ident, ip = args[0:7]
        ts = int(ts)
        self._check_nick_collision(nick)
        realname = args[(-1)]
        self.users[uid] = userobj = User(self, nick, ts, uid, numeric, ident, host, realname, realhost, ip)
        parsedmodes = self.parse_modes(uid, [args[8], args[9]])
        self.apply_modes(uid, parsedmodes)
        self._check_oper_status_change(uid, parsedmodes)
        self.servers[numeric].users.add(uid)
        return {'uid':uid, 
         'ts':ts,  'nick':nick,  'realhost':realhost,  'host':host,  'ident':ident,  'ip':ip}

    def handle_server(self, source, command, args):
        """Handles incoming SERVER commands (introduction of servers)."""
        if self.uplink is None:
            servername = args[0].lower()
            source = args[3]
            if args[1] != self.serverdata['recvpass']:
                raise ProtocolError('recvpass from uplink server %s does not match configuration!' % servername)
            sdesc = args[(-1)]
            self.servers[source] = Server(self, None, servername, desc=sdesc)
            self.uplink = source
            log.debug('(%s) inspircd: found uplink %s', self.name, self.uplink)
            return
        else:
            servername = args[0].lower()
            if self.proto_ver >= 1205:
                sid = args[1]
            else:
                sid = args[3]
            sdesc = args[(-1)]
            self.servers[sid] = Server(self, source, servername, desc=sdesc)
            return {'name':servername, 
             'sid':sid,  'text':sdesc}

    def handle_fmode(self, numeric, command, args):
        """Handles the FMODE command, used for channel mode changes."""
        channel = args[0]
        oldobj = self._channels[channel].deepcopy()
        modes = args[2:]
        changedmodes = self.parse_modes(channel, modes)
        self.apply_modes(channel, changedmodes)
        ts = int(args[1])
        return {'target':channel, 
         'modes':changedmodes,  'ts':ts,  'channeldata':oldobj}

    def handle_idle(self, source, command, args):
        """
        Handles the IDLE command, sent between servers in remote WHOIS queries.
        """
        if self.serverdata.get('force_whois_extensions', True):
            return {'target':args[0],  'parse_as':'WHOIS'}
        target = args[0]
        start_time = self.start_ts if (conf.conf['pylink'].get('whois_show_startup_time', True) and self.get_service_bot(target)) else 0
        self._send_with_prefix(target, 'IDLE %s %s 0' % (source, start_time))

    def handle_ftopic(self, source, command, args):
        """Handles incoming topic changes."""
        channel = args[0]
        if self.proto_ver >= 1205:
            if command == 'FTOPIC':
                ts = args[2]
                if source in self.users:
                    setter = source
                else:
                    setter = args[3]
        else:
            ts = args[1]
            setter = args[2]
        ts = int(ts)
        topic = args[(-1)]
        self._channels[channel].topic = topic
        self._channels[channel].topicset = True
        return {'channel':channel, 
         'setter':setter,  'ts':ts,  'text':topic}

    handle_svstopic = handle_ftopic

    def handle_opertype(self, target, command, args):
        """Handles incoming OPERTYPE, which is used to denote an oper up.

        This calls the internal hook CLIENT_OPERED, sets the internal
        opertype of the client, and assumes setting user mode +o on the caller."""
        opertype = args[0].replace('_', ' ')
        omode = [
         ('+o', None)]
        self.apply_modes(target, omode)
        self.call_hooks([target, 'CLIENT_OPERED', {'text': opertype}])
        return {'target':target, 
         'modes':omode}

    def handle_fident(self, numeric, command, args):
        """Handles FIDENT, used for denoting ident changes."""
        self.users[numeric].ident = newident = args[0]
        return {'target':numeric, 
         'newident':newident}

    def handle_fhost(self, numeric, command, args):
        """Handles FHOST, used for denoting hostname changes."""
        self.users[numeric].host = newhost = args[0]
        return {'target':numeric, 
         'newhost':newhost}

    def handle_fname(self, numeric, command, args):
        """Handles FNAME, used for denoting real name/gecos changes."""
        self.users[numeric].realname = newgecos = args[0]
        return {'target':numeric, 
         'newgecos':newgecos}

    def handle_endburst(self, numeric, command, args):
        """ENDBURST handler; sends a hook with empty contents."""
        self.servers[numeric].has_eob = True
        if numeric == self.uplink:
            self.connected.set()
        return {}

    def handle_away(self, numeric, command, args):
        """Handles incoming AWAY messages."""
        try:
            ts = args[0]
            self.users[numeric].away = text = args[1]
            return {'text':text, 
             'ts':ts}
        except IndexError:
            self.users[numeric].away = ''
            return {'text': ''}

    def handle_rsquit(self, numeric, command, args):
        """
        Handles the RSQUIT command, which is sent by opers to SQUIT remote
        servers.
        """
        target = self._get_SID(args[0])
        if self.is_internal_server(target):
            uplink = self.servers[target].uplink
            reason = 'Requested by %s' % self.get_hostmask(numeric)
            self._send_with_prefix(uplink, 'SQUIT %s :%s' % (target, reason))
            return self.handle_squit(numeric, 'SQUIT', [target, reason])
        log.debug("(%s) Got RSQUIT for '%s', which is either invalid or not a server of ours!", self.name, args[0])

    def handle_metadata(self, numeric, command, args):
        """
        Handles the METADATA command, used by servers to send metadata for various objects.
        """
        uid = args[0]
        if args[1] == 'accountname':
            if uid in self.users:
                self.call_hooks([uid, 'CLIENT_SERVICES_LOGIN', {'text': args[(-1)]}])
        if args[1] == 'modules':
            if numeric == self.uplink:
                for module in args[(-1)].split():
                    if module.startswith('-'):
                        log.debug('(%s) Removing module %s', self.name, module[1:])
                        self._modsupport.discard(module[1:])
                    else:
                        if module.startswith('+'):
                            log.debug('(%s) Adding module %s', self.name, module[1:])
                            self._modsupport.add(module[1:])
                        else:
                            log.warning('(%s) Got unknown METADATA modules string: %r', self.name, args[(-1)])

    def handle_version(self, numeric, command, args):
        """
        Stub VERSION handler (does nothing) to override the one in ts6_common.
        """
        pass

    def handle_sakick(self, source, command, args):
        """Handles forced kicks (SAKICK)."""
        target = args[1]
        channel = args[0]
        try:
            reason = args[2]
        except IndexError:
            reason = self.get_friendly_name(source)

        if not self.is_internal_client(target):
            log.warning('(%s) Got SAKICK for client that not one of ours: %s', self.name, target)
            return
        else:
            server = self.get_server(target)
            self.kick(server, channel, target, reason)
            return {'channel':channel, 
             'target':target,  'text':reason}

    def handle_alltime(self, source, command, args):
        """Handles /ALLTIME requests."""
        timestring = '%s (%s)' % (time.strftime('%Y-%m-%d %H:%M:%S'), int(time.time()))
        self._send_with_prefix(self.sid, 'NOTICE %s :System time is %s on %s' % (source, timestring, self.hostname()))


Class = InspIRCdProtocol
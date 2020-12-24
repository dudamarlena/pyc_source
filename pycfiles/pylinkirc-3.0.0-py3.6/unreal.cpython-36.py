# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/unreal.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 46383 bytes
"""
unreal.py: UnrealIRCd 4.x-5.x protocol module for PyLink.
"""
import codecs, re, socket, time
from pylinkirc import conf, utils
from pylinkirc.classes import *
from pylinkirc.log import log
from pylinkirc.protocols.ts6_common import *
SJOIN_PREFIXES = {'q':'*', 
 'a':'~',  'o':'@',  'h':'%',  'v':'+',  'b':'&',  'e':'"',  'I':"'"}

class UnrealProtocol(TS6BaseProtocol):
    S2S_BUFSIZE = 427
    _KNOWN_CMODES = {'ban':'b',  'banexception':'e', 
     'blockcolor':'c', 
     'censor':'G', 
     'delayjoin':'D', 
     'flood_unreal':'f', 
     'invex':'I', 
     'inviteonly':'i', 
     'issecure':'Z', 
     'key':'k', 
     'limit':'l', 
     'moderated':'m', 
     'noctcp':'C', 
     'noextmsg':'n', 
     'noinvite':'V', 
     'nokick':'Q', 
     'noknock':'K', 
     'nonick':'N', 
     'nonotice':'T', 
     'op':'o', 
     'operonly':'O', 
     'permanent':'P', 
     'private':'p', 
     'registered':'r', 
     'regmoderated':'M', 
     'regonly':'R', 
     'secret':'s', 
     'sslonly':'z', 
     'stripcolor':'S', 
     'topiclock':'t', 
     'voice':'v'}
    _KNOWN_UMODES = {'bot':'B',  'censor':'G', 
     'cloak':'x', 
     'deaf':'d', 
     'filter':'G', 
     'hidechans':'p', 
     'hideidle':'I', 
     'hideoper':'H', 
     'invisible':'i', 
     'noctcp':'T', 
     'protected':'q', 
     'regdeaf':'R', 
     'registered':'r', 
     'sslonlymsg':'Z', 
     'servprotect':'S', 
     'showwhois':'W', 
     'snomask':'s', 
     'ssl':'z', 
     'vhost':'t', 
     'wallops':'w'}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.protocol_caps |= {'slash-in-nicks', 'underscore-in-hosts', 'slash-in-hosts'}
        self.casemapping = 'ascii'
        self.proto_ver = 4203
        self.min_proto_ver = 4000
        self.hook_map = {'UMODE2':'MODE', 
         'SVSKILL':'KILL',  'SVSMODE':'MODE',  'SVS2MODE':'MODE', 
         'SJOIN':'JOIN',  'SETHOST':'CHGHOST',  'SETIDENT':'CHGIDENT', 
         'SETNAME':'CHGNAME',  'EOS':'ENDBURST'}
        self.caps = []
        self.prefixmodes = {'q':'~', 
         'a':'&',  'o':'@',  'h':'%',  'v':'+'}
        self.needed_caps = [
         'VL', 'SID', 'CHANMODES', 'NOQUIT', 'SJ3', 'NICKIP', 'UMODE2', 'SJOIN']
        self.handle_svskill = self.handle_kill
        self.topic_burst = self.topic

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
        modes = set(modes)
        modes |= {('+x', None), ('+t', None)}
        raw_modes = self.join_modes(modes)
        u = self.users[uid] = User(self, nick, ts, uid, server, ident=ident, host=host, realname=realname, realhost=realhost,
          ip=ip,
          manipulatable=manipulatable,
          opertype=opertype)
        self.apply_modes(uid, modes)
        self.servers[server].users.add(uid)
        if ip == '0.0.0.0':
            encoded_ip = '*'
        else:
            try:
                binary_ip = socket.inet_pton(socket.AF_INET, ip)
            except OSError:
                try:
                    binary_ip = socket.inet_pton(socket.AF_INET6, ip)
                except OSError:
                    raise ValueError('Invalid IPv4 or IPv6 address %r.' % ip)

            encoded_ip = codecs.encode(binary_ip, 'base64')
            encoded_ip = encoded_ip.strip().decode()
        self._send_with_prefix(server, 'UID {nick} {hopcount} {ts} {ident} {realhost} {uid} 0 {modes} {host} * {ip} :{realname}'.format(ts=ts,
          host=host,
          nick=nick,
          ident=ident,
          uid=uid,
          modes=raw_modes,
          realname=realname,
          realhost=realhost,
          ip=encoded_ip,
          hopcount=(self.servers[server].hopcount)))
        return u

    def join(self, client, channel):
        """Joins a PyLink client to a channel."""
        if not self.is_internal_client(client):
            raise LookupError('No such PyLink client exists.')
        else:
            if channel not in self.channels:
                prefix = 'o'
            else:
                prefix = ''
        self.sjoin(self.sid, channel, [(prefix, client)])

    def sjoin(self, server, channel, users, ts=None, modes=set()):
        """Sends an SJOIN for a group of users to a channel.

        The sender should always be a server (SID). TS is optional, and defaults
        to the one we've stored in the channel state if not given.
        <users> is a list of (prefix mode, UID) pairs:

        Example uses:
            sjoin('100', '#test', [('', '100AAABBC'), ('o', 100AAABBB'), ('v', '100AAADDD')])
            sjoin(self.sid, '#test', [('o', self.pseudoclient.uid)])
        """
        server = server or self.sid
        assert users, 'sjoin: No users sent?'
        if not server:
            raise LookupError('No such PyLink server exists.')
        changedmodes = set(modes or self._channels[channel].modes)
        orig_ts = self._channels[channel].ts
        ts = ts or orig_ts
        uids = []
        itemlist = []
        for userpair in users:
            assert len(userpair) == 2, 'Incorrect format of userpair: %r' % userpair
            prefixes, user = userpair
            prefixchars = ''.join([SJOIN_PREFIXES.get(prefix, '') for prefix in prefixes])
            if prefixchars:
                changedmodes |= {('+%s' % prefix, user) for prefix in prefixes}
            itemlist.append(prefixchars + user)
            uids.append(user)
            try:
                self.users[user].channels.add(channel)
            except KeyError:
                log.debug("(%s) sjoin: KeyError trying to add %r to %r's channel list?", self.name, channel, user)

        simplemodes = set()
        for modepair in modes:
            if modepair[0][(-1)] in self.cmodes['*A']:
                if (
                 modepair[0][(-1)], modepair[1]) in self._channels[channel].modes:
                    pass
                else:
                    sjoin_prefix = SJOIN_PREFIXES.get(modepair[0][(-1)])
                    if sjoin_prefix:
                        itemlist.append(sjoin_prefix + modepair[1])
            else:
                simplemodes.add(modepair)

        sjoin_prefix = ':{sid} SJOIN {ts} {channel}'.format(sid=server, ts=ts, channel=channel)
        if modes:
            sjoin_prefix += ' %s' % self.join_modes(simplemodes)
        sjoin_prefix += ' :'
        for line in utils.wrap_arguments(sjoin_prefix, itemlist, self.S2S_BUFSIZE):
            self.send(line)

        self._channels[channel].users.update(uids)
        self.updateTS(server, channel, ts, changedmodes)

    def _ping_uplink(self):
        """Sends a PING to the uplink."""
        if self.sid:
            if self.uplink:
                self._send_with_prefix(self.sid, 'PING %s %s' % (self.get_friendly_name(self.sid), self.get_friendly_name(self.uplink)))

    def mode(self, numeric, target, modes, ts=None):
        """
        Sends mode changes from a PyLink client/server. The mode list should be
        a list of (mode, arg) tuples, i.e. the format of utils.parse_modes() output.
        """
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        self.apply_modes(target, modes)
        if self.is_channel(target):
            modes = list(modes)
            for idx, mode in enumerate(modes):
                if mode[0][(-1)] in self.prefixmodes:
                    log.debug('(%s) mode: expanding PUID of mode %s', self.name, str(mode))
                    modes[idx] = (mode[0], self._expandPUID(mode[1]))

            ts = ts or self._channels[target].ts
            bufsize = self.S2S_BUFSIZE - 7
            bufsize -= len(str(ts))
            bufsize -= len(target)
            bufsize -= 5 if self.is_internal_server(numeric) else 11
            for modestring in self.wrap_modes(modes, bufsize, max_modes_per_msg=12):
                self._send_with_prefix(numeric, 'MODE %s %s %s' % (target, modestring, ts))

        else:
            if not self.is_internal_client(target):
                raise ProtocolError('Cannot force mode change on external clients!')
            joinedmodes = self.join_modes(modes)
            self._send_with_prefix(target, 'UMODE2 %s' % joinedmodes)

    def set_server_ban(self, source, duration, user='*', host='*', reason='User banned'):
        """
        Sets a server ban.
        """
        if not not user == host == '*':
            raise AssertionError('Refusing to set ridiculous ban on *@*')
        else:
            if source in self.users:
                real_source = self.get_server(source)
            else:
                real_source = source
        setter = self.get_hostmask(source) if source in self.users else self.get_friendly_name(source)
        currtime = int(time.time())
        self._send_with_prefix(real_source, 'TKL + G %s %s %s %s %s :%s' % (user, host, setter, currtime + duration if duration != 0 else 0, currtime, reason))

    def update_client(self, target, field, text):
        """Updates the ident, host, or realname of any connected client."""
        field = field.upper()
        if field not in ('IDENT', 'HOST', 'REALNAME', 'GECOS'):
            raise NotImplementedError('Changing field %r of a client is unsupported by this protocol.' % field)
        if self.is_internal_client(target):
            if field == 'IDENT':
                self.users[target].ident = text
                self._send_with_prefix(target, 'SETIDENT %s' % text)
            else:
                if field == 'HOST':
                    self.users[target].host = text
                    self._send_with_prefix(target, 'SETHOST %s' % text)
                else:
                    if field in ('REALNAME', 'GECOS'):
                        self.users[target].realname = text
                        self._send_with_prefix(target, 'SETNAME :%s' % text)
        else:
            if field == 'IDENT':
                self.users[target].ident = text
                self._send_with_prefix(self.sid, 'CHGIDENT %s %s' % (target, text))
                self.call_hooks([self.sid, 'CHGIDENT',
                 {'target':target, 
                  'newident':text}])
            else:
                if field == 'HOST':
                    self.users[target].host = text
                    self._send_with_prefix(self.sid, 'CHGHOST %s %s' % (target, text))
                    self.call_hooks([self.sid, 'CHGHOST',
                     {'target':target, 
                      'newhost':text}])
                elif field in ('REALNAME', 'GECOS'):
                    self.users[target].realname = text
                    self._send_with_prefix(self.sid, 'CHGNAME %s :%s' % (target, text))
                    self.call_hooks([self.sid, 'CHGNAME',
                     {'target':target, 
                      'newgecos':text}])

    def knock(self, numeric, target, text):
        """Sends a KNOCK from a PyLink client."""
        assert self.is_channel(target), 'Can only knock on channels!'
        sender = self.get_server(numeric)
        s = '[Knock] by %s (%s)' % (self.get_hostmask(numeric), text)
        self._send_with_prefix(sender, 'NOTICE @%s :%s' % (target, s))

    def post_connect(self):
        """Initializes a connection to a server."""
        ts = self.start_ts
        self.prefixmodes = {'q':'~',  'a':'&',  'o':'@',  'h':'%',  'v':'+'}
        self.legacy_uidgen = PUIDGenerator('U32user')
        f = self.send
        host = self.serverdata['hostname']
        f('PASS :%s' % self.serverdata['sendpass'])
        f('PROTOCTL SJOIN SJ3 NOQUIT NICKv2 VL UMODE2 PROTOCTL NICKIP EAUTH=%s SID=%s VHP ESVID' % (self.serverdata['hostname'], self.sid))
        sdesc = self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']
        f('SERVER %s 1 U%s-h6e-%s :%s' % (host, self.proto_ver, self.sid, sdesc))
        self._send_with_prefix(self.sid, 'EOS')
        self.extbans_acting = {'quiet':'~q:', 
         'ban_nonick':'~n:', 
         'ban_nojoins':'~j:', 
         'filter':'~T:block:', 
         'filter_censor':'~T:censor:', 
         'msgbypass_external':'~m:external:', 
         'msgbypass_censor':'~m:censor:', 
         'msgbypass_moderated':'~m:moderated:', 
         'ban_stripcolor':'~m:color:', 
         'ban_nonotice':'~m:notice:', 
         'timedban_unreal':'~t:'}
        self.extbans_matching = {'ban_account':'~a:',  'ban_inchannel':'~c:', 
         'ban_opertype':'~O:', 
         'ban_realname':'~r:', 
         'ban_account_legacy':'~R:', 
         'ban_certfp':'~S:'}

    def handle_eos(self, numeric, command, args):
        """EOS is used to denote end of burst."""
        self.servers[numeric].has_eob = True
        if numeric == self.uplink:
            self.connected.set()
        return {}

    def handle_uid(self, numeric, command, args):
        nick = args[0]
        self._check_nick_collision(nick)
        ts, ident, realhost, uid, accountname, modestring, host = args[2:9]
        ts = int(ts)
        if host == '*':
            host = args[9]
        raw_ip = args[10].encode()
        if raw_ip == b'*':
            ip = '0.0.0.0'
        else:
            ip = codecs.decode(raw_ip, 'base64')
        try:
            ip = socket.inet_ntop(socket.AF_INET, ip)
        except ValueError:
            ip = socket.inet_ntop(socket.AF_INET6, ip)
            if ip.startswith(':'):
                ip = '0' + ip

        realname = args[(-1)]
        self.users[uid] = User(self, nick, ts, uid, numeric, ident, host, realname, realhost, ip)
        self.servers[numeric].users.add(uid)
        parsedmodes = self.parse_modes(uid, [modestring])
        self.apply_modes(uid, parsedmodes)
        self.users[uid].cloaked_host = args[9]
        self._check_oper_status_change(uid, parsedmodes)
        if ('+x', None) not in parsedmodes:
            self.users[uid].host = realhost
        if ('+r', None) in parsedmodes:
            if accountname.isdigit():
                accountname = nick
        if not accountname.isdigit():
            self.call_hooks([uid, 'CLIENT_SERVICES_LOGIN', {'text': accountname}])
        return {'uid':uid, 
         'ts':ts,  'nick':nick,  'realhost':realhost,  'host':host,  'ident':ident, 
         'ip':ip,  'parse_as':'UID'}

    def handle_pass(self, numeric, command, args):
        if args[0] != self.serverdata['recvpass']:
            raise ProtocolError('RECVPASS from uplink does not match configuration!')

    def handle_ping(self, numeric, command, args):
        if numeric == self.uplink:
            self.send(('PONG %s :%s' % (self.serverdata['hostname'], args[(-1)])), queue=False)

    def handle_server(self, numeric, command, args):
        sname = args[0]
        if self.uplink not in self.servers:
            for cap in self.needed_caps:
                if cap not in self.caps:
                    raise ProtocolError('Not all required capabilities were met by the remote server. Your version of UnrealIRCd is probably too old! (Got: %s, needed: %s)' % (
                     sorted(self.caps), sorted(self.needed_caps)))

            sdesc = args[(-1)].split(' ', 1)
            vline = sdesc[0].split('-', 1)
            sdesc = ' '.join(sdesc[1:])
            try:
                protover = int(vline[0].strip('U'))
            except ValueError:
                raise ProtocolError('Protocol version too old! (needs at least %s (Unreal 4.x), got something invalid; is VL being sent?)' % self.min_proto_ver)

            if protover < self.min_proto_ver:
                raise ProtocolError('Protocol version too old! (needs at least %s (Unreal 4.x), got %s)' % (
                 self.min_proto_ver, protover))
            self.servers[numeric] = Server(self, None, sname, desc=sdesc)
            if protover < 4203:
                self.umodes.update(self._KNOWN_UMODES)
                self.umodes['*D'] = ''.join(self._KNOWN_UMODES.values())
        else:
            return super().handle_server(numeric, command, args)

    def handle_protoctl(self, numeric, command, args):
        """Handles protocol negotiation."""
        self.caps += [arg.split('=')[0] for arg in args]
        for cap in args:
            if cap.startswith('SID'):
                self.uplink = cap.split('=', 1)[1]
            else:
                if cap.startswith('CHANMODES'):
                    supported_cmodes = cap.split('=', 1)[1]
                    self.cmodes['*A'], self.cmodes['*B'], self.cmodes['*C'], self.cmodes['*D'] = supported_cmodes.split(',')
                    for namedmode, modechar in self._KNOWN_CMODES.items():
                        if modechar in supported_cmodes:
                            self.cmodes[namedmode] = modechar

                else:
                    if cap.startswith('USERMODES'):
                        self.umodes['*D'] = supported_umodes = cap.split('=', 1)[1]
                        for namedmode, modechar in self._KNOWN_UMODES.items():
                            if modechar in supported_umodes:
                                self.umodes[namedmode] = modechar

        self.cmodes.update({'halfop':'h',  'admin':'a',  'owner':'q',  'op':'o', 
         'voice':'v'})

    def handle_join(self, numeric, command, args):
        """Handles the UnrealIRCd JOIN command."""
        if args[0] == '0':
            oldchans = self.users[numeric].channels.copy()
            log.debug('(%s) Got /join 0 from %r, channel list is %r', self.name, numeric, oldchans)
            for ch in oldchans:
                self._channels[ch].users.discard(numeric)
                self.users[numeric].channels.discard(ch)

            return {'channels':oldchans, 
             'text':'Left all channels.',  'parse_as':'PART'}
        for channel in args[0].split(','):
            c = self._channels[channel]
            self.users[numeric].channels.add(channel)
            self._channels[channel].users.add(numeric)
            self.call_hooks([numeric, command,
             {'channel':channel,  'users':[numeric],  'modes':c.modes, 
              'ts':c.ts}])

    def handle_sjoin(self, numeric, command, args):
        """Handles the UnrealIRCd SJOIN command."""
        channel = args[1]
        chandata = self._channels[channel].deepcopy()
        userlist = args[(-1)].split()
        namelist = []
        log.debug('(%s) handle_sjoin: got userlist %r for %r', self.name, userlist, channel)
        modestring = ''
        changedmodes = set()
        parsedmodes = []
        try:
            if args[2].startswith('+'):
                modestring = args[2:-1] or args[2]
                modestring = [m for m in modestring if m]
                parsedmodes = self.parse_modes(channel, modestring)
                changedmodes = set(parsedmodes)
        except IndexError:
            pass

        for userpair in userlist:
            if userpair.startswith('&'):
                changedmodes.add(('+b', userpair[1:]))
            elif userpair.startswith('"'):
                changedmodes.add(('+e', userpair[1:]))
            elif userpair.startswith("'"):
                changedmodes.add(('+I', userpair[1:]))
            else:
                r = re.search('([~*@%+]*)(.*)', userpair)
                user = r.group(2)
                if not user:
                    pass
                else:
                    user = self._get_UID(user)
                    if user not in self.users:
                        log.debug("(%s) Ignoring user %s in SJOIN to %s, they don't exist anymore", self.name, user, channel)
                    else:
                        modeprefix = (r.group(1) or '').replace('~', '&').replace('*', '~')
                        finalprefix = ''
                        log.debug('(%s) handle_sjoin: got modeprefix %r for user %r', self.name, modeprefix, user)
                        for m in modeprefix:
                            for char, prefix in self.prefixmodes.items():
                                if m == prefix:
                                    finalprefix += char

                        namelist.append(user)
                        self.users[user].channels.add(channel)
                        changedmodes |= {('+%s' % mode, user) for mode in finalprefix}
                        self._channels[channel].users.add(user)

        our_ts = self._channels[channel].ts
        their_ts = int(args[0])
        self.updateTS(numeric, channel, their_ts, changedmodes)
        return {'channel':channel, 
         'users':namelist,  'modes':parsedmodes,  'ts':their_ts, 
         'channeldata':chandata}

    def handle_nick(self, numeric, command, args):
        if len(args) > 2:
            log.debug('(%s) got legacy NICK args: %s', self.name, ' '.join(args))
            new_args = args[:]
            servername = new_args[5].lower()
            fake_uid = self.legacy_uidgen.next_uid(prefix=(args[0]))
            new_args[5] = fake_uid
            new_args.insert(-2, args[4])
            log.debug('(%s) translating legacy NICK args to: %s', self.name, ' '.join(new_args))
            return self.handle_uid(servername, 'UID_LEGACY', new_args)
        else:
            return super().handle_nick(numeric, command, args)

    def handle_mode(self, numeric, command, args):
        if self.is_channel(args[0]):
            channel = args[0]
            oldobj = self._channels[channel].deepcopy()
            modes = [arg for arg in args[1:] if arg]
            parsedmodes = self.parse_modes(channel, modes)
            if parsedmodes:
                if parsedmodes[0][0] == '+&':
                    log.debug('(%s) Received mode bounce %s in channel %s! Our TS: %s', self.name, modes, channel, self._channels[channel].ts)
                    return
                self.apply_modes(channel, parsedmodes)
            if numeric in self.servers:
                if args[(-1)].isdigit():
                    their_ts = int(args[(-1)])
                    if their_ts > 0:
                        self.updateTS(numeric, channel, their_ts)
            return {'target':channel, 
             'modes':parsedmodes,  'channeldata':oldobj}
        else:
            target = self._get_UID(args[0])
            return self._handle_umode(target, self.parse_modes(target, args[1:]))

    def _check_cloak_change(self, uid, parsedmodes):
        """
        Checks whether +x/-x was set in the mode query, and changes the
        hostname of the user given to or from their cloaked host if True.
        """
        userobj = self.users[uid]
        final_modes = userobj.modes
        oldhost = userobj.host
        if ('+x', None) in parsedmodes and ('t', None) not in final_modes or ('-t',
                                                                              None) in parsedmodes and ('x',
                                                                                                        None) in final_modes:
            newhost = userobj.host = userobj.cloaked_host
        else:
            if ('-x', None) in parsedmodes or ('-t', None) in parsedmodes:
                newhost = userobj.host = userobj.realhost
            else:
                return
        if newhost != oldhost:
            self.call_hooks([uid, 'SETHOST',
             {'target':uid, 
              'newhost':newhost}])

    def handle_svsmode(self, numeric, command, args):
        """Handles SVSMODE, used by services for setting user modes on others."""
        target = self._get_UID(args[0])
        return self._handle_umode(target, self.parse_modes(target, args[1:]))

    def handle_svs2mode(self, sender, command, args):
        """
        Handles SVS2MODE, which sets services login information on the given target.
        """
        target = self._get_UID(args[0])
        parsedmodes = self.parse_modes(target, args[1:])
        if ('+r', None) in parsedmodes:
            try:
                account = args[2]
            except IndexError:
                if not self.users[target].services_account:
                    account = self.get_friendly_name(target)
                else:
                    return
            else:
                if account.isdigit():
                    account = self.get_friendly_name(target)
        else:
            if ('-r', None) in parsedmodes:
                if not self.users[target].services_account:
                    return
                account = ''
            else:
                if ('+d', None) in parsedmodes:
                    account = args[2]
                    if account == '0':
                        account = ''
                else:
                    return
        self.call_hooks([target, 'CLIENT_SERVICES_LOGIN', {'text': account}])
        return self._handle_umode(target, [mode for mode in parsedmodes if mode[0][(-1)] != 'd'])

    def _handle_umode(self, target, parsedmodes):
        """Internal helper function to parse umode changes."""
        if not parsedmodes:
            return
        else:
            self.apply_modes(target, parsedmodes)
            self._check_oper_status_change(target, parsedmodes)
            self._check_cloak_change(target, parsedmodes)
            return {'target':target, 
             'modes':parsedmodes}

    def handle_umode2(self, source, command, args):
        """Handles UMODE2, used to set user modes on oneself."""
        target = self._get_UID(source)
        return self._handle_umode(target, self.parse_modes(target, args))

    def handle_topic(self, numeric, command, args):
        """Handles the TOPIC command."""
        channel = args[0]
        topic = args[(-1)]
        setter = args[1]
        ts = args[2]
        oldtopic = self._channels[channel].topic
        self._channels[channel].topic = topic
        self._channels[channel].topicset = True
        return {'channel':channel, 
         'setter':setter,  'ts':ts,  'text':topic,  'oldtopic':oldtopic}

    def handle_setident(self, numeric, command, args):
        """Handles SETIDENT, used for self ident changes."""
        self.users[numeric].ident = newident = args[0]
        return {'target':numeric,  'newident':newident}

    def handle_sethost(self, numeric, command, args):
        """Handles CHGHOST, used for self hostname changes."""
        self.users[numeric].host = newhost = args[0]
        self.apply_modes(numeric, [('+x', None), ('+t', None)])
        return {'target':numeric, 
         'newhost':newhost}

    def handle_setname(self, numeric, command, args):
        """Handles SETNAME, used for self real name/gecos changes."""
        self.users[numeric].realname = newgecos = args[0]
        return {'target':numeric,  'newgecos':newgecos}

    def handle_chgident(self, numeric, command, args):
        """Handles CHGIDENT, used for denoting ident changes."""
        target = self._get_UID(args[0])
        self.users[target].ident = newident = args[1]
        return {'target':target,  'newident':newident}

    def handle_chghost(self, numeric, command, args):
        """Handles CHGHOST, used for denoting hostname changes."""
        target = self._get_UID(args[0])
        self.users[target].host = newhost = args[1]
        self.apply_modes(target, [('+x', None), ('+t', None)])
        return {'target':target, 
         'newhost':newhost}

    def handle_chgname(self, numeric, command, args):
        """Handles CHGNAME, used for denoting real name/gecos changes."""
        target = self._get_UID(args[0])
        self.users[target].realname = newgecos = args[1]
        return {'target':target,  'newgecos':newgecos}

    def handle_tsctl(self, source, command, args):
        """Handles /TSCTL alltime requests."""
        if args[0] == 'alltime':
            self._send_with_prefix(self.sid, 'NOTICE %s :*** Server=%s time()=%d' % (source, self.hostname(), time.time()))


Class = UnrealProtocol
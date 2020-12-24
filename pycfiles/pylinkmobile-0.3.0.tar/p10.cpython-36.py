# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/p10.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 57137 bytes
__doc__ = '\np10.py: P10 protocol module for PyLink, supporting Nefarious IRCu and others.\n'
import base64, struct, time
from ipaddress import ip_address
from pylinkirc import conf, structures, utils
from pylinkirc.classes import *
from pylinkirc.log import log
from pylinkirc.protocols.ircs2s_common import *

class P10UIDGenerator(IncrementalUIDGenerator):
    """P10UIDGenerator"""

    def __init__(self, sid):
        self.allowedchars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]'
        self.length = 3
        super().__init__(sid)


def p10b64encode(num, length=2):
    """
    Encodes a given numeric using P10 Base64 numeric nicks, as documented at
    https://github.com/evilnet/nefarious2/blob/a29b63144/doc/p10.txt#L69-L92
    """
    sidbytes = struct.pack('>I', num)[1:]
    sid = base64.b64encode(sidbytes, '[]')[-length:]
    return sid.decode()


class P10SIDGenerator:

    def __init__(self, irc):
        self.irc = irc
        try:
            query = irc.serverdata['sidrange']
        except (KeyError, ValueError):
            raise RuntimeError('(%s) "sidrange" is missing from your server configuration block!' % irc.name)

        try:
            self.minnum, self.maxnum = map(int, query.split('-', 1))
        except ValueError:
            raise RuntimeError('(%s) Invalid sidrange %r' % (irc.name, query))
        else:
            self.currentnum = self.minnum

    def next_sid(self):
        """
        Returns the next available SID.
        """
        if self.currentnum > self.maxnum:
            raise ProtocolError("Ran out of valid SIDs! Check your 'sidrange' setting and try again.")
        sid = p10b64encode(self.currentnum)
        self.currentnum += 1
        return sid


GLINE_MAX_EXPIRE = 604800

class P10Protocol(IRCS2SProtocol):
    COMMAND_TOKENS = {'AC':'ACCOUNT', 
     'AD':'ADMIN', 
     'LL':'ASLL', 
     'A':'AWAY', 
     'B':'BURST', 
     'CAP':'CAP', 
     'CM':'CLEARMODE', 
     'CLOSE':'CLOSE', 
     'CN':'CNOTICE', 
     'CO':'CONNECT', 
     'CP':'CPRIVMSG', 
     'C':'CREATE', 
     'DE':'DESTRUCT', 
     'DS':'DESYNCH', 
     'DIE':'DIE', 
     'DNS':'DNS', 
     'EB':'END_OF_BURST', 
     'EA':'EOB_ACK', 
     'Y':'ERROR', 
     'GET':'GET', 
     'GL':'GLINE', 
     'HASH':'HASH', 
     'HELP':'HELP', 
     'F':'INFO', 
     'I':'INVITE', 
     'ISON':'ISON', 
     'J':'JOIN', 
     'JU':'JUPE', 
     'K':'KICK', 
     'D':'KILL', 
     'LI':'LINKS', 
     'LIST':'LIST', 
     'LU':'LUSERS', 
     'MAP':'MAP', 
     'M':'MODE', 
     'MO':'MOTD', 
     'E':'NAMES', 
     'N':'NICK', 
     'O':'NOTICE', 
     'OPER':'OPER', 
     'OM':'OPMODE', 
     'L':'PART', 
     'PA':'PASS', 
     'G':'PING', 
     'Z':'PONG', 
     'POST':'POST', 
     'P':'PRIVMSG', 
     'PRIVS':'PRIVS', 
     'PROTO':'PROTO', 
     'Q':'QUIT', 
     'REHASH':'REHASH', 
     'RESET':'RESET', 
     'RESTART':'RESTART', 
     'RI':'RPING', 
     'RO':'RPONG', 
     'S':'SERVER', 
     'SERVSET':'SERVLIST', 
     'SERVSET':'SERVSET', 
     'SET':'SET', 
     'SE':'SETTIME', 
     'U':'SILENCE', 
     'SQUERY':'SQUERY', 
     'SQ':'SQUIT', 
     'R':'STATS', 
     'TI':'TIME', 
     'T':'TOPIC', 
     'TR':'TRACE', 
     'UP':'UPING', 
     'USER':'USER', 
     'USERHOST':'USERHOST', 
     'USERIP':'USERIP', 
     'V':'VERSION', 
     'WC':'WALLCHOPS', 
     'WH':'WALLHOPS', 
     'WA':'WALLOPS', 
     'WU':'WALLUSERS', 
     'WV':'WALLVOICES', 
     'H':'WHO', 
     'W':'WHOIS', 
     'X':'WHOWAS', 
     'XQ':'XQUERY', 
     'XR':'XREPLY', 
     'SN':'SVSNICK', 
     'SJ':'SVSJOIN', 
     'SH':'SETHOST', 
     'FA':'FAKE'}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.uidgen = structures.KeyedDefaultdict(P10UIDGenerator)
        self.sidgen = P10SIDGenerator(self)
        self.hook_map = {'END_OF_BURST':'ENDBURST', 
         'OPMODE':'MODE',  'CLEARMODE':'MODE', 
         'BURST':'JOIN',  'WALLCHOPS':'NOTICE', 
         'WALLHOPS':'NOTICE',  'WALLVOICES':'NOTICE'}
        self.protocol_caps |= {'slash-in-hosts', 'underscore-in-hosts',
         'has-statusmsg'}
        self.handle_opmode = self.handle_mode

    def _send_with_prefix(self, source, text, **kwargs):
        (self.send)(('%s %s' % (source, text)), **kwargs)

    @staticmethod
    def access_sort(key):
        """
        Sorts (prefixmode, UID) keys based on the prefix modes given.
        """
        prefixes, user = key
        accesses = {'o':100, 
         'h':10,  'v':1}
        num = 0
        for prefix in prefixes:
            num += accesses.get(prefix, 0)

        return num

    @staticmethod
    def decode_p10_ip(ip):
        """Decodes a P10 IP."""
        if len(ip) == 6:
            ip = 'AA' + ip
            ip = base64.b64decode(ip, altchars='[]')[2:]
            return socket.inet_ntoa(ip)
        if len(ip) <= 24 or '_' in ip:
            s = ''
            head = ip
            tail = ''
            byteshead = ''
            bytestail = ''
            if '_' in ip:
                head, tail = ip.split('_')
            for section in range(0, len(head), 3):
                byteshead += base64.b64decode('A' + head[section:section + 3], '[]')[1:]

            for section in range(0, len(tail), 3):
                bytestail += base64.b64decode('A' + tail[section:section + 3], '[]')[1:]

            ipbytes = byteshead
            pad = 16 - len(byteshead) - len(bytestail)
            ipbytes += '\x00' * pad
            ipbytes += bytestail
            ip = socket.inet_ntop(socket.AF_INET6, ipbytes)
            if ip.startswith(':'):
                ip = '0' + ip
            return ip

    @staticmethod
    def encode_p10_ipv6(ip):
        """Encodes a P10 IPv6 address."""
        ipbits = []
        for ipbit in ip.split(':'):
            if not ipbit:
                ipbits.append('_')
            else:
                ipbit = int(ipbit, base=16)
                ipbits.append(p10b64encode(ipbit, length=3))

        encoded_ip = ''.join(ipbits)
        if encoded_ip.startswith('_'):
            encoded_ip = 'AAA' + encoded_ip
        return encoded_ip

    def spawn_client(self, nick, ident='null', host='null', realhost=None, modes=set(), server=None, ip='0.0.0.0', realname=None, ts=None, opertype='IRC Operator', manipulatable=False):
        """
        Spawns a new client with the given options.

        Note: No nick collision / valid nickname checks are done here; it is
        up to plugins to make sure they don't introduce anything invalid.
        """
        server = server or self.sid
        if not self.is_internal_server(server):
            raise ValueError('Server %r is not a PyLink server!' % server)
        else:
            uid = self.uidgen.setdefault(server, P10UIDGenerator(server)).next_uid()
            ts = ts or int(time.time())
            realname = realname or conf.conf['pylink']['realname']
            realhost = realhost or host
            raw_modes = self.join_modes(modes)
            u = self.users[uid] = User(self, nick, ts, uid, server, ident=ident, host=host, realname=realname, realhost=realhost,
              ip=ip,
              manipulatable=manipulatable,
              opertype=opertype)
            self.apply_modes(uid, modes)
            self.servers[server].users.add(uid)
            if ip_address(ip).version == 4:
                ip = '\x00\x00' + socket.inet_aton(ip)
                b64ip = base64.b64encode(ip, '[]')[2:].decode()
            else:
                if '6' in self._flags:
                    b64ip = self.encode_p10_ipv6(ip)
                else:
                    b64ip = 'AAAAAA'
        self._send_with_prefix(server, 'N {nick} {hopcount} {ts} {ident} {host} {modes} {ip} {uid} :{realname}'.format(ts=ts,
          host=host,
          nick=nick,
          ident=ident,
          uid=uid,
          modes=raw_modes,
          ip=b64ip,
          realname=realname,
          realhost=realhost,
          hopcount=(self.servers[server].hopcount)))
        return u

    def away(self, source, text):
        """Sends an AWAY message from a PyLink client. <text> can be an empty string
        to unset AWAY status."""
        if not self.is_internal_client(source):
            raise LookupError('No such PyLink client exists.')
        else:
            if text:
                self._send_with_prefix(source, 'A :%s' % text)
            else:
                self._send_with_prefix(source, 'A')
        self.users[source].away = text

    def invite(self, numeric, target, channel):
        """Sends INVITEs from a PyLink client."""
        if not self.is_internal_client(numeric):
            raise LookupError('No such PyLink client exists.')
        nick = self.users[target].nick
        self._send_with_prefix(numeric, 'I %s %s %s' % (nick, channel, self._channels[channel].ts))

    def join(self, client, channel):
        """Joins a PyLink client to a channel."""
        ts = self._channels[channel].ts
        if not self.is_internal_client(client):
            raise LookupError('No such PyLink client exists.')
        else:
            if not self._channels[channel].users:
                self._send_with_prefix(client, 'C {channel} {ts}'.format(ts=ts, channel=channel))
            else:
                self._send_with_prefix(client, 'J {channel} {ts}'.format(ts=ts, channel=channel))
        self._channels[channel].users.add(client)
        self.users[client].channels.add(channel)

    def kick(self, numeric, channel, target, reason=None):
        """Sends kicks from a PyLink client/server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
            if not reason:
                reason = 'No reason given'
        else:
            cobj = self._channels[channel]
            if numeric not in self.servers:
                if not cobj.is_halfop_plus(numeric):
                    reason = '(%s) %s' % (self.get_friendly_name(numeric), reason)
                    numeric = self.get_server(numeric)
            self._send_with_prefix(numeric, 'K %s %s :%s' % (channel, target, reason))
            self.handle_part(target, 'KICK', [channel])
            if self.is_internal_client(target):
                self._send_with_prefix(target, 'L %s :%s' % (channel, reason))

    def kill(self, numeric, target, reason):
        """Sends a kill from a PyLink client/server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        self._send_with_prefix(numeric, 'D %s :Killed (%s)' % (target, reason))
        self._remove_client(target)

    def knock(self, source, target, text):
        """KNOCK wrapper for P10: notifies chanops that someone wants to join
        the channel."""
        prefix = '%' if 'h' in self.prefixmodes else '@'
        self.notice(self.pseudoclient.uid, prefix + target, 'Knock from %s: %s' % (self.get_friendly_name(source), text))

    def message(self, source, target, text, _notice=False):
        """Sends a PRIVMSG from a PyLink client or server."""
        if not self.is_internal_client(source):
            if not self.is_internal_server(source):
                raise LookupError('No such PyLink client/server exists.')
        token = 'O' if _notice else 'P'
        stripped_target = target.lstrip(''.join(self.prefixmodes.values()))
        if self.is_channel(stripped_target):
            msgprefixes = target.split('#', 1)[0]
            if '@' in msgprefixes:
                token = 'WC'
                text = '@ ' + text
            else:
                if '%' in msgprefixes:
                    token = 'WH'
                    text = '% ' + text
                else:
                    if '+' in msgprefixes:
                        token = 'WV'
                        text = '+ ' + text
            target = stripped_target
        self._send_with_prefix(source, '%s %s :%s' % (token, target, text))

    def notice(self, source, target, text):
        """Sends a NOTICE from a PyLink client or server."""
        self.message(source, target, text, _notice=True)

    def mode(self, numeric, target, modes, ts=None):
        """Sends mode changes from a PyLink client/server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        else:
            modes = list(modes)
            is_cmode = self.is_channel(target)
            if is_cmode:
                cobj = self._channels[target]
                ts = ts or cobj.ts
                if numeric not in self.servers:
                    if not cobj.is_halfop_plus(numeric):
                        numeric = self.get_server(numeric)
                bufsize = self.S2S_BUFSIZE - len(numeric) - 4 - len(target) - len(str(ts))
                real_target = target
            elif not target in self.users:
                raise AssertionError('Unknown mode target %s' % target)
            real_target = self.users[target].nick
        self.apply_modes(target, modes)
        while modes[:12]:
            joinedmodes = self.join_modes([m for m in modes[:12]])
            if is_cmode:
                for wrapped_modes in self.wrap_modes(modes[:12], bufsize):
                    self._send_with_prefix(numeric, 'M %s %s %s' % (real_target, wrapped_modes, ts))

            else:
                self._send_with_prefix(numeric, 'M %s %s' % (real_target, joinedmodes))
            modes = modes[12:]

    def nick(self, numeric, newnick):
        """Changes the nick of a PyLink client."""
        if not self.is_internal_client(numeric):
            raise LookupError('No such PyLink client exists.')
        self._send_with_prefix(numeric, 'N %s %s' % (newnick, int(time.time())))
        self.users[numeric].nick = newnick
        self.users[numeric].ts = int(time.time())

    def numeric(self, source, numeric, target, text):
        """Sends raw numerics from a server to a remote client. This is used for WHOIS
        replies."""
        self._send_with_prefix(source, '%s %s %s' % (numeric, target, text))

    def part(self, client, channel, reason=None):
        """Sends a part from a PyLink client."""
        if not self.is_internal_client(client):
            raise LookupError('No such PyLink client exists.')
        msg = 'L %s' % channel
        if reason:
            msg += ' :%s' % reason
        self._send_with_prefix(client, msg)
        self.handle_part(client, 'PART', [channel])

    def _ping_uplink(self):
        """Sends a PING to the uplink."""
        if self.sid:
            self._send_with_prefix(self.sid, 'G %s' % self.sid)

    def quit(self, numeric, reason):
        """Quits a PyLink client."""
        if self.is_internal_client(numeric):
            self._send_with_prefix(numeric, 'Q :%s' % reason)
            self._remove_client(numeric)
        else:
            raise LookupError('No such PyLink client exists.')

    def set_server_ban(self, source, duration, user='*', host='*', reason='User banned'):
        """
        Sets a server ban.
        """
        assert not user == host == '*', 'Refusing to set ridiculous ban on *@*'
        currtime = int(time.time())
        if duration == 0 or duration > GLINE_MAX_EXPIRE:
            log.debug('(%s) Lowering GLINE duration on %s@%s from %s to %s', self.name, user, host, duration, GLINE_MAX_EXPIRE)
            duration = GLINE_MAX_EXPIRE
        self._send_with_prefix(source, 'GL * +%s@%s %s %s %s :%s' % (user, host, duration, currtime, currtime + duration, reason))

    def sjoin(self, server, channel, users, ts=None, modes=set()):
        """Sends an SJOIN for a group of users to a channel.

        The sender should always be a Server ID (SID). TS is optional, and defaults
        to the one we've stored in the channel state if not given.
        <users> is a list of (prefix mode, UID) pairs:

        Example uses:
            sjoin('100', '#test', [('', '100AAABBC'), ('o', 100AAABBB'), ('v', '100AAADDD')])
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
        bans = []
        exempts = []
        regularmodes = []
        for mode in modes:
            modechar = mode[0][(-1)]
            if modechar in self.cmodes['*A']:
                if (
                 modechar, mode[1]) not in self._channels[channel].modes:
                    if modechar == 'b':
                        bans.append(mode[1])
                    elif modechar == 'e':
                        exempts.append(mode[1])
            else:
                regularmodes.append(mode)

        log.debug('(%s) sjoin: bans: %s, exempts: %s, other modes: %s', self.name, bans, exempts, regularmodes)
        changedmodes = set(modes)
        changedusers = []
        namelist = []
        users = sorted(users, key=(self.access_sort))
        msgprefix = '{sid} B {channel} {ts} '.format(sid=server, channel=channel, ts=ts)
        if regularmodes:
            msgprefix += '%s ' % self.join_modes(regularmodes)
        last_prefixes = ''
        for userpair in users:
            if not len(userpair) == 2:
                raise AssertionError('Incorrect format of userpair: %r' % userpair)
            else:
                prefixes, user = userpair
                changedusers.append(user)
                log.debug('(%s) sjoin: adding %s:%s to namelist', self.name, user, prefixes)
                if prefixes:
                    if prefixes != last_prefixes:
                        namelist.append('%s:%s' % (user, prefixes))
                else:
                    namelist.append(user)
                last_prefixes = prefixes
                if prefixes:
                    for prefix in prefixes:
                        changedmodes.add(('+%s' % prefix, user))

            self.users[user].channels.add(channel)
        else:
            if namelist:
                log.debug('(%s) sjoin: got %r for namelist', self.name, namelist)
                names_dict = {uid:prefixes for prefixes, uid in users}
                for linenum, wrapped_msg in enumerate(utils.wrap_arguments(msgprefix, namelist, (self.S2S_BUFSIZE - 1 - len(self.prefixmodes)), separator=',')):
                    if linenum:
                        wrapped_args = self.parse_args(wrapped_msg.split(' '))
                        wrapped_namelist = wrapped_args[(-1)].split(',')
                        log.debug('(%s) sjoin: wrapped args: %s (post-wrap fixing)', self.name, wrapped_args)
                        first_uid = wrapped_namelist[0]
                        first_prefix = names_dict.get(first_uid, '')
                        log.debug('(%s) sjoin: prefixes for first user %s: %s (post-wrap fixing)', self.name, first_uid, first_prefix)
                        if ':' not in first_uid:
                            if first_prefix:
                                log.debug('(%s) sjoin: re-adding prefix %s to user %s (post-wrap fixing)', self.name, first_uid, first_prefix)
                                wrapped_namelist[0] += ':%s' % prefixes
                                wrapped_msg = ' '.join(wrapped_args[:-1])
                                wrapped_msg += ' '
                                wrapped_msg += ','.join(wrapped_namelist)
                    self.send(wrapped_msg)

        self._channels[channel].users.update(changedusers)
        if bans or exempts:
            msgprefix += ':%'
            if bans:
                for wrapped_msg in utils.wrap_arguments(msgprefix, bans, self.S2S_BUFSIZE):
                    self.send(wrapped_msg)

            if exempts:
                msgprefix += ' ~ '
                for wrapped_msg in utils.wrap_arguments(msgprefix, exempts, self.S2S_BUFSIZE):
                    self.send(wrapped_msg)

        self.updateTS(server, channel, ts, changedmodes)

    def spawn_server(self, name, sid=None, uplink=None, desc=None):
        """
        Spawns a server off a PyLink server. desc (server description)
        defaults to the one in the config. uplink defaults to the main PyLink
        server, and sid (the server ID) is automatically generated if not
        given.
        """
        uplink = uplink or self.sid
        name = name.lower()
        desc = desc or self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']
        if sid is None:
            sid = self.sidgen.next_sid()
        elif not len(sid) == 2:
            raise AssertionError('Incorrect SID length')
        if sid in self.servers:
            raise ValueError('A server with SID %r already exists!' % sid)
        for server in self.servers.values():
            if name == server.name:
                raise ValueError('A server named %r already exists!' % name)

        if not self.is_internal_server(uplink):
            raise ValueError('Server %r is not a PyLink server!' % uplink)
        if not self.is_server_name(name):
            raise ValueError('Invalid server name %r' % name)
        self.servers[sid] = Server(self, uplink, name, internal=True, desc=desc)
        self._send_with_prefix(uplink, 'SERVER %s %s %s %s P10 %s]]] +h6 :%s' % (
         name, self.servers[sid].hopcount, self.start_ts, int(time.time()), sid, desc))
        return sid

    def squit(self, source, target, text='No reason given'):
        """SQUITs a PyLink server."""
        targetname = self.servers[target].name
        self._send_with_prefix(source, 'SQ %s 0 :%s' % (targetname, text))
        self.handle_squit(source, 'SQUIT', [target, text])

    def topic(self, source, target, text):
        """Sends a TOPIC change from a PyLink client or server."""
        if not self.is_internal_client(source):
            if not self.is_internal_server(source):
                raise LookupError('No such PyLink client/server exists.')
        else:
            if source in self.users:
                sendername = self.get_hostmask(source)
            else:
                sendername = self.get_friendly_name(source)
        creationts = self._channels[target].ts
        self._send_with_prefix(source, 'T %s %s %s %s :%s' % (target, sendername, creationts,
         int(time.time()), text))
        self._channels[target].topic = text
        self._channels[target].topicset = True

    topic_burst = topic

    def update_client(self, target, field, text):
        """Updates the ident or host of any connected client."""
        uobj = self.users[target]
        ircd = self.serverdata.get('ircd', self.serverdata.get('p10_ircd', 'nefarious')).lower()
        if self.is_internal_client(target):
            if ircd not in ('nefarious', 'snircd'):
                raise NotImplementedError("Host changing for internal clients (via SETHOST) is only available on nefarious and snircd, and we're using p10_ircd=%r" % ircd)
            else:
                if field == 'HOST':
                    self.mode(target, target, [('+x', None), ('+h', '%s@%s' % (uobj.ident, text))])
                else:
                    if field == 'IDENT':
                        self.mode(target, target, [('-h', None)])
                        self.mode(target, target, [('+x', None), ('+h', '%s@%s' % (text, uobj.host))])
                    else:
                        raise NotImplementedError('Changing field %r of a client is unsupported by this protocol.' % field)
        else:
            if field == 'HOST':
                if ircd != 'nefarious':
                    raise NotImplementedError("vHost changing for non-PyLink clients (via FAKE) is only available on nefarious, and we're using p10_ircd=%r" % ircd)
                self._send_with_prefix(self.sid, 'FA %s %s' % (target, text))
                self.apply_modes(target, [('+f', text)])
                self.mode(self.sid, target, [('+x', None)])
            else:
                raise NotImplementedError('Changing field %r of a client is unsupported by this protocol.' % field)
            self._check_cloak_change(target)

    def post_connect(self):
        """Initializes a connection to a server."""
        ts = self.start_ts
        self.send('PASS :%s' % self.serverdata['sendpass'])
        name = self.serverdata['hostname']
        self.sid = sid = p10b64encode(self.serverdata['sid'])
        desc = self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']
        self._flags = []
        p10_ircd = self.serverdata.get('p10_ircd', 'nefarious').lower()
        if p10_ircd == 'nefarious':
            cmodes = {'delayjoin':'D', 
             'registered':'R',  'key':'k',  'banexception':'e',  'redirect':'L', 
             'oplevel_apass':'A',  'oplevel_upass':'U',  'adminonly':'a', 
             'operonly':'O',  'regmoderated':'M',  'nonotice':'N',  'permanent':'z', 
             'hidequits':'Q',  'noctcp':'C',  'noamsg':'T',  'blockcolor':'c',  'stripcolor':'S', 
             'had_delayjoin':'d',  'regonly':'r',  '*A':'be', 
             '*B':'AUk',  '*C':'Ll',  '*D':'psmtinrDRaOMNzQCTcSd'}
            self.umodes.update({'servprotect':'k',  'sno_debug':'g',  'cloak':'x',  'privdeaf':'D',  'hidechans':'n', 
             'deaf_commonchan':'q',  'bot':'B',  'deaf':'d',  'hideoper':'H', 
             'hideidle':'I',  'regdeaf':'R',  'showwhois':'W',  'admin':'a', 
             'override':'X',  'noforward':'L',  'ssl':'z',  'registered':'r', 
             'cloak_sethost':'h',  'cloak_fakehost':'f',  'cloak_hashedhost':'C', 
             'cloak_hashedip':'c',  'locop':'O',  '*A':'', 
             '*B':'',  '*C':'fCcrh',  '*D':'oOiwskgxnqBdDHIRWaXLz'})
            self.extbans_matching.update({'ban_account':'~a:', 
             'ban_inchannel':'~c:', 
             'ban_realname':'~r:', 
             'ban_mark':'~m:', 
             'ban_unregistered_mark':'~M:', 
             'ban_banshare':'~j:'})
            self.extbans_acting.update({'quiet':'~q:', 
             'ban_nonick':'~n:'})
        else:
            if p10_ircd == 'snircd':
                cmodes = {'oplevel_apass':'A',  'oplevel_upass':'U',  'delayjoin':'D',  'regonly':'r',  'had_delayjoin':'d', 
                 'hidequits':'u',  'regmoderated':'M',  'blockcolor':'c',  'noctcp':'C', 
                 'nonotice':'N',  'noamsg':'T',  '*A':'b', 
                 '*B':'AUk',  '*C':'l',  '*D':'imnpstrDducCMNT'}
                self.umodes.update({'servprotect':'k',  'sno_debug':'g',  'cloak':'x',  'hidechans':'n', 
                 'deaf':'d',  'hideidle':'I',  'regdeaf':'R',  'override':'X', 
                 'registered':'r',  'cloak_sethost':'h',  'locop':'O',  '*A':'', 
                 '*B':'',  '*C':'h',  '*D':'imnpstrkgxndIRXO'})
            else:
                if p10_ircd == 'ircu':
                    cmodes = {'oplevel_apass':'A',  'oplevel_upass':'U',  'delayjoin':'D',  'regonly':'r',  'had_delayjoin':'d', 
                     'blockcolor':'c',  'noctcp':'C',  'registered':'R',  '*A':'b', 
                     '*B':'AUk',  '*C':'l',  '*D':'imnpstrDdRcC'}
                    self.umodes.update({'servprotect':'k',  'sno_debug':'g',  'cloak':'x',  'deaf':'d', 
                     'registered':'r',  'locop':'O',  '*A':'', 
                     '*B':'',  '*C':'',  '*D':'imnpstrkgxdO'})
        if self.serverdata.get('use_halfop'):
            cmodes['halfop'] = 'h'
            self.prefixmodes['h'] = '%'
        self.cmodes.update(cmodes)
        self.send('SERVER %s 1 %s %s J10 %s]]] +s6 :%s' % (name, ts, ts, sid, desc))
        self._send_with_prefix(sid, 'EB')

    def handle_server(self, source, command, args):
        """Handles incoming server introductions."""
        servername = args[0].lower()
        sid = args[5][:2]
        sdesc = args[(-1)]
        self.servers[sid] = Server(self, source, servername, desc=sdesc)
        self._flags = list(args[6])[1:]
        if self.uplink is None:
            self.uplink = sid
        return {'name':servername, 
         'sid':sid,  'text':sdesc}

    def handle_nick(self, source, command, args):
        """Handles the NICK command, used for user introductions and nick changes."""
        if len(args) > 2:
            nick = args[0]
            self._check_nick_collision(nick)
            ts, ident, host = args[2:5]
            ts = int(ts)
            realhost = host
            ip = args[(-3)]
            ip = self.decode_p10_ip(ip)
            uid = args[(-2)]
            realname = args[(-1)]
            log.debug('(%s) handle_nick got args: nick=%s ts=%s uid=%s ident=%s host=%s realname=%s realhost=%s ip=%s', self.name, nick, ts, uid, ident, host, realname, realhost, ip)
            uobj = self.users[uid] = User(self, nick, ts, uid, source, ident, host, realname, realhost, ip)
            self.servers[source].users.add(uid)
            if args[5].startswith('+'):
                modes = args[5:-3]
                parsedmodes = self.parse_modes(uid, modes)
                self.apply_modes(uid, parsedmodes)
                for modepair in parsedmodes:
                    if modepair[0][(-1)] == 'r':
                        accountname = modepair[1].split(':', 1)[0]
                        self.call_hooks([uid, 'CLIENT_SERVICES_LOGIN', {'text': accountname}])

                self._check_oper_status_change(uid, parsedmodes)
            self._check_cloak_change(uid)
            return {'uid':uid, 
             'ts':ts,  'nick':nick,  'realhost':realhost,  'host':host,  'ident':ident,  'ip':ip,  'parse_as':'UID'}
        else:
            oldnick = self.users[source].nick
            newnick = self.users[source].nick = args[0]
            self.users[source].ts = ts = int(args[1])
            return {'newnick':newnick, 
             'oldnick':oldnick,  'ts':ts}

    def _check_cloak_change(self, uid):
        """Checks for cloak changes (ident and host) on the given UID."""
        uobj = self.users[uid]
        ident = uobj.ident
        modes = dict(uobj.modes)
        log.debug('(%s) _check_cloak_change: modes of %s are %s', self.name, uid, modes)
        if 'x' not in modes:
            newhost = uobj.realhost
        else:
            if 'h' in modes:
                ident, newhost = modes['h'].split('@')
            else:
                if 'f' in modes:
                    newhost = modes['f']
                else:
                    if uobj.services_account and self.serverdata.get('use_account_cloaks'):
                        if self.serverdata.get('use_oper_account_cloaks'):
                            if 'o' in modes:
                                try:
                                    suffix = self.serverdata['oper_cloak_suffix']
                                except KeyError:
                                    raise ProtocolError('(%s) use_oper_account_cloaks was enabled, but oper_cloak_suffix was not defined!' % self.name)

                        try:
                            suffix = self.serverdata['cloak_suffix']
                        except KeyError:
                            raise ProtocolError('(%s) use_account_cloaks was enabled, but cloak_suffix was not defined!' % self.name)

                        accountname = uobj.services_account
                        newhost = '%s.%s' % (accountname, suffix)
                    elif 'C' in modes:
                        if self.serverdata.get('use_hashed_cloaks'):
                            newhost = modes['C']
                    else:
                        newhost = uobj.realhost
        if newhost != uobj.host:
            self.call_hooks([uid, 'CHGHOST', {'target':uid,  'newhost':newhost}])
        if ident != uobj.ident:
            self.call_hooks([uid, 'CHGIDENT', {'target':uid,  'newident':ident}])
        uobj.host = newhost
        uobj.ident = ident
        return newhost

    def handle_ping(self, source, command, args):
        """Handles incoming PING requests."""
        target = args[1]
        sid = self._get_SID(target)
        orig_pingtime = args[0][1:]
        currtime = time.time()
        timediff = int(time.time() - float(orig_pingtime))
        if self.is_internal_server(sid):
            self._send_with_prefix((self.sid), ('Z %s %s %s %s' % (target, orig_pingtime, timediff, currtime)), queue=False)

    def handle_pass(self, source, command, args):
        """Handles authentication with our uplink."""
        if args[0] != self.serverdata['recvpass']:
            raise ProtocolError('RECVPASS from uplink does not match configuration!')

    def handle_burst(self, source, command, args):
        """Handles the BURST command, used for bursting channels on link.

        This is equivalent to SJOIN on most IRCds."""
        if len(args) < 3:
            return
        else:
            channel = args[0]
            chandata = self._channels[channel].deepcopy()
            bans = []
            if args[(-1)].startswith('%'):
                exempts = False
                for host in args[(-1)][1:].split(' '):
                    if not host:
                        continue
                    else:
                        if host == '~':
                            exempts = True
                            continue
                    if exempts:
                        bans.append(('+e', host))
                    else:
                        bans.append(('+b', host))

                args = args[:-1]
            modestring = args[2:-1]
            if modestring:
                parsedmodes = self.parse_modes(channel, modestring)
            else:
                parsedmodes = []
            changedmodes = set(parsedmodes + bans)
            namelist = []
            prefixes = ''
            userlist = args[(-1)].split(',')
            log.debug('(%s) handle_burst: got userlist %r for %r', self.name, userlist, channel)
            if args[(-1)] != args[1]:
                for userpair in userlist:
                    try:
                        user, prefixes = userpair.split(':')
                    except ValueError:
                        user = userpair

                    log.debug('(%s) handle_burst: got mode prefixes %r for user %r', self.name, prefixes, user)
                    if user not in self.users:
                        log.warning('(%s) handle_burst: tried to introduce user %s not in our user list, ignoring...', self.name, user)
                    else:
                        namelist.append(user)
                        self.users[user].channels.add(channel)
                        changedmodes |= {('+%s' % mode, user) for mode in prefixes}
                        self._channels[channel].users.add(user)

            their_ts = int(args[1])
            our_ts = self._channels[channel].ts
            self.updateTS(source, channel, their_ts, changedmodes)
            return {'channel':channel, 
             'users':namelist,  'modes':parsedmodes,  'ts':their_ts,  'channeldata':chandata}

    def handle_join(self, source, command, args):
        """Handles incoming JOINs and channel creations."""
        try:
            ts = int(args[1])
        except IndexError:
            ts = None

        if args[0] == '0' and command == 'JOIN':
            oldchans = self.users[source].channels.copy()
            log.debug('(%s) Got /join 0 from %r, channel list is %r', self.name, source, oldchans)
            for channel in oldchans:
                self._channels[channel].users.discard(source)
                self.users[source].channels.discard(channel)

            return {'channels':oldchans, 
             'text':'Left all channels.',  'parse_as':'PART'}
        else:
            channel = args[0]
            if ts:
                self.updateTS(source, channel, ts)
            self.users[source].channels.add(channel)
            self._channels[channel].users.add(source)
            return {'channel':channel, 
             'users':[source],  'modes':self._channels[channel].modes, 
             'ts':ts or int(time.time())}

    handle_create = handle_join

    def handle_end_of_burst(self, source, command, args):
        """Handles end of burst from servers."""
        if source == self.uplink:
            self._send_with_prefix(self.sid, 'EA')
            self.connected.set()
        self.servers[source].has_eob = True
        return {}

    def handle_kick(self, source, command, args):
        """Handles incoming KICKs."""
        channel = args[0]
        kicked = args[1]
        self.handle_part(kicked, 'KICK', [channel, args[2]])
        self._send_with_prefix(kicked, 'L %s :%s' % (channel, args[2]))
        return {'channel':channel, 
         'target':kicked,  'text':args[2]}

    def handle_topic(self, source, command, args):
        """Handles TOPIC changes."""
        channel = args[0]
        topic = args[(-1)]
        oldtopic = self._channels[channel].topic
        self._channels[channel].topic = topic
        self._channels[channel].topicset = True
        return {'channel':channel, 
         'setter':args[1],  'text':topic,  'oldtopic':oldtopic}

    def handle_clearmode(self, numeric, command, args):
        """Handles CLEARMODE, which is used to clear a channel's modes."""
        channel = args[0]
        modes = args[1]
        existing = list(self._channels[channel].modes)
        for pmode, userlist in self._channels[channel].prefixmodes.items():
            modechar = self.cmodes.get(pmode)
            existing += [(modechar, user) for user in userlist]

        oldobj = self._channels[channel].deepcopy()
        changedmodes = []
        for modepair in existing:
            modechar, data = modepair
            if modechar in modes:
                if modechar in self.cmodes['*A'] + self.cmodes['*B'] + ''.join(self.prefixmodes.keys()):
                    changedmodes.append(('-%s' % modechar, data))
                else:
                    changedmodes.append(('-%s' % modechar, None))

        self.apply_modes(channel, changedmodes)
        return {'target':channel, 
         'modes':changedmodes,  'channeldata':oldobj}

    def handle_account(self, numeric, command, args):
        """Handles services account changes."""
        target = args[0]
        if self.serverdata.get('use_extended_accounts'):
            if args[1] in ('R', 'M'):
                accountname = args[2]
            else:
                if args[1] == 'U':
                    accountname = ''
                else:
                    if len(args[1]) > 1:
                        log.warning('(%s) Got subcommand %r for %s in ACCOUNT message, is use_extended_accounts set correctly?', self.name, args[1], target)
                        return
                    else:
                        return
        else:
            accountname = args[1]
        self.call_hooks([target, 'CLIENT_SERVICES_LOGIN', {'text': accountname}])
        self._check_cloak_change(target)

    def handle_fake(self, numeric, command, args):
        """Handles incoming FAKE hostmask changes."""
        target = args[0]
        text = args[1]
        self.apply_modes(target, [('+f', text)])
        self._check_cloak_change(target)

    def handle_svsnick(self, source, command, args):
        """Handles SVSNICK (forced nickname change attempts)."""
        return {'target':args[0], 
         'newnick':args[1]}

    def handle_wallchops(self, source, command, args):
        """Handles WALLCHOPS/WALLHOPS/WALLVOICES, the equivalent of @#channel
        messages and the like on P10."""
        prefix, text = args[(-1)].split(' ', 1)
        return {'target':prefix + args[0], 
         'text':text}

    handle_wallhops = handle_wallvoices = handle_wallchops


Class = P10Protocol
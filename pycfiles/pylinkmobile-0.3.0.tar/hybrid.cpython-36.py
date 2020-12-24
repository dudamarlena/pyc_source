# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/hybrid.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 12430 bytes
__doc__ = '\nhybrid.py: IRCD-Hybrid protocol module for PyLink.\n'
import time
from pylinkirc import conf, utils
from pylinkirc.classes import *
from pylinkirc.log import log
from pylinkirc.protocols.ts6 import *

class HybridProtocol(TS6Protocol):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.casemapping = 'ascii'
        self.hook_map = {'EOB':'ENDBURST',  'TBURST':'TOPIC',  'SJOIN':'JOIN'}
        self.protocol_caps -= {'slash-in-hosts'}

    def post_connect(self):
        """Initializes a connection to a server."""
        ts = self.start_ts
        f = self.send
        cmodes = {'op':'o', 
         'halfop':'h',  'voice':'v',  'ban':'b',  'key':'k',  'limit':'l', 
         'moderated':'m',  'noextmsg':'n',  'secret':'s', 
         'topiclock':'t',  'private':'p',  'blockcolor':'c', 
         'inviteonly':'i',  'noctcp':'C',  'regmoderated':'M', 
         'operonly':'O',  'regonly':'R',  'sslonly':'S', 
         'banexception':'e',  'noknock':'p',  'registered':'r', 
         'invex':'I',  'paranoia':'p',  'banexception':'e', 
         '*A':'beI', 
         '*B':'k',  '*C':'l',  '*D':'cimnprstCMORS'}
        self.cmodes = cmodes
        umodes = {'oper':'o', 
         'invisible':'i',  'wallops':'w',  'locops':'l',  'cloak':'x', 
         'hidechans':'p',  'regdeaf':'R',  'deaf':'D',  'callerid':'g', 
         'admin':'a',  'deaf_commonchan':'G',  'hideoper':'H',  'webirc':'W', 
         'sno_clientconnections':'c',  'sno_badclientconnections':'u',  'sno_rejectedclients':'j', 
         'sno_skill':'k',  'sno_fullauthblock':'f',  'sno_remoteclientconnections':'F', 
         'sno_stats':'y',  'sno_debug':'d',  'sno_nickchange':'n', 
         'hideidle':'q',  'registered':'r',  'snomask':'s', 
         'ssl':'S',  'sno_serverconnects':'e',  'sno_botfloods':'b',  '*A':'', 
         '*B':'',  '*C':'',  '*D':'DFGHRSWabcdefgijklnopqrsuwxy'}
        self.umodes = umodes
        self.extbans_matching.clear()
        self.prefixmodes = {'o':'@', 
         'h':'%',  'v':'+'}
        f('PASS %s TS 6 %s' % (self.serverdata['sendpass'], self.sid))
        f('CAPAB :TBURST DLN KNOCK UNDLN UNKLN KLN ENCAP IE EX HOPS CHW SVS CLUSTER EOB QS')
        f('SERVER %s 0 :%s' % (self.serverdata['hostname'],
         self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']))
        self.send(':%s EOB' % (self.sid,))

    def spawn_client(self, nick, ident='null', host='null', realhost=None, modes=set(), server=None, ip='0.0.0.0', realname=None, ts=None, opertype=None, manipulatable=False):
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
        u = self.users[uid] = User(self, nick, ts, uid, server, ident=ident, host=host, realname=realname, realhost=realhost,
          ip=ip,
          manipulatable=manipulatable)
        self.apply_modes(uid, modes)
        self.servers[server].users.add(uid)
        self._send_with_prefix(server, 'UID {nick} {hopcount} {ts} {modes} {ident} {host} {ip} {uid} * :{realname}'.format(ts=ts,
          host=host,
          nick=nick,
          ident=ident,
          uid=uid,
          modes=raw_modes,
          ip=ip,
          realname=realname,
          hopcount=(self.servers[server].hopcount)))
        return u

    def update_client(self, target, field, text):
        """Updates the ident, host, or realname of a PyLink client."""
        field = field.upper()
        ts = self.users[target].ts
        if field == 'HOST':
            self.users[target].host = text
            self._send_with_prefix(self.sid, 'SVSMODE %s %s +x %s' % (target, ts, text))
        else:
            raise NotImplementedError('Changing field %r of a client is unsupported by this protocol.' % field)

    def set_server_ban(self, source, duration, user='*', host='*', reason='User banned'):
        """
        Sets a server ban.
        """
        assert not user == host == '*', 'Refusing to set ridiculous ban on *@*'
        if source not in self.users:
            log.debug('(%s) Forcing KLINE sender to %s as TS6 does not allow KLINEs from servers', self.name, self.pseudoclient.uid)
            source = self.pseudoclient.uid
        self._send_with_prefix(source, 'KLINE * %s %s %s :%s' % (duration, user, host, reason))

    def topic_burst(self, numeric, target, text):
        """Sends a topic change from a PyLink server. This is usually used on burst."""
        if not self.is_internal_server(numeric):
            raise LookupError('No such PyLink server exists.')
        ts = self._channels[target].ts
        servername = self.servers[numeric].name
        self._send_with_prefix(numeric, 'TBURST %s %s %s %s :%s' % (ts, target, int(time.time()), servername, text))
        self._channels[target].topic = text
        self._channels[target].topicset = True

    def handle_capab(self, numeric, command, args):
        self._caps = caps = args[0].split()
        for required_cap in ('SVS', 'EOB', 'HOPS', 'QS', 'TBURST'):
            if required_cap not in caps:
                raise ProtocolError('%s not found in TS6 capabilities list; this is required! (got %r)' % (required_cap, caps))

    def handle_uid(self, numeric, command, args):
        """
        Handles Hybrid-style UID commands (user introduction). This is INCOMPATIBLE
        with standard TS6 implementations, as the arguments are slightly different.
        """
        nick = args[0]
        self._check_nick_collision(nick)
        ts, modes, ident, host, ip, uid, account, realname = args[2:10]
        ts = int(ts)
        if account == '*':
            account = None
        log.debug('(%s) handle_uid: got args nick=%s ts=%s uid=%s ident=%s host=%s realname=%s ip=%s', self.name, nick, ts, uid, ident, host, realname, ip)
        self.users[uid] = User(self, nick, ts, uid, numeric, ident, host, realname, host, ip)
        parsedmodes = self.parse_modes(uid, [modes])
        log.debug('(%s) handle_uid: Applying modes %s for %s', self.name, parsedmodes, uid)
        self.apply_modes(uid, parsedmodes)
        self.servers[numeric].users.add(uid)
        self._check_oper_status_change(uid, parsedmodes)
        if account:
            self.call_hooks([uid, 'CLIENT_SERVICES_LOGIN', {'text': account}])
        return {'uid':uid, 
         'ts':ts,  'nick':nick,  'realname':realname,  'host':host,  'ident':ident,  'ip':ip}

    def handle_tburst(self, numeric, command, args):
        """Handles incoming topic burst (TBURST) commands."""
        channel = args[1]
        ts = args[2]
        setter = args[3]
        topic = args[(-1)]
        self._channels[channel].topic = topic
        self._channels[channel].topicset = True
        return {'channel':channel, 
         'setter':setter,  'ts':ts,  'text':topic}

    def handle_eob(self, numeric, command, args):
        """EOB (end-of-burst) handler."""
        log.debug('(%s) end of burst received from %s', self.name, numeric)
        if not self.servers[numeric].has_eob:
            self.servers[numeric].has_eob = True
            if numeric == self.uplink:
                self.connected.set()
            return {}

    def handle_svsmode(self, numeric, command, args):
        """
        Handles SVSMODE, which is used for sending services metadata
        (vhosts, account logins), and other forced usermode changes.
        """
        target = args[0]
        ts = args[1]
        modes = args[2:]
        parsedmodes = self.parse_modes(target, modes)
        for modepair in parsedmodes:
            if modepair[0] == '+d':
                account = args[(-1)]
                if account == '*':
                    account = ''
                self.call_hooks([target, 'CLIENT_SERVICES_LOGIN', {'text': account}])
                parsedmodes.remove(modepair)
            else:
                if modepair[0] == '+x':
                    host = args[(-1)]
                    self.users[target].host = host
                    self.call_hooks([numeric, 'CHGHOST',
                     {'target':target, 
                      'newhost':host}])
                    parsedmodes.remove(modepair)

        if parsedmodes:
            self.apply_modes(target, parsedmodes)
        return {'target':target, 
         'modes':parsedmodes}


Class = HybridProtocol
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/classes.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 99233 bytes
__doc__ = '\nclasses.py - Base classes for PyLink IRC Services.\n\nThis module contains the base classes used by PyLink, including threaded IRC\nconnections and objects used to represent IRC servers, users, and channels.\n\nHere be dragons.\n'
import collections, collections.abc, functools, hashlib, ipaddress, queue, re, socket, ssl, string, textwrap, threading, time
from . import __version__, conf, selectdriver, structures, utils, world
from .log import *
from .utils import ProtocolError
QUEUE_FULL = queue.Full

class ChannelState(structures.IRCCaseInsensitiveDict):
    """ChannelState"""

    def __getitem__(self, key):
        key = self._keymangle(key)
        if key not in self._data:
            log.debug('(%s) ChannelState: creating new channel %s in memory', self._irc.name, key)
            self._data[key] = newchan = Channel(self._irc, key)
            return newchan
        else:
            return self._data[key]


class TSObject:
    """TSObject"""

    def __init__(self, *args, **kwargs):
        self._ts = int(time.time())

    @property
    def ts(self):
        return self._ts

    @ts.setter
    def ts(self, value):
        if not isinstance(value, int):
            if not isinstance(value, float):
                log.warning('TSObject: Got bad type for TS, converting from %s to int', (type(value)),
                  stack_info=True)
                value = int(value)
        self._ts = value


class User(TSObject):
    """User"""

    def __init__(self, irc, nick, ts, uid, server, ident='null', host='null', realname='PyLink dummy client', realhost='null', ip='0.0.0.0', manipulatable=False, opertype='IRC Operator'):
        super().__init__()
        self._nick = nick
        self.lower_nick = irc.to_lower(nick)
        self.ts = ts
        self.uid = uid
        self.ident = ident
        self.host = host
        self.realhost = realhost
        self.ip = ip
        self.realname = realname
        self.modes = set()
        self.server = server
        self._irc = irc
        self.account = ''
        self.opertype = opertype
        self.services_account = ''
        self.channels = structures.IRCCaseInsensitiveSet(self._irc)
        self.away = ''
        self.manipulatable = manipulatable
        self.cloaked_host = None
        self.service = None

    @property
    def nick(self):
        return self._nick

    @nick.setter
    def nick(self, newnick):
        oldnick = self.lower_nick
        self._nick = newnick
        self.lower_nick = self._irc.to_lower(newnick)
        if oldnick in self._irc.users.bynick:
            self._irc.users.bynick[oldnick].remove(self.uid)
            if not self._irc.users.bynick[oldnick]:
                del self._irc.users.bynick[oldnick]
        self._irc.users.bynick.setdefault(self.lower_nick, []).append(self.uid)

    def get_fields(self):
        """
        Returns all template/substitution-friendly fields for the User object in a read-only dictionary.
        """
        fields = self.__dict__.copy()
        for field in ('manipulatable', '_irc', 'channels', 'modes'):
            del fields[field]

        fields['sid'] = self.server
        try:
            fields['server'] = self._irc.get_friendly_name(self.server)
        except KeyError:
            pass

        fields['netname'] = self._irc.name
        fields['nick'] = self._nick
        return fields

    def __repr__(self):
        return 'User(%s/%s)' % (self.uid, self.nick)


IrcUser = User

class UserMapping(collections.abc.MutableMapping, structures.CopyWrapper):
    """UserMapping"""

    def __init__(self, irc, data=None):
        if data is not None:
            assert isinstance(data, dict)
            self._data = data
        else:
            self._data = {}
        self.bynick = collections.defaultdict(list)
        self._irc = irc

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, userobj):
        assert hasattr(userobj, 'lower_nick'), 'Cannot add object without lower_nick attribute to UserMapping'
        if key in self._data:
            log.warning('(%s) Attempting to replace User object for %r: %r -> %r', self._irc.name, key, self._data.get(key), userobj)
        self._data[key] = userobj
        self.bynick.setdefault(userobj.lower_nick, []).append(key)

    def __delitem__(self, key):
        if self[key].lower_nick in self.bynick:
            self.bynick[self[key].lower_nick].remove(key)
            if not self.bynick[self[key].lower_nick]:
                del self.bynick[self[key].lower_nick]
        del self._data[key]

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._data)

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return self._data.__contains__(key)

    def __copy__(self):
        return self.__class__((self._irc), data=(self._data.copy()))


class PyLinkNetworkCore(structures.CamelCaseToSnakeCase):
    """PyLinkNetworkCore"""

    def __init__(self, netname):
        self.loghandlers = []
        self.name = netname
        self.conf = conf.conf
        if not hasattr(self, 'sid'):
            self.sid = None
        if netname in conf.conf['servers']:
            if not hasattr(self, 'serverdata'):
                self.serverdata = conf.conf['servers'][netname]
        self.protoname = self.__class__.__module__.split('.')[(-1)]
        self.casemapping = 'rfc1459'
        self.hook_map = {}
        self.conf_keys = {
         'ip', 'port', 'hostname', 'sid', 'sidrange', 'protocol', 'sendpass',
         'recvpass'}
        self.protocol_caps = set()
        self.encoding = None
        self.connected = threading.Event()
        self._aborted = threading.Event()
        self._aborted_send = threading.Event()
        self._reply_lock = threading.RLock()
        self.autoconnect_active_multiplier = 1
        self.was_successful = False
        self._init_vars()

    def log_setup(self):
        """
        Initializes any channel loggers defined for the current network.
        """
        try:
            channels = conf.conf['logging']['channels'][self.name]
        except (KeyError, TypeError):
            return
        else:
            log.debug('(%s) Setting up channel logging to channels %r', self.name, channels)
            if not self.loghandlers:
                if not isinstance(channels, dict):
                    log.warning('(%s) Got invalid channel logging configuration %r; are your indentation and block commenting consistent?', self.name, channels)
                    return
                for channel, chandata in channels.items():
                    level = None
                    if isinstance(chandata, dict):
                        level = chandata.get('loglevel')
                    else:
                        log.warning('(%s) Got invalid channel logging pair %r: %r; are your indentation and block commenting consistent?', self.name, filename, config)
                    handler = PyLinkChannelLogger(self, channel, level=level)
                    self.loghandlers.append(handler)
                    log.addHandler(handler)

    def _init_vars(self):
        """
        (Re)sets an IRC object to its default state. This should be called when
        an IRC object is first created, and on every reconnection to a network.
        """
        self.encoding = self.serverdata.get('encoding') or 'utf-8'
        self.pseudoclient = None
        self.called_by = None
        self.called_in = None
        self.servers = {}
        self.users = UserMapping(self)
        self._channels = ChannelState(self)
        self.channels = structures.IRCCaseInsensitiveDict(self, data=(self._channels._data))
        self.cmodes = {'op':'o', 
         'secret':'s',  'private':'p',  'noextmsg':'n', 
         'moderated':'m',  'inviteonly':'i',  'topiclock':'t', 
         'limit':'l',  'ban':'b',  'voice':'v', 
         'key':'k',  '*A':'b', 
         '*B':'k', 
         '*C':'l', 
         '*D':'imnpst'}
        self.umodes = {'invisible':'i',  'snomask':'s',  'wallops':'w',  'oper':'o', 
         '*A':'', 
         '*B':'',  '*C':'',  '*D':'iosw'}
        self.extbans_acting = {}
        self.extbans_matching = {}
        self.maxnicklen = self.serverdata.get('maxnicklen', 30)
        self.prefixmodes = {'o':'@', 
         'v':'+'}
        self.uplink = None
        self.start_ts = int(time.time())
        self.log_setup()

    def __repr__(self):
        return '<%s object for network %r>' % (self.__class__.__name__, self.name)

    def validate_server_conf(self):
        pass

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def call_hooks(self, hook_args):
        """Calls a hook function with the given hook args."""
        numeric, command, parsed_args = hook_args
        if 'ts' not in parsed_args:
            parsed_args['ts'] = int(time.time())
        hook_cmd = command
        hook_map = self.hook_map
        if command in hook_map:
            hook_cmd = hook_map[command]
        hook_cmd = parsed_args.get('parse_as') or hook_cmd
        log.debug('(%s) Raw hook data: [%r, %r, %r] received from %s handler (calling hook %s)', self.name, numeric, hook_cmd, parsed_args, command, hook_cmd)
        for hook_pair in world.hooks[hook_cmd].copy():
            hook_func = hook_pair[1]
            try:
                log.debug('(%s) Calling hook function %s from plugin "%s"', self.name, hook_func, hook_func.__module__)
                retcode = hook_func(self, numeric, command, parsed_args)
                if retcode is False:
                    log.debug('(%s) Stopping hook loop for %r (command=%r)', self.name, hook_func, command)
                    break
            except Exception:
                log.exception('(%s) Unhandled exception caught in hook %r from plugin "%s"', self.name, hook_func, hook_func.__module__)
                log.error('(%s) The offending hook data was: %s', self.name, hook_args)
                continue

    def call_command(self, source, text):
        """
        Calls a PyLink bot command. source is the caller's UID, and text is the
        full, unparsed text of the message.
        """
        world.services['pylink'].call_cmd(self, source, text)

    def msg(self, target, text, notice=None, source=None, loopback=True, wrap=True):
        """Handy function to send messages/notices to clients. Source
        is optional, and defaults to the main PyLink client if not specified."""
        if not text:
            return
        else:
            if not (source or self.pseudoclient):
                return
            source = source or self.pseudoclient.uid

            def _msg(text):
                if notice:
                    self.notice(source, target, text)
                    cmd = 'PYLINK_SELF_NOTICE'
                else:
                    self.message(source, target, text)
                    cmd = 'PYLINK_SELF_PRIVMSG'
                if loopback:
                    self.call_hooks([source, cmd, {'target':target,  'text':text}])

            if wrap:
                for line in self.wrap_message(source, target, text):
                    _msg(line)

            else:
                _msg(text)

    def _reply(self, text, notice=None, source=None, private=None, force_privmsg_in_private=False, loopback=True, wrap=True):
        """
        Core of the reply() function - replies to the last caller in the right context
        (channel or PM).
        """
        if private is None:
            private = conf.conf['pylink'].get('prefer_private_replies')
        else:
            if private or self.called_in in self.users:
                if not force_privmsg_in_private:
                    notice = True
                target = self.called_by
            else:
                target = self.called_in
        self.msg(target, text, notice=notice, source=source, loopback=loopback, wrap=wrap)

    def reply(self, *args, **kwargs):
        """
        Replies to the last caller in the right context (channel or PM).

        This function wraps around _reply() and can be monkey-patched in a thread-safe manner
        to temporarily redirect plugin output to another target.
        """
        with self._reply_lock:
            (self._reply)(*args, **kwargs)

    def error(self, text, **kwargs):
        """Replies with an error to the last caller in the right context (channel or PM)."""
        (self.reply)(('Error: %s' % text), **kwargs)

    def version(self):
        """
        Returns a detailed version string including the PyLink daemon version,
        the protocol module in use, and the server hostname.
        """
        fullversion = 'PyLink-%s. %s :[protocol:%s, encoding:%s]' % (__version__, self.hostname(), self.protoname, self.encoding)
        return fullversion

    def hostname(self):
        """
        Returns the server hostname used by PyLink on the given server.
        """
        return self.serverdata.get('hostname', world.fallback_hostname)

    def get_full_network_name(self):
        """
        Returns the full network name (as defined by the "netname" option), or the
        short network name if that isn't defined.
        """
        return self.serverdata.get('netname', self.name)

    def get_service_option(self, servicename, option, default=None, global_option=None):
        """
        Returns the value of the requested service bot option on the current network, or the
        global value if it is not set for this network. This function queries and returns:

        1) If present, the value of the config option servers::<NETNAME>::<SERVICENAME>_<OPTION>
        2) If present, the value of the config option <SERVICENAME>::<GLOBAL_OPTION>, where
           <GLOBAL_OPTION> is either the 'global_option' keyword argument or <OPTION>.
        3) The default value given in the 'keyword' argument.

        While service bot and config option names can technically be uppercase or mixed case,
        the convention is to define them in all lowercase characters.
        """
        netopt = self.serverdata.get('%s_%s' % (servicename, option))
        if netopt is not None:
            return netopt
        else:
            if global_option is not None:
                option = global_option
            globalopt = conf.conf.get(servicename, {}).get(option)
            if globalopt is not None:
                return globalopt
            return default

    def get_service_options(self, servicename: str, option: str, itertype: type, global_option=None):
        """
        Returns a merged copy of the requested service bot option. This includes:

        1) If present, the value of the config option servers::<NETNAME>::<SERVICENAME>_<OPTION> (netopt)
        2) If present, the value of the config option <SERVICENAME>::<GLOBAL_OPTION>, where
           <GLOBAL_OPTION> is either the 'global_option' keyword value or <OPTION> (globalopt)

        For itertype, the following types are allowed:
            - list: items are combined as globalopt + netopt
            - dict: items are combined as {**globalopt, **netopt}
        """
        netopt = self.serverdata.get('%s_%s' % (servicename, option)) or itertype()
        globalopt = conf.conf.get(servicename, {}).get(global_option or option) or itertype()
        return utils.merge_iterables(globalopt, netopt)

    def has_cap(self, capab):
        """
        Returns whether this protocol module instance has the requested capability.
        """
        return capab.lower() in self.protocol_caps

    def _pre_connect(self):
        """
        Implements triggers called before a network connects.
        """
        self._aborted_send.clear()
        self._aborted.clear()
        self._init_vars()
        try:
            self.validate_server_conf()
        except Exception as e:
            log.error('(%s) Configuration error: %s', self.name, e)
            raise

    def _run_autoconnect(self):
        """Blocks for the autoconnect time and returns True if autoconnect is enabled."""
        if world.shutting_down.is_set():
            log.debug('(%s) _run_autoconnect: aborting autoconnect attempt since we are shutting down.', self.name)
            return
        else:
            autoconnect = self.serverdata.get('autoconnect')
            autoconnect_multiplier = self.serverdata.get('autoconnect_multiplier', 2)
            autoconnect_max = self.serverdata.get('autoconnect_max', 1800)
            autoconnect_multiplier = max(autoconnect_multiplier, 1)
            autoconnect_max = max(autoconnect_max, 1)
            log.debug('(%s) _run_autoconnect: Autoconnect delay set to %s seconds.', self.name, autoconnect)
            if autoconnect is not None:
                if autoconnect >= 1:
                    log.debug('(%s) _run_autoconnect: Multiplying autoconnect delay %s by %s.', self.name, autoconnect, self.autoconnect_active_multiplier)
                    autoconnect *= self.autoconnect_active_multiplier
                    autoconnect = min(autoconnect, autoconnect_max)
                    log.info('(%s) _run_autoconnect: Going to auto-reconnect in %s seconds.', self.name, autoconnect)
                    self._aborted.clear()
                    self._aborted.wait(autoconnect)
                    self.autoconnect_active_multiplier *= autoconnect_multiplier
                    if self not in world.networkobjects.values():
                        log.debug('(%s) _run_autoconnect: Stopping stale connect loop', self.name)
                        return
                    return True
            log.debug('(%s) _run_autoconnect: Stopping connect loop (autoconnect value %r is < 1).', self.name, autoconnect)
            return

    def _pre_disconnect(self):
        """
        Implements triggers called before a network disconnects.
        """
        self._aborted.set()
        self.was_successful = self.connected.is_set()
        log.debug('(%s) _pre_disconnect: got %s for was_successful state', self.name, self.was_successful)
        log.debug('(%s) _pre_disconnect: Clearing self.connected state.', self.name)
        self.connected.clear()
        log.debug('(%s) _pre_disconnect: Removing channel logging handlers due to disconnect.', self.name)
        while self.loghandlers:
            log.removeHandler(self.loghandlers.pop())

    def _post_disconnect(self):
        """
        Implements triggers called after a network disconnects.
        """
        self.call_hooks([None, 'PYLINK_DISCONNECT', {'was_successful': self.was_successful}])
        self.to_lower.cache_clear()

    def _remove_client(self, numeric):
        """
        Internal function to remove a client from our internal state.

        If the removal was successful, return the User object for the given numeric (UID)."""
        for c, v in self.channels.copy().items():
            v.remove_user(numeric)
            if not (self.channels[c].users or (self.cmodes.get('permanent'), None) in self.channels[c].modes):
                del self.channels[c]

        sid = self.get_server(numeric)
        try:
            userobj = self.users[numeric]
            del self.users[numeric]
            self.servers[sid].users.discard(numeric)
        except KeyError:
            log.debug('(%s) Skipping removing client %s that no longer exists', (self.name), numeric, exc_info=True)
        else:
            log.debug('(%s) Removing client %s from user + server state', self.name, numeric)
            return userobj

    def nick_to_uid(self, nick, multi=False, filterfunc=None):
        """Looks up the UID of a user with the given nick, or return None if no such nick exists.

        If multi is given, return all matches for nick instead of just the last result. (Return an empty list if no matches)
        If filterfunc is given, filter matched users by the given function first."""
        nick = self.to_lower(nick)
        uids = self.users.bynick.get(nick, [])
        if filterfunc:
            uids = list(filter(filterfunc, uids))
        if multi:
            return uids
        if len(uids) > 1:
            log.warning('(%s) Multiple UIDs found for nick %r: %r; using the last one!', self.name, nick, uids)
        try:
            return uids[(-1)]
        except IndexError:
            return

    def is_internal_client(self, uid):
        """
        Returns whether the given UID is a PyLink client.

        This returns False if the numeric doesn't exist.
        """
        sid = self.get_server(uid)
        if sid:
            if self.servers[sid].internal:
                return True
        return False

    def is_internal_server(self, sid):
        """Returns whether the given SID is an internal PyLink server."""
        return sid in self.servers and self.servers[sid].internal

    def get_server(self, uid):
        """Finds the ID of the server a user is on. Return None if the user does not exist."""
        userobj = self.users.get(uid)
        if userobj:
            return userobj.server

    def is_manipulatable_client(self, uid):
        """
        Returns whether the given client is marked manipulatable for interactions
        such as force-JOIN.
        """
        return self.is_internal_client(uid) and self.users[uid].manipulatable

    def get_service_bot(self, uid):
        """
        Checks whether the given UID exists and is a registered service bot.

        If True, returns the corresponding ServiceBot object.
        Otherwise, return False.
        """
        userobj = self.users.get(uid)
        if not userobj:
            return False
        else:
            sname = userobj.service
            if sname is not None:
                if sname not in world.services.keys():
                    log.warning("(%s) User %s / %s had a service bot record to a service that doesn't exist (%s)!", self.name, uid, userobj.nick, sname)
            return world.services.get(sname)


structures._BLACKLISTED_COPY_TYPES.append(PyLinkNetworkCore)

class PyLinkNetworkCoreWithUtils(PyLinkNetworkCore):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._ts_lock = threading.Lock()

    @functools.lru_cache(maxsize=8192)
    def to_lower(self, text):
        """
        Returns the lowercase representation of text. This respects IRC casemappings defined by the protocol module.
        """
        if not text or not isinstance(text, str):
            return text
        else:
            if self.casemapping == 'rfc1459':
                text = text.replace('{', '[')
                text = text.replace('}', ']')
                text = text.replace('|', '\\')
                text = text.replace('~', '^')
            return text.encode().lower().decode()

    _NICK_REGEX = '^[A-Za-z\\|\\\\_\\[\\]\\{\\}\\^\\`][A-Z0-9a-z\\-\\|\\\\_\\[\\]\\{\\}\\^\\`]*$'

    @classmethod
    def is_nick(cls, s, nicklen=None):
        """
        Returns whether the string given is a valid nick.

        Other platforms SHOULD redefine this if their definition of a valid nick is different."""
        if nicklen:
            if len(s) > nicklen:
                return False
        return bool(re.match(cls._NICK_REGEX, s))

    @staticmethod
    def is_channel(obj):
        """
        Returns whether the item given is a valid channel (for a mapping key).

        For IRC, this checks if the item's name starts with a "#".

        Other platforms SHOULD redefine this if they track channels by some other format (e.g. numerical IDs).
        """
        return str(obj).startswith('#')

    _HOSTNAME_RE = re.compile('^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)+([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9])*$')

    @classmethod
    def is_server_name(cls, text):
        """Returns whether the string given is a valid server name."""
        return bool(cls._HOSTNAME_RE.match(text))

    _HOSTMASK_RE = re.compile('^\\S+!\\S+@\\S+$')

    @classmethod
    def is_hostmask(cls, text):
        """
        Returns whether the given text is a valid hostmask (nick!user@host)

        Other protocols may redefine this to meet their definition of hostmask
        (i.e. some unique identifier for a user).
        """
        return bool(cls._HOSTMASK_RE.match(text) and '#' not in text)

    def _get_SID(self, sname):
        """Returns the SID of a server with the given name, if present."""
        name = sname.lower()
        if name in self.servers:
            return name
        for k, v in self.servers.items():
            if v.name.lower() == name:
                return k
        else:
            return sname

    def _get_UID(self, target):
        """
        Converts a nick argument to its matching UID. This differs from nick_to_uid()
        in that it returns the original text instead of None if no matching nick is found.

        Subclasses like Clientbot may override this to tweak the nick lookup behaviour,
        e.g. by filtering virtual clients out.
        """
        if target in self.users:
            return target
        else:
            target = self.nick_to_uid(target) or target
            return target

    def _squit(self, numeric, command, args):
        """Handles incoming SQUITs."""
        split_server = self._get_SID(args[0])
        if split_server in (self.sid, self.uplink):
            raise ProtocolError('SQUIT received: (reason: %s)' % args[(-1)])
        affected_users = []
        affected_servers = [split_server]
        affected_nicks = collections.defaultdict(list)
        log.debug('(%s) Splitting server %s (reason: %s)', self.name, split_server, args[(-1)])
        if split_server not in self.servers:
            log.warning("(%s) Tried to split a server (%s) that didn't exist!", self.name, split_server)
            return
        else:
            old_servers = self.servers.copy()
            old_channels = self._channels.copy()
            for sid, data in old_servers.items():
                if data.uplink == split_server:
                    log.debug('Server %s also hosts server %s, removing those users too...', split_server, sid)
                    args = self._squit(sid, 'SQUIT', [sid, '0',
                     'PyLink: Automatically splitting leaf servers of %s' % sid])
                    affected_users += args['users']
                    affected_servers += args['affected_servers']

            for user in self.servers[split_server].users.copy():
                affected_users.append(user)
                nick = self.users[user].nick
                for name, cdata in old_channels.items():
                    if user in cdata.users:
                        affected_nicks[name].append(nick)

                log.debug('Removing client %s (%s)', user, nick)
                self._remove_client(user)

            serverdata = self.servers[split_server]
            sname = serverdata.name
            uplink = serverdata.uplink
            del self.servers[split_server]
            log.debug('(%s) Netsplit affected users: %s', self.name, affected_users)
            return {'target':split_server, 
             'users':affected_users,  'name':sname,  'uplink':uplink, 
             'nicks':affected_nicks,  'serverdata':serverdata,  'channeldata':old_channels, 
             'affected_servers':affected_servers}

    @staticmethod
    def _log_debug_modes(*args, **kwargs):
        """
        Log debug info related to mode parsing if enabled.
        """
        if conf.conf['pylink'].get('log_mode_parsers'):
            (log.debug)(*args, **kwargs)

    def _parse_modes(self, args, existing, supported_modes, is_channel=False, prefixmodes=None, ignore_missing_args=False):
        """
        parse_modes() core.

        args: A mode string or a mode string split by space (type list)
        existing: A set or iterable of existing modes
        supported_modes: a dict of PyLink supported modes (mode names mapping
                         to mode chars, with *ABCD keys)
        prefixmodes: a dict of prefix modes (irc.prefixmodes style)
        """
        prefix = ''
        if isinstance(args, str):
            args = args.split()
        elif not args:
            raise AssertionError('No valid modes were supplied!')
        modestring = args[0]
        args = args[1:]
        existing = set(existing)
        existing_casemap = {}
        for modepair in existing:
            arg = modepair[1]
            if arg is not None:
                existing_casemap[(modepair[0], self.to_lower(arg))] = modepair
            else:
                existing_casemap[modepair] = modepair

        res = []
        for mode in modestring:
            if mode in '+-':
                prefix = mode
            else:
                if not prefix:
                    prefix = '+'
                arg = None
                self._log_debug_modes('Current mode: %s%s; args left: %s', prefix, mode, args)
                try:
                    if prefixmodes and mode in self.prefixmodes:
                        self._log_debug_modes('Mode %s: This mode is a prefix mode.', mode)
                        arg = args.pop(0)
                        arg = self._get_UID(arg)
                        if arg not in self.users:
                            self._log_debug_modes('(%s) Skipping setting mode "%s %s"; the target doesn\'t seem to exist!', self.name, mode, arg)
                            continue
                    else:
                        if mode in supported_modes['*A'] + supported_modes['*B']:
                            self._log_debug_modes('Mode %s: This mode must have parameter.', mode)
                            arg = args.pop(0)
                            if prefix == '-':
                                if mode in supported_modes['*B']:
                                    if arg == '*':
                                        oldarg = dict(existing).get(mode)
                                        if oldarg:
                                            arg = oldarg
                                            self._log_debug_modes("Mode %s: coersing argument of '*' to %r.", mode, arg)
                                self._log_debug_modes('(%s) parse_modes: checking if +%s %s is in old modes list: %s; existing_casemap=%s', self.name, mode, arg, existing, existing_casemap)
                                arg = self.to_lower(arg)
                                casefolded_modepair = existing_casemap.get((mode, arg))
                                if casefolded_modepair not in existing:
                                    self._log_debug_modes('(%s) parse_modes: ignoring removal of non-existent list mode +%s %s; casefolded_modepair=%s', self.name, mode, arg, casefolded_modepair)
                                    continue
                                arg = casefolded_modepair[1]
                        else:
                            if prefix == '+':
                                if mode in supported_modes['*C']:
                                    self._log_debug_modes('Mode %s: Only has parameter when setting.', mode)
                                    arg = args.pop(0)
                except IndexError:
                    logfunc = self._log_debug_modes if ignore_missing_args else log.warning
                    logfunc('(%s) Error while parsing mode %r: mode requires an argument but none was found. (modestring: %r)', self.name, mode, modestring)
                    continue

                newmode = (
                 prefix + mode, arg)
                res.append(newmode)
                existing = self._apply_modes(existing, [newmode], is_channel=is_channel)
                lowered_mode = (
                 newmode[0][(-1)], self.to_lower(newmode[1]) if newmode[1] else newmode[1])
                if prefix == '+' and lowered_mode not in existing_casemap:
                    existing_casemap[lowered_mode] = (
                     mode, arg)
                else:
                    if prefix == '-' and lowered_mode in existing_casemap:
                        del existing_casemap[lowered_mode]

        return res

    def parse_modes(self, target, args, ignore_missing_args=False):
        """Parses a modestring list into a list of (mode, argument) tuples.
        ['+mitl-o', '3', 'person'] => [('+m', None), ('+i', None), ('+t', None), ('+l', '3'), ('-o', 'person')]
        """
        is_channel = self.is_channel(target)
        if not is_channel:
            self._log_debug_modes('(%s) Using self.umodes for this query: %s', self.name, self.umodes)
            if target not in self.users:
                self._log_debug_modes('(%s) Possible desync! Mode target %s is not in the users index.', self.name, target)
                return []
            supported_modes = self.umodes
            oldmodes = self.users[target].modes
            prefixmodes = None
        else:
            self._log_debug_modes('(%s) Using self.cmodes for this query: %s', self.name, self.cmodes)
            supported_modes = self.cmodes
            oldmodes = self._channels[target].modes
            prefixmodes = self._channels[target].prefixmodes
        return self._parse_modes(args, oldmodes, supported_modes, is_channel=is_channel, prefixmodes=prefixmodes,
          ignore_missing_args=ignore_missing_args)

    def _apply_modes(self, old_modelist, changedmodes, is_channel=False, prefixmodes=None):
        """
        Takes a list of parsed IRC modes, and applies them onto the given target mode list.
        """
        modelist = set(old_modelist)
        mapping = collections.defaultdict(set)
        if is_channel:
            supported_modes = self.cmodes
        else:
            supported_modes = self.umodes
        for modepair in modelist:
            mapping[modepair[0]].add(modepair[1])

        for mode in changedmodes:
            try:
                real_mode = (
                 mode[0][1], mode[1])
            except IndexError:
                real_mode = mode

            if is_channel:
                if prefixmodes is not None:
                    for pmode, pmodelist in prefixmodes.items():
                        if pmode in supported_modes and real_mode[0] == supported_modes[pmode]:
                            if mode[0][0] == '+':
                                pmodelist.add(mode[1])
                            else:
                                pmodelist.discard(mode[1])

                if real_mode[0] in self.prefixmodes:
                    self._log_debug_modes("(%s) Not adding mode %s to Channel.modes because it's a prefix mode.", self.name, str(mode))
                    continue
            if mode[0][0] != '-':
                self._log_debug_modes('(%s) Adding mode %r on %s', self.name, real_mode, modelist)
                existing = mapping.get(real_mode[0])
                if existing:
                    if real_mode[0] not in supported_modes['*A']:
                        self._log_debug_modes('(%s) Old modes for mode %r exist in %s, removing them: %s', self.name, real_mode, modelist, str(existing))
                        while existing:
                            oldvalue = existing.pop()
                            modelist.discard((real_mode[0], oldvalue))

                modelist.add(real_mode)
                mapping[real_mode[0]].add(real_mode[1])
            else:
                self._log_debug_modes('(%s) Removing mode %r from %s', self.name, real_mode, modelist)
                existing = mapping.get(real_mode[0])
                arg = real_mode[1]
                if real_mode[0] in supported_modes['*A'] + supported_modes['*B']:
                    modelist.discard((real_mode[0], self.to_lower(arg)))
                else:
                    while existing:
                        oldvalue = existing.pop()
                        if arg is None or self.to_lower(arg) == self.to_lower(oldvalue):
                            modelist.discard((real_mode[0], oldvalue))

        self._log_debug_modes('(%s) Final modelist: %s', self.name, modelist)
        return modelist

    def apply_modes(self, target, changedmodes):
        """Takes a list of parsed IRC modes, and applies them on the given target.

        The target can be either a channel or a user; this is handled automatically."""
        is_channel = self.is_channel(target)
        prefixmodes = None
        try:
            if is_channel:
                c = self._channels[target]
                old_modelist = c.modes
                prefixmodes = c.prefixmodes
            else:
                old_modelist = self.users[target].modes
        except KeyError:
            log.warning('(%s) Possible desync? Mode target %s is unknown.', self.name, target)
            return
        else:
            modelist = self._apply_modes(old_modelist, changedmodes, is_channel=is_channel, prefixmodes=prefixmodes)
            try:
                if is_channel:
                    self._channels[target].modes = modelist
                else:
                    self.users[target].modes = modelist
            except KeyError:
                log.warning('(%s) Invalid MODE target %s (is_channel=%s)', self.name, target, is_channel)

    @staticmethod
    def _flip(mode):
        """Flips a mode character."""
        mode = list(mode)
        if mode[0] == '-':
            mode[0] = '+'
        else:
            if mode[0] == '+':
                mode[0] = '-'
            else:
                mode.insert(0, '-')
        return ''.join(mode)

    def reverse_modes(self, target, modes, oldobj=None):
        """
        IRC specific: Reverses/inverts the mode string or mode list given.

        Optionally, an oldobj argument can be given to look at an earlier state of
        a channel/user object, e.g. for checking the op status of a mode setter
        before their modes are processed and added to the channel state.

        This function allows both mode strings or mode lists. Example uses:
            "+mi-lk test => "-mi+lk test"
            "mi-k test => "-mi+k test"
            [('+m', None), ('+r', None), ('+l', '3'), ('-o', 'person')
             => [('-m', None), ('-r', None), ('-l', None), ('+o', 'person')}]
            {('s', None), ('+o', 'whoever') => [('-s', None), ('-o', 'whoever')}]
        """
        origstring = isinstance(modes, str)
        if origstring:
            modes = self.parse_modes(target, modes.split(' '))
        else:
            if self.is_channel(target):
                c = oldobj or self._channels[target]
                oldmodes = c.modes.copy()
                possible_modes = self.cmodes.copy()
                possible_modes['*A'] += ''.join(self.prefixmodes)
                for name, userlist in c.prefixmodes.items():
                    try:
                        oldmodes |= {(self.cmodes[name], u) for u in userlist}
                    except KeyError:
                        continue

            else:
                oldmodes = set(self.users[target].modes)
                possible_modes = self.umodes
        oldmodes_mapping = dict(oldmodes)
        oldmodes_lower = {(modepair[0], self.to_lower(modepair[1]) if modepair[1] else modepair[1]) for modepair in oldmodes}
        newmodes = []
        self._log_debug_modes('(%s) reverse_modes: old/current mode list for %s is: %s', self.name, target, oldmodes)
        for char, arg in modes:
            mchar = char[(-1)]
            if mchar in possible_modes['*B'] + possible_modes['*C']:
                oldarg = oldmodes_mapping.get(mchar)
                if oldarg:
                    mpair = (
                     '+%s' % mchar, oldarg)
                else:
                    if mchar in possible_modes['*C']:
                        if char[0] != '-':
                            arg = None
                    mpair = (
                     self._flip(char), arg)
            else:
                mpair = (
                 self._flip(char), arg)
            if arg is not None:
                arg = self.to_lower(arg)
            if char[0] != '-':
                if (mchar, arg) in oldmodes:
                    self._log_debug_modes("(%s) reverse_modes: skipping reversing '%s %s' with %s since we're setting a mode that's already set.", self.name, char, arg, mpair)
                    continue
            if char[0] == '-':
                if (mchar, arg) not in oldmodes:
                    if mchar in possible_modes['*A']:
                        self._log_debug_modes("(%s) reverse_modes: skipping reversing '%s %s' with %s since it wasn't previously set.", self.name, char, arg, mpair)
                        continue
            if char[0] == '-':
                if mchar not in oldmodes_mapping:
                    self._log_debug_modes("(%s) reverse_modes: skipping reversing '%s %s' with %s since it wasn't previously set.", self.name, char, arg, mpair)
                    continue
            if mpair in newmodes:
                self._log_debug_modes('(%s) reverse_modes: skipping duplicate reverse mode %s', self.name, mpair)
                continue
            newmodes.append(mpair)

        self._log_debug_modes('(%s) reverse_modes: new modes: %s', self.name, newmodes)
        if origstring:
            return self.join_modes(newmodes)
        else:
            return newmodes

    @staticmethod
    def join_modes(modes, sort=False):
        """
        IRC specific: Takes a list of (mode, arg) tuples in parse_modes() format, and
        joins them into a string.
        """
        prefix = '+'
        modelist = ''
        args = []
        if sort:
            modes = sorted(modes)
        for modepair in modes:
            mode, arg = modepair
            assert len(mode) in (1, 2), 'Incorrect length of a mode (received %r)' % mode
            try:
                curr_prefix, mode = mode
            except ValueError:
                pass

            if prefix != curr_prefix:
                modelist += curr_prefix
                prefix = curr_prefix
            modelist += mode
            if arg is not None:
                args.append(arg)

        if not modelist.startswith(('+', '-')):
            modelist = '+' + modelist
        if args:
            modelist += ' '
            modelist += ' '.join(str(arg) for arg in args)
        return modelist

    @classmethod
    def wrap_modes(cls, modes, limit, max_modes_per_msg=0):
        """
        IRC specific: Takes a list of modes and wraps it across multiple lines.
        """
        strings = []
        queued_modes = []
        total_length = 0
        last_prefix = '+'
        orig_modes = modes.copy()
        modes = list(modes)
        while modes:
            next_mode = modes.pop(0)
            modechar, arg = next_mode
            prefix = modechar[0]
            if prefix not in '+-':
                prefix = last_prefix
                modechar = prefix + modechar
                next_mode = (
                 modechar, arg)
            next_length = 1
            if prefix != last_prefix:
                next_length += 1
            last_prefix = prefix
            if arg:
                next_length += 1
                next_length += len(arg)
            assert next_length <= limit, 'wrap_modes: Mode %s is too long for the given length %s' % (next_mode, limit)
            if next_length + total_length <= limit and (not max_modes_per_msg or len(queued_modes) < max_modes_per_msg):
                total_length += next_length
                cls._log_debug_modes('wrap_modes: Adding mode %s to queued modes', str(next_mode))
                queued_modes.append(next_mode)
                cls._log_debug_modes('wrap_modes: queued modes: %s', queued_modes)
            else:
                strings.append(cls.join_modes(queued_modes))
                queued_modes.clear()
                cls._log_debug_modes('wrap_modes: cleared queue (length %s) and now adding %s', limit, str(next_mode))
                queued_modes.append(next_mode)
                total_length = next_length
        else:
            strings.append(cls.join_modes(queued_modes))

        cls._log_debug_modes('wrap_modes: returning %s for %s', strings, orig_modes)
        return strings

    def get_hostmask(self, user, realhost=False, ip=False):
        """
        Returns a representative hostmask / user friendly identifier for a user.
        On IRC, this is nick!user@host; other platforms may choose to define a different
        style for user hostmasks.

        If the realhost option is given, prefer showing the real host of the user instead
        of the displayed host.
        If the ip option is given, prefering showing the IP address of the user (this overrides
        realhost)."""
        userobj = self.users.get(user)
        try:
            nick = userobj.nick
        except AttributeError:
            nick = '<unknown-nick>'

        try:
            ident = userobj.ident
        except AttributeError:
            ident = '<unknown-ident>'

        try:
            if ip:
                host = userobj.ip
            else:
                if realhost:
                    host = userobj.realhost
                else:
                    host = userobj.host
        except AttributeError:
            host = '<unknown-host>'

        return '%s!%s@%s' % (nick, ident, host)

    def get_friendly_name(self, entityid):
        """
        Returns the display name of an entity:

        For servers, this returns the server name given a SID.
        For users, this returns a nick given the UID.
        For channels, return the channel name (returned as-is for IRC).
        """
        if entityid in self.servers:
            return self.servers[entityid].name
        else:
            if entityid in self.users:
                return self.users[entityid].nick
            if self.is_channel(entityid.lstrip(''.join(self.prefixmodes.values()))):
                return entityid
        raise KeyError('Unknown UID/SID %s' % entityid)

    def is_privileged_service(self, entityid):
        """
        Returns whether the given UID and SID belongs to a privileged service.

        For IRC, this reads the 'ulines' option in the server configuration. Other platforms
        may override this to suit their needs.
        """
        ulines = self.serverdata.get('ulines', [])
        if entityid in self.users:
            sid = self.get_server(entityid)
        else:
            sid = entityid
        return self.get_friendly_name(sid) in ulines

    def is_oper(self, uid, **kwargs):
        """
        Returns whether the given user has operator / server administration status.
        For IRC, this checks usermode +o. Other platforms may choose to define this another way.

        The allowAuthed and allowOper keyword arguments are deprecated since PyLink 2.0-alpha4.
        """
        if 'allowAuthed' in kwargs or 'allowOper' in kwargs:
            log.warning('(%s) is_oper: the "allowAuthed" and "allowOper" options are deprecated as of PyLink 2.0-alpha4 and now imply False and True respectively. To check forPyLink account status, instead check the User.account attribute directly.', self.name)
        if uid in self.users:
            if ('o', None) in self.users[uid].modes:
                return True
        return False

    def match_host(self, glob, target, ip=True, realhost=True):
        """
        Checks whether the given host or given UID's hostmask matches the given glob
        (nick!user@host for IRC). PyLink extended targets are also supported.

        If the target given is a UID, and the 'ip' or 'realhost' options are True, this will also
        match against the target's IP address and real host, respectively.

        This function respects IRC casemappings (rfc1459 and ascii). If the given target is a UID,
        and the 'ip' option is enabled, the host portion of the glob is also matched as a CIDR range.
        """
        invert = glob.startswith('!')
        if invert:
            glob = glob.lstrip('!')

        def match_host_core():
            nonlocal glob
            if target in self.users:
                if not self.is_hostmask(glob):
                    for specialchar in '$:()':
                        if specialchar in glob:
                            break
                    else:
                        log.debug('(%s) Using target $pylinkacc:%s instead of raw string %r', self.name, glob, glob)
                        glob = '$pylinkacc:' + glob

                else:
                    if glob.startswith('$'):
                        glob = glob.lstrip('$')
                        exttargetname = glob.split(':', 1)[0]
                        handler = world.exttarget_handlers.get(exttargetname)
                        if handler:
                            result = handler(self, glob, target)
                            log.debug('(%s) Got %s from exttarget %s in match_host() glob $%s for target %s', self.name, result, exttargetname, glob, target)
                            return result
                        else:
                            log.debug('(%s) Unknown exttarget %s in match_host() glob $%s', self.name, exttargetname, glob)
                            return False
                    hosts = {
                     self.get_hostmask(target)}
                    if ip:
                        hosts.add(self.get_hostmask(target, ip=True))
                        try:
                            header, cidrtarget = glob.split('@', 1)
                            network = ipaddress.ip_network(cidrtarget)
                            real_ip = self.users[target].ip
                            if ipaddress.ip_address(real_ip) in network:
                                glob = '@'.join((header, real_ip))
                                log.debug('(%s) Found matching CIDR %s for %s, replacing target glob with IP %s', self.name, cidrtarget, target, real_ip)
                        except ValueError:
                            pass

                if realhost:
                    hosts.add(self.get_hostmask(target, realhost=True))
            else:
                hosts = [
                 target]
            for host in hosts:
                if self.match_text(glob, host):
                    return True

            return False

        result = match_host_core()
        if invert:
            result = not result
        return result

    def match_text(self, glob, text):
        """
        Returns whether the given glob matches the given text under the network's current case mapping.
        """
        return utils.match_text(glob, text, filterfunc=(self.to_lower))

    def match_all(self, banmask, channel=None):
        """
        Returns all users matching the target hostmask/exttarget. Users can also be filtered by channel.
        """
        if channel:
            banmask = '$and:(%s+$channel:%s)' % (banmask, channel)
        for uid, userobj in self.users.copy().items():
            if self.match_host(banmask, uid) and uid in self.users:
                yield uid

    def match_all_re(self, re_mask, channel=None):
        """
        Returns all users whose "nick!user@host [gecos]" mask matches the given regular expression. Users can also be filtered by channel.
        """
        regexp = re.compile(re_mask)
        for uid, userobj in self.users.copy().items():
            target = '%s [%s]' % (self.get_hostmask(uid), userobj.realname)
            if regexp.fullmatch(target) and (not channel or channel in userobj.channels):
                yield uid

    def make_channel_ban(self, uid, ban_type='ban', ban_style=None):
        """Creates a hostmask-based ban for the given user.

        Ban exceptions, invite exceptions quiets, and extbans are also supported by setting ban_type
        to the appropriate PyLink named mode (e.g. "ban", "banexception", "invex", "quiet", "ban_nonick")."""
        if not uid in self.users:
            raise AssertionError('Unknown user %s' % uid)
        else:
            ban_style = ban_style or self.serverdata.get('ban_style') or conf.conf['pylink'].get('ban_style') or '*!*@$host'
            template = string.Template(ban_style)
            banhost = template.safe_substitute(self.users[uid].get_fields())
            if not self.is_hostmask(banhost):
                raise ValueError('Ban mask %r is not a valid hostmask!' % banhost)
            if ban_type in self.cmodes:
                return ('+%s' % self.cmodes[ban_type], banhost)
            if ban_type in self.extbans_acting:
                return ('+%s' % self.cmodes['ban'], self.extbans_acting[ban_type] + banhost)
        raise ValueError('ban_type %r is not available on IRCd %r' % (ban_type, self.protoname))

    def updateTS(self, sender, channel, their_ts, modes=None):
        """
        IRC specific: Merges modes of a channel given the remote TS and a list of modes.
        """
        if modes is None:
            modes = []

        def _clear():
            log.debug('(%s) Clearing local modes from channel %s due to TS change', self.name, channel)
            self._channels[channel].modes.clear()
            for p in self._channels[channel].prefixmodes.values():
                for user in p.copy():
                    if not self.is_internal_client(user):
                        p.discard(user)

        def _apply():
            if modes:
                log.debug('(%s) Applying modes on channel %s (TS ok)', self.name, channel)
                self.apply_modes(channel, modes)

        with self._ts_lock:
            our_ts = self._channels[channel].ts
            assert isinstance(our_ts, int), 'Wrong type for our_ts (expected int, got %s)' % type(our_ts)
            assert isinstance(their_ts, int), 'Wrong type for their_ts (expected int, got %s)' % type(their_ts)
            our_mode = self.is_internal_client(sender) or self.is_internal_server(sender)
            log.debug('(%s/%s) our_ts: %s; their_ts: %s; is the mode origin us? %s', self.name, channel, our_ts, their_ts, our_mode)
            if their_ts == our_ts:
                log.debug('(%s/%s) remote TS of %s is equal to our %s; mode query %s', self.name, channel, their_ts, our_ts, modes)
                _apply()
            else:
                if their_ts < our_ts:
                    if their_ts < 750000:
                        if their_ts != 0:
                            if self.serverdata.get('ignore_ts_errors'):
                                log.debug('(%s) Silently ignoring bogus TS %s on channel %s', self.name, their_ts, channel)
                            else:
                                log.warning('(%s) Possible desync? Not setting bogus TS %s on channel %s', self.name, their_ts, channel)
                    else:
                        log.debug('(%s) Resetting channel TS of %s from %s to %s (remote has lower TS)', self.name, channel, our_ts, their_ts)
                        self._channels[channel].ts = their_ts
                    _clear()
                    _apply()

    def _check_nick_collision(self, nick):
        """
        IRC specific: Nick collision preprocessor for user introductions.

        If the given nick matches an existing UID, send out a SAVE hook payload indicating a nick collision.
        """
        uid = self.nick_to_uid(nick)
        if uid:
            log.info('(%s) Nick collision on %s/%s, forwarding this to plugins', self.name, uid, nick)
            self.call_hooks([self.sid, 'SAVE', {'target': uid}])

    def _expandPUID(self, entityid):
        """
        Returns the nick or server name for the given UID/SID. This method helps support protocol
        modules that use PUIDs internally, as they must convert them to talk with the uplink.
        """
        if isinstance(entityid, str) and '@' in entityid:
            name = self.get_friendly_name(entityid)
            log.debug('(%s) _expandPUID: mangling pseudo ID %s to %s', self.name, entityid, name)
            return name
        else:
            return entityid

    def wrap_message(self, source, target, text):
        """
        Wraps the given message text into multiple lines (length depends on how much the protocol
        allows), and returns these as a list.
        """
        raise NotImplementedError


KEEPALIVE_MAX_MISSED = 2

class IRCNetwork(PyLinkNetworkCoreWithUtils):
    S2S_BUFSIZE = 510

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._queue = None
        self._ping_timer = None
        self._socket = None
        self._selector_key = None
        self._buffer = bytearray()
        self._reconnect_thread = None
        self._queue_thread = None

    def _init_vars(self, *args, **kwargs):
        (super()._init_vars)(*args, **kwargs)
        self.lastping = time.time()
        self.pingfreq = self.serverdata.get('pingfreq') or 90
        self.maxsendq = self.serverdata.get('maxsendq', 4096)
        self._queue = queue.Queue(self.maxsendq)

    def _schedule_ping(self):
        """Schedules periodic pings in a loop."""
        self._ping_uplink()
        if self._aborted.is_set():
            return
        elapsed = time.time() - self.lastping
        if elapsed > self.pingfreq * KEEPALIVE_MAX_MISSED:
            log.error('(%s) Disconnected from IRC: Ping timeout (%d secs)', self.name, elapsed)
            self.disconnect()
            return
        self._ping_timer = threading.Timer(self.pingfreq, self._schedule_ping)
        self._ping_timer.daemon = True
        self._ping_timer.name = 'Ping timer loop for %s' % self.name
        self._ping_timer.start()
        log.debug('(%s) Ping scheduled at %s', self.name, time.time())

    def _log_connection_error(self, *args, **kwargs):
        if self._aborted.is_set() or world.shutting_down.is_set():
            (log.debug)(*args, **kwargs)
        else:
            (log.error)(*args, **kwargs)

    def _make_ssl_context(self):
        """
        Returns a ssl.SSLContext instance appropriate for this connection.
        """
        context = ssl.create_default_context()
        if self.serverdata.get('ssl_accept_invalid_certs', not self.has_cap('ssl-should-verify')):
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        else:
            context.check_hostname = self.serverdata.get('ssl_validate_hostname', self.has_cap('ssl-should-verify') or utils.get_hostname_type(self.serverdata['ip']) == 0)
        return context

    def _setup_ssl(self):
        """
        Initializes SSL/TLS for this network.
        """
        log.info('(%s) Using TLS/SSL for this connection...', self.name)
        certfile = self.serverdata.get('ssl_certfile')
        keyfile = self.serverdata.get('ssl_keyfile')
        context = self._make_ssl_context()
        if certfile:
            if keyfile:
                try:
                    context.load_cert_chain(certfile, keyfile)
                except OSError:
                    log.exception('(%s) Caught OSError trying to initialize the SSL connection; are "ssl_certfile" and "ssl_keyfile" set correctly?', self.name)
                    raise

        self._socket = context.wrap_socket((self._socket), server_hostname=(self.serverdata.get('ip')))

    def _verify_ssl(self):
        """
        Implements additional SSL/TLS verifications (so far, only certificate fingerprints when enabled).
        """
        peercert = self._socket.getpeercert(binary_form=True)
        hashtype = self.serverdata.get('ssl_fingerprint_type', 'sha256').lower()
        try:
            hashfunc = getattr(hashlib, hashtype)
        except AttributeError:
            raise conf.ConfigurationError('Unsupported or invalid TLS/SSL certificate fingerprint type %r', hashtype)
        else:
            expected_fp = self.serverdata.get('ssl_fingerprint')
            if expected_fp:
                if peercert is None:
                    raise ssl.CertificateError('TLS/SSL certificate fingerprint checking is enabled but the uplink did not provide a certificate')
            fp = hashfunc(peercert).hexdigest()
            if expected_fp:
                if fp != expected_fp:
                    raise ssl.CertificateError('Uplink TLS/SSL certificate fingerprint (%s: %r) does not match the one configured (%s: %r)' % (
                     hashtype, fp, hashtype, expected_fp))
                else:
                    log.info('(%s) Uplink TLS/SSL certificate fingerprint verified (%s: %r)', self.name, hashtype, fp)
            elif hasattr(self._socket, 'context'):
                if self._socket.context.verify_mode == ssl.CERT_NONE:
                    log.info('(%s) Uplink\'s TLS/SSL certificate fingerprint (%s) is %r. You can enhance the security of your link by specifying this in a "ssl_fingerprint" option in your server block.', self.name, hashtype, fp)

    def _connect(self):
        """
        Connects to the network.
        """
        self._pre_connect()
        ip = self.serverdata['ip']
        port = self.serverdata['port']
        try:
            isipv6 = self.serverdata.get('ipv6', utils.get_hostname_type(ip) == 2)
            if not isipv6:
                if 'bindhost' in self.serverdata:
                    isipv6 = utils.get_hostname_type(self.serverdata['bindhost']) == 2
            stype = socket.AF_INET6 if isipv6 else socket.AF_INET
            self._socket = socket.socket(stype)
            if 'bindhost' in self.serverdata:
                self._socket.bind((self.serverdata['bindhost'], 0))
            old_ip = ip
            ip = socket.getaddrinfo(ip, port, stype)[0][(-1)][0]
            log.debug('(%s) Resolving address %s to %s', self.name, old_ip, ip)
            self.ssl = self.serverdata.get('ssl')
            if self.ssl:
                self._setup_ssl()
            else:
                if not ipaddress.ip_address(ip).is_loopback:
                    log.warning('(%s) This connection will be made via plain text, which is vulnerable to man-in-the-middle (MITM) attacks and passive eavesdropping. Consider enabling TLS/SSL with either certificate validation or fingerprint pinning to better secure your network traffic.', self.name)
            log.info('Connecting to network %r on %s:%s', self.name, ip, port)
            self._socket.settimeout(self.pingfreq)
            self._socket.connect((ip, port))
            if self not in world.networkobjects.values():
                log.debug('(%s) _connect: disconnecting socket %s as the network was removed', self.name, self._socket)
                try:
                    self._socket.shutdown(socket.SHUT_RDWR)
                finally:
                    self._socket.close()

                return
            self._socket.setblocking(False)
            self._selector_key = selectdriver.register(self)
            if self.ssl:
                self._verify_ssl()
            self._queue_thread = threading.Thread(name=('Queue thread for %s' % self.name), target=(self._process_queue),
              daemon=True)
            self._queue_thread.start()
            self.sid = self.serverdata.get('sid')
            self.post_connect()
            log.info('(%s) Enumerating our own SID %s', self.name, self.sid)
            host = self.hostname()
            self.servers[self.sid] = Server(self, None, host, internal=True, desc=(self.serverdata.get('serverdesc') or conf.conf['pylink']['serverdesc']))
            log.info('(%s) Starting ping schedulers....', self.name)
            self._schedule_ping()
            log.info('(%s) Server ready; listening for data.', self.name)
            self.autoconnect_active_multiplier = 1
        except:
            self._log_connection_error('(%s) Disconnected from IRC:', (self.name), exc_info=True)
            if not self._aborted.is_set():
                self.disconnect()

    def connect(self):
        """
        Starts a thread to connect the network.
        """
        connect_thread = threading.Thread(target=(self._connect), daemon=True, name=('Connect thread for %s' % self.name))
        connect_thread.start()

    def disconnect(self):
        """Handle disconnects from the remote server."""
        if self._aborted.is_set():
            return
        else:
            self._pre_disconnect()
            if self._queue is not None:
                try:
                    with self._queue.mutex:
                        self._queue.queue[0] = None
                except IndexError:
                    self._queue.put(None)

            if self._socket is not None:
                try:
                    selectdriver.unregister(self)
                except KeyError:
                    pass

                try:
                    log.debug('(%s) disconnect: shutting down read half of socket %s', self.name, self._socket)
                    self._socket.shutdown(socket.SHUT_RD)
                except:
                    log.debug('(%s) Error on socket shutdown:', (self.name), exc_info=True)

                log.debug('(%s) disconnect: waiting for write half of socket %s to shutdown', self.name, self._socket)
                if self._queue_thread is None or self._aborted_send.wait(10):
                    log.debug('(%s) disconnect: closing socket %s', self.name, self._socket)
                    self._socket.close()
            if self._ping_timer:
                log.debug('(%s) Canceling pingTimer at %s due to disconnect() call', self.name, time.time())
                self._ping_timer.cancel()
        self._buffer.clear()
        self._post_disconnect()
        self._socket = None
        self._start_reconnect()

    def _start_reconnect(self):
        """Schedules a reconnection to the network."""

        def _reconnect():
            if self._run_autoconnect():
                self.connect()

        if self not in world.networkobjects.values():
            log.debug('(%s) _start_reconnect: Stopping reconnect timer as the network was removed', self.name)
            return
        else:
            if self._reconnect_thread is None or not self._reconnect_thread.is_alive():
                self._reconnect_thread = threading.Thread(target=_reconnect, name=('Reconnecting network %s' % self.name))
                self._reconnect_thread.start()
            else:
                log.debug('(%s) Ignoring attempt to reschedule reconnect as one is in progress.', self.name)

    def handle_events(self, line):
        raise NotImplementedError

    def parse_irc_command(self, line):
        """Sends a command to the protocol module."""
        log.debug('(%s) <- %s', self.name, line)
        if not line:
            log.warning('(%s) Got empty line %r from IRC?', self.name, line)
            return
        try:
            hook_args = self.handle_events(line)
        except Exception:
            log.exception('(%s) Caught error in handle_events, disconnecting!', self.name)
            log.error('(%s) The offending line was: <- %s', self.name, line)
            self.disconnect()
            return
        else:
            if hook_args is not None:
                self.call_hooks(hook_args)
            return hook_args

    def _run_irc(self):
        """
        Message handler, called when select() has data to read.
        """
        if self._socket is None:
            log.debug('(%s) Ignoring attempt to read data because self._socket is None', self.name)
            return
        data = bytearray()
        try:
            data = self._socket.recv(2048)
        except (BlockingIOError, ssl.SSLWantReadError, ssl.SSLWantWriteError):
            log.debug('(%s) No data to read, trying again later...', (self.name), exc_info=True)
            return
        except OSError:
            if self._aborted.is_set():
                return
            raise

        self._buffer += data
        if not data:
            self._log_connection_error('(%s) Connection lost, disconnecting.', self.name)
            self.disconnect()
            return
        while '\n' in self._buffer:
            line, self._buffer = self._buffer.split('\n', 1)
            line = line.strip('\r')
            line = line.decode(self.encoding, 'replace')
            self.parse_irc_command(line)

        self.lastping = time.time()

    def _send(self, data):
        """Sends raw text to the uplink server."""
        if self._aborted.is_set():
            log.debug('(%s) Not sending message %r since the connection is dead', self.name, data)
            return
        else:
            data = data.replace('\n', ' ')
            encoded_data = data.encode(self.encoding, 'replace')
            if self.S2S_BUFSIZE > 0:
                encoded_data = encoded_data[:self.S2S_BUFSIZE]
            encoded_data += '\r\n'
            log.debug('(%s) -> %s', self.name, data)
            try:
                self._socket.send(encoded_data)
            except:
                log.exception('(%s) Failed to send message %r; aborting!', self.name, data)
                self.disconnect()

    def send(self, data, queue=True):
        """send() wrapper with optional queueing support."""
        if self._aborted.is_set():
            log.debug('(%s) refusing to queue data %r as self._aborted is set', self.name, data)
            return
        else:
            if queue:
                try:
                    self._queue.put_nowait(data)
                except QUEUE_FULL:
                    log.error('(%s) Max SENDQ exceeded (%s), disconnecting!', self.name, self._queue.maxsize)
                    self.disconnect()
                    raise

            else:
                self._send(data)

    def _process_queue(self):
        """Loop to process outgoing queue data."""
        while 1:
            throttle_time = self.serverdata.get('throttle_time', 0)
            data = self._aborted.wait(throttle_time) or self._queue.get()
            if data is None:
                log.debug('(%s) Stopping queue thread due to getting None as item', self.name)
                break
            else:
                if self not in world.networkobjects.values():
                    log.debug('(%s) Stopping stale queue thread; no longer matches world.networkobjects', self.name)
                    break
                else:
                    if self._aborted.is_set():
                        log.debug('(%s) Stopping queue thread since the connection is dead', self.name)
                        break
                    elif data:
                        self._send(data)
                    else:
                        break

        if self._socket:
            log.debug('(%s) _process_queue: shutting down write half of socket %s', self.name, self._socket)
            self._socket.shutdown(socket.SHUT_WR)
        self._aborted_send.set()

    def wrap_message(self, source, target, text):
        """
        Wraps the given message text into multiple lines, and returns these as a list.

        For IRC, the maximum length of one message is calculated as S2S_BUFSIZE (default to 510)
        minus the length of ":sender-nick!sender-user@sender-host PRIVMSG #target :"
        """
        bufsize = self.S2S_BUFSIZE or IRCNetwork.S2S_BUFSIZE
        try:
            target = self.get_friendly_name(target)
        except KeyError:
            log.warning('(%s) Possible desync? Error while expanding wrap_message target %r (source=%s)', (self.name),
              target, source, exc_info=True)

        prefixstr = ':%s PRIVMSG %s :' % (self.get_hostmask(source), target)
        maxlen = bufsize - len(prefixstr)
        log.debug('(%s) wrap_message: length of prefix %r is %s, bufsize=%s, maxlen=%s', self.name, prefixstr, len(prefixstr), bufsize, maxlen)
        if maxlen <= 0:
            log.error('(%s) Got invalid maxlen %s for wrap_message (%s -> %s)', self.name, maxlen, source, target)
            return [
             text]
        else:
            return textwrap.wrap(text, width=maxlen)


Irc = IRCNetwork

class Server:
    """Server"""

    def __init__(self, irc, uplink, name, internal=False, desc='(None given)'):
        self.uplink = uplink
        self.users = set()
        self.internal = internal
        if isinstance(name, str):
            self.name = name.lower()
        else:
            self.name = name
        self.desc = desc
        self._irc = irc
        if not uplink is None:
            if not uplink in self._irc.servers:
                raise AssertionError('Unknown uplink %s' % uplink)
        else:
            if uplink is None:
                self.hopcount = 1
            else:
                self.hopcount = self._irc.servers[uplink].hopcount + 1
        self.has_eob = False

    def __repr__(self):
        return 'Server(%s)' % self.name


IrcServer = Server

class Channel(TSObject, structures.CamelCaseToSnakeCase, structures.CopyWrapper):
    """Channel"""

    def __init__(self, irc, name=None):
        super().__init__()
        self.users = set()
        self.modes = set()
        self.topic = ''
        self.prefixmodes = {'op':set(),  'halfop':set(),  'voice':set(),  'owner':set(), 
         'admin':set()}
        self._irc = irc
        self.topicset = False
        self.name = name

    def __repr__(self):
        return 'Channel(%s)' % self.name

    def remove_user(self, target):
        """Removes a user from a channel."""
        for s in self.prefixmodes.values():
            s.discard(target)

        self.users.discard(target)

    removeuser = remove_user

    def is_voice(self, uid):
        """Returns whether the given user is voice in the channel."""
        return uid in self.prefixmodes['voice']

    def is_halfop(self, uid):
        """Returns whether the given user is halfop in the channel."""
        return uid in self.prefixmodes['halfop']

    def is_op(self, uid):
        """Returns whether the given user is op in the channel."""
        return uid in self.prefixmodes['op']

    def is_admin(self, uid):
        """Returns whether the given user is admin (&) in the channel."""
        return uid in self.prefixmodes['admin']

    def is_owner(self, uid):
        """Returns whether the given user is owner (~) in the channel."""
        return uid in self.prefixmodes['owner']

    def is_voice_plus(self, uid):
        """Returns whether the given user is voice or above in the channel."""
        return bool(self.get_prefix_modes(uid))

    def is_halfop_plus(self, uid):
        """Returns whether the given user is halfop or above in the channel."""
        for mode in ('halfop', 'op', 'admin', 'owner'):
            if uid in self.prefixmodes[mode]:
                return True

        return False

    def is_op_plus(self, uid):
        """Returns whether the given user is op or above in the channel."""
        for mode in ('op', 'admin', 'owner'):
            if uid in self.prefixmodes[mode]:
                return True

        return False

    @staticmethod
    def sort_prefixes(key):
        """
        Returns a numeric value for a named prefix mode: higher ranks have lower values
        (sorted first), and lower ranks have higher values (sorted last).

        This function essentially implements a sorted() key function for named prefix modes.
        """
        values = {'owner':0, 
         'admin':100,  'op':200,  'halfop':300,  'voice':500}
        return values.get(key, 1000)

    def get_prefix_modes(self, uid, prefixmodes=None):
        """
        Returns a list of all named prefix modes the user has in the channel, in
        decreasing order from owner to voice.

        Optionally, a prefixmodes argument can be given to look at an earlier state of
        the channel's prefix modes mapping, e.g. for checking the op status of a mode
        setter before their modes are processed and added to the channel state.
        """
        if uid not in self.users:
            raise KeyError('User %s does not exist or is not in the channel' % uid)
        result = []
        prefixmodes = prefixmodes or self.prefixmodes
        for mode, modelist in prefixmodes.items():
            if uid in modelist:
                result.append(mode)

        return sorted(result, key=(self.sort_prefixes))


IrcChannel = Channel

class PUIDGenerator:
    """PUIDGenerator"""

    def __init__(self, prefix, start=0):
        self.prefix = prefix
        self.counter = start

    def next_uid(self, prefix=''):
        """
        Generates the next PUID.
        """
        uid = '%s@%s' % (prefix or self.prefix, self.counter)
        self.counter += 1
        return uid

    next_sid = next_uid
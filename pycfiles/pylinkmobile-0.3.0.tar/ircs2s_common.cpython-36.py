# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/ircs2s_common.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 30552 bytes
__doc__ = '\nircs2s_common.py: Common base protocol class with functions shared by TS6 and P10-based protocols.\n'
import re, time
from collections import defaultdict
from pylinkirc import conf, utils
from pylinkirc.classes import IRCNetwork, ProtocolError
from pylinkirc.log import log

class IncrementalUIDGenerator:
    """IncrementalUIDGenerator"""

    def __init__(self, sid):
        if not (hasattr(self, 'allowedchars') and hasattr(self, 'length')):
            raise RuntimeError('Allowed characters list not defined. Subclass %s by defining self.allowedchars and self.length and then calling super().__init__().' % self.__class__.__name__)
        self.uidchars = [
         self.allowedchars[0]] * self.length
        self.sid = str(sid)

    def increment(self, pos=None):
        """
        Increments the UID generator to the next available UID.
        """
        if pos is None:
            pos = self.length - 1
        else:
            if self.uidchars[pos] == self.allowedchars[(-1)]:
                self.uidchars[pos] = self.allowedchars[0]
                self.increment(pos - 1)
            else:
                idx = self.allowedchars.find(self.uidchars[pos])
                self.uidchars[pos] = self.allowedchars[(idx + 1)]

    def next_uid(self):
        """
        Returns the next unused UID for the server.
        """
        uid = self.sid + ''.join(self.uidchars)
        self.increment()
        return uid


class IRCCommonProtocol(IRCNetwork):
    COMMON_PREFIXMODES = [
     ('h', 'halfop'), ('a', 'admin'), ('q', 'owner'), ('y', 'owner')]

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._caps = {}
        self._use_builtin_005_handling = False
        self.protocol_caps |= {'has-irc-modes', 'can-manage-bot-channels'}

    def post_connect(self):
        self._caps.clear()

    def validate_server_conf(self):
        """Validates that the server block given contains the required keys."""
        for k in self.conf_keys:
            log.debug('(%s) Checking presence of conf key %r', self.name, k)
            conf.validate(k in self.serverdata, 'Missing option %r in server block for network %s.' % (
             k, self.name))

        port = self.serverdata['port']
        conf.validate(isinstance(port, int) and 0 < port < 65535, 'Invalid port %r for network %s' % (
         port, self.name))

    @staticmethod
    def parse_args(args):
        """
        Parses a string or list of of RFC1459-style arguments, where ":" may
        be used for multi-word arguments that last until the end of a line.
        """
        if isinstance(args, str):
            args = args.split(' ')
        real_args = []
        for idx, arg in enumerate(args):
            if arg.startswith(':') and idx != 0:
                joined_arg = ' '.join(args[idx:])[1:]
                real_args.append(joined_arg)
                break
            else:
                if arg.strip():
                    real_args.append(arg)

        return real_args

    @classmethod
    def parse_prefixed_args(cls, args):
        """Similar to parse_args(), but stripping leading colons from the first argument
        of a line (usually the sender field)."""
        args = cls.parse_args(args)
        args[0] = args[0].split(':', 1)[1]
        return args

    @staticmethod
    def parse_isupport(args, fallback=''):
        """
        Parses a string of capabilities in the 005 / RPL_ISUPPORT format.
        """
        if isinstance(args, str):
            args = args.split(' ')
        caps = {}
        for cap in args:
            try:
                key, value = cap.split('=', 1)
            except ValueError:
                key = cap
                value = fallback

            caps[key] = value

        return caps

    @staticmethod
    def parse_isupport_prefixes(args):
        """
        Separates prefixes field like "(qaohv)~&@%+" into a dict mapping mode characters to mode
        prefixes.
        """
        prefixsearch = re.search('\\(([A-Za-z]+)\\)(.*)', args)
        return dict(zip(prefixsearch.group(1), prefixsearch.group(2)))

    @classmethod
    def parse_message_tags(cls, data):
        """
        Parses IRCv3.2 message tags from a message, as described at http://ircv3.net/specs/core/message-tags-3.2.html

        data is a list of command arguments, split by spaces.
        """
        if data[0].startswith('@'):
            tagdata = data[0].lstrip('@').split(';')
            for idx, tag in enumerate(tagdata):
                tag = tag.replace('\\s', ' ')
                tag = tag.replace('\\r', '\r')
                tag = tag.replace('\\n', '\n')
                tag = tag.replace('\\:', ';')
                tag = tag.replace('\\\\', '\x00')
                tag = tag.replace('\\', '')
                tag = tag.replace('\x00', '\\')
                tagdata[idx] = tag

            results = cls.parse_isupport(tagdata, fallback='')
            return results
        else:
            return {}

    def handle_away(self, source, command, args):
        """Handles incoming AWAY messages."""
        if source not in self.users:
            return
        else:
            try:
                self.users[source].away = text = args[0]
            except IndexError:
                self.users[source].away = text = ''

            return {'text': text}

    def handle_error(self, numeric, command, args):
        """Handles ERROR messages - these mean that our uplink has disconnected us!"""
        raise ProtocolError('Received an ERROR, disconnecting!')

    def handle_pong(self, source, command, args):
        """Handles incoming PONG commands."""
        if source == self.uplink:
            self.lastping = time.time()

    def handle_005(self, source, command, args):
        """
        Handles 005 / RPL_ISUPPORT. This is used by at least Clientbot and ngIRCd (for server negotiation).
        """
        if not self._use_builtin_005_handling:
            log.warning('(%s) Got spurious 005 message from %s: %r', self.name, source, args)
            return
        else:
            newcaps = self.parse_isupport(args[1:-1])
            self._caps.update(newcaps)
            log.debug('(%s) handle_005: self._caps is %s', self.name, self._caps)
            if 'CHANMODES' in newcaps:
                self.cmodes['*A'], self.cmodes['*B'], self.cmodes['*C'], self.cmodes['*D'] = newcaps['CHANMODES'].split(',')
            log.debug('(%s) handle_005: cmodes: %s', self.name, self.cmodes)
            if 'USERMODES' in newcaps:
                self.umodes['*A'], self.umodes['*B'], self.umodes['*C'], self.umodes['*D'] = newcaps['USERMODES'].split(',')
            log.debug('(%s) handle_005: umodes: %s', self.name, self.umodes)
            if 'CASEMAPPING' in newcaps:
                self.casemapping = newcaps.get('CASEMAPPING', self.casemapping)
                log.debug('(%s) handle_005: casemapping set to %s', self.name, self.casemapping)
            if 'PREFIX' in newcaps:
                self.prefixmodes = prefixmodes = self.parse_isupport_prefixes(newcaps['PREFIX'])
                log.debug('(%s) handle_005: prefix modes set to %s', self.name, self.prefixmodes)
                for char, modename in self.COMMON_PREFIXMODES:
                    if char in self.prefixmodes and modename not in self.cmodes:
                        self.cmodes[modename] = char
                        log.debug('(%s) handle_005: autodetecting mode %s (%s) as %s', self.name, char, self.prefixmodes[char], modename)

            if 'EXCEPTS' in newcaps:
                self.cmodes['banexception'] = newcaps.get('EXCEPTS') or 'e'
                log.debug('(%s) handle_005: got cmode banexception=%r', self.name, self.cmodes['banexception'])
            if 'INVEX' in newcaps:
                self.cmodes['invex'] = newcaps.get('INVEX') or 'I'
                log.debug('(%s) handle_005: got cmode invex=%r', self.name, self.cmodes['invex'])
            if 'NICKLEN' in newcaps:
                assert newcaps['NICKLEN'], 'Got NICKLEN tag with no content?'
                self.maxnicklen = int(newcaps['NICKLEN'])
                log.debug('(%s) handle_005: got %r for maxnicklen', self.name, self.maxnicklen)
            if 'DEAF' in newcaps:
                self.umodes['deaf'] = newcaps.get('DEAF') or 'D'
                log.debug('(%s) handle_005: got umode deaf=%r', self.name, self.umodes['deaf'])
            if 'CALLERID' in newcaps:
                self.umodes['callerid'] = newcaps.get('CALLERID') or 'g'
                log.debug('(%s) handle_005: got umode callerid=%r', self.name, self.umodes['callerid'])
            if 'STATUSMSG' in newcaps:
                self.protocol_caps |= {'has-statusmsg'}

    def _send_with_prefix(self, source, msg, **kwargs):
        """Sends a RFC1459-style raw command from the given sender."""
        (self.send)((':%s %s' % (self._expandPUID(source), msg)), **kwargs)


class IRCS2SProtocol(IRCCommonProtocol):
    COMMAND_TOKENS = {}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.protocol_caps |= {'can-spawn-clients', 'has-ts', 'can-host-relay',
         'can-track-servers'}
        self.handle_squit = self._squit

    def handle_events(self, data):
        """Event handler for RFC1459-like protocols.

        This passes most commands to the various handle_ABCD() functions
        elsewhere defined protocol modules, coersing various sender prefixes
        from nicks and server names to UIDs and SIDs respectively,
        whenever possible.

        Commands sent without an explicit sender prefix will have them set to
        the SID of the uplink server.
        """
        data = data.split(' ')
        tags = self.parse_message_tags(data)
        if tags:
            data = data[1:]
        args = self.parse_args(data)
        sender = args[0]
        sender = sender.lstrip(':')
        sender_sid = self._get_SID(sender)
        sender_uid = self._get_UID(sender)
        if sender_sid in self.servers:
            sender = sender_sid
        else:
            if sender_uid in self.users:
                sender = sender_uid
            else:
                if not args[0].startswith(':'):
                    sender = self.uplink
                    args.insert(0, sender)
        raw_command = args[1].upper()
        args = args[2:]
        log.debug('(%s) Found message sender as %s, raw_command=%r, args=%r', self.name, sender, raw_command, args)
        command = self.COMMAND_TOKENS.get(raw_command, raw_command)
        if command != raw_command:
            log.debug('(%s) Translating token %s to command %s', self.name, raw_command, command)
        if self.is_internal_client(sender) or self.is_internal_server(sender):
            log.warning('(%s) Received command %s being routed the wrong way!', self.name, command)
            return
        if command == 'ENCAP':
            command = args[1]
            args = args[2:]
            log.debug('(%s) Rewriting incoming ENCAP to command %s (args: %s)', self.name, command, args)
        try:
            func = getattr(self, 'handle_' + command.lower())
        except AttributeError:
            pass
        else:
            parsed_args = func(sender, command, args)
            if parsed_args is not None:
                if tags:
                    parsed_args['tags'] = tags
                return [sender, command, parsed_args]

    def invite(self, source, target, channel):
        """Sends an INVITE from a PyLink client."""
        if not self.is_internal_client(source):
            raise LookupError('No such PyLink client exists.')
        self._send_with_prefix(source, 'INVITE %s %s' % (self._expandPUID(target), channel))

    def kick(self, numeric, channel, target, reason=None):
        """Sends kicks from a PyLink client/server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        if not reason:
            reason = 'No reason given'
        real_target = self._expandPUID(target)
        self._send_with_prefix(numeric, 'KICK %s %s :%s' % (channel, real_target, reason))
        self.handle_part(target, 'KICK', [channel])

    def numeric(self, source, numeric, target, text):
        """Sends raw numerics from a server to a remote client. This is used for WHOIS replies."""
        target = self._expandPUID(target)
        self._send_with_prefix(source, '%s %s %s' % (numeric, target, text))

    def part(self, client, channel, reason=None):
        """Sends a part from a PyLink client."""
        if not self.is_internal_client(client):
            log.error('(%s) Error trying to part %r from %r (no such client exists)', self.name, client, channel)
            raise LookupError('No such PyLink client exists.')
        msg = 'PART %s' % channel
        if reason:
            msg += ' :%s' % reason
        self._send_with_prefix(client, msg)
        self.handle_part(client, 'PART', [channel])

    def _ping_uplink(self):
        """Sends a PING to the uplink.

        This is mostly used by PyLink internals to check whether the remote link is up."""
        if self.sid:
            if self.connected.is_set():
                self._send_with_prefix(self.sid, 'PING %s' % self._expandPUID(self.uplink))

    def quit(self, numeric, reason):
        """Quits a PyLink client."""
        if self.is_internal_client(numeric):
            self._send_with_prefix(numeric, 'QUIT :%s' % reason)
            self._remove_client(numeric)
        else:
            raise LookupError('No such PyLink client exists.')

    def message(self, numeric, target, text):
        """Sends a PRIVMSG from a PyLink client."""
        if not self.is_internal_client(numeric):
            raise LookupError('No such PyLink client exists.')
        target = self._expandPUID(target)
        self._send_with_prefix(numeric, 'PRIVMSG %s :%s' % (target, text))

    def notice(self, numeric, target, text):
        """Sends a NOTICE from a PyLink client or server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        target = self._expandPUID(target)
        self._send_with_prefix(numeric, 'NOTICE %s :%s' % (target, text))

    def squit(self, source, target, text='No reason given'):
        """SQUITs a PyLink server."""
        log.debug('(%s) squit: source=%s, target=%s', self.name, source, target)
        self._send_with_prefix(source, 'SQUIT %s :%s' % (self._expandPUID(target), text))
        self.handle_squit(source, 'SQUIT', [target, text])

    def topic(self, source, target, text):
        """Sends a TOPIC change from a PyLink client or server."""
        if not self.is_internal_client(source):
            if not self.is_internal_server(source):
                raise LookupError('No such PyLink client/server exists.')
        self._send_with_prefix(source, 'TOPIC %s :%s' % (target, text))
        self._channels[target].topic = text
        self._channels[target].topicset = True

    topic_burst = topic

    def handle_invite(self, numeric, command, args):
        """Handles incoming INVITEs."""
        target = self._get_UID(args[0])
        channel = args[1]
        curtime = int(time.time())
        try:
            ts = int(args[2])
        except IndexError:
            ts = curtime

        ts = ts or curtime
        return {'target':target, 
         'channel':channel,  'ts':ts}

    def handle_kick(self, source, command, args):
        """Handles incoming KICKs."""
        channel = args[0]
        kicked = self._get_UID(args[1])
        try:
            reason = args[2]
        except IndexError:
            reason = ''

        log.debug('(%s) Removing kick target %s from %s', self.name, kicked, channel)
        self.handle_part(kicked, 'KICK', [channel, reason])
        return {'channel':channel, 
         'target':kicked,  'text':reason}

    def handle_kill(self, source, command, args):
        """Handles incoming KILLs."""
        killed = self._get_UID(args[0])
        if killed in self.users:
            userdata = self._remove_client(killed)
        else:
            return
            if '!' in args[1].split(' ', 1)[0]:
                try:
                    killer = self.get_friendly_name(source)
                except KeyError:
                    killer = source

                killmsg = ' '.join(args[1].split(' ')[1:])[1:-1]
                if not killmsg:
                    log.warning('(%s) Failed to extract kill reason: %r', self.name, args)
                    killmsg = args[1]
            else:
                killmsg = args[1]
        return {'target':killed,  'text':killmsg,  'userdata':userdata}

    def _check_cloak_change(self, uid):
        pass

    def _check_umode_away_change(self, uid):
        awaymode = self.umodes.get('away')
        if uid in self.users:
            if awaymode:
                u = self.users[uid]
                old_away_status = u.away
                away_status = (
                 awaymode, None) in u.modes
                if away_status != bool(old_away_status):
                    self.call_hooks([uid, 'AWAY', {'text': 'Away' if away_status else ''}])

    def _check_oper_status_change(self, uid, modes):
        if uid in self.users:
            u = self.users[uid]
            if 'servprotect' in self.umodes:
                if (self.umodes['servprotect'], None) in u.modes:
                    opertype = 'Network Service'
            elif 'netadmin' in self.umodes:
                if (self.umodes['netadmin'], None) in u.modes:
                    opertype = 'Network Administrator'
            elif 'admin' in self.umodes:
                if (self.umodes['admin'], None) in u.modes:
                    opertype = 'Server Administrator'
            else:
                opertype = 'IRC Operator'
            if ('+o', None) in modes:
                self.call_hooks([uid, 'CLIENT_OPERED', {'text': opertype}])

    def handle_mode(self, source, command, args):
        """Handles mode changes."""
        target = self._get_UID(args[0])
        if self.is_channel(target):
            channeldata = self._channels[target].deepcopy()
        else:
            channeldata = None
        modestrings = args[1:]
        changedmodes = self.parse_modes(target, modestrings)
        self.apply_modes(target, changedmodes)
        if target in self.users:
            self._check_cloak_change(target)
            self._check_umode_away_change(target)
            self._check_oper_status_change(target, changedmodes)
        return {'target':target, 
         'modes':changedmodes,  'channeldata':channeldata}

    def handle_part(self, source, command, args):
        """Handles incoming PART commands."""
        channels = args[0].split(',')
        for channel in channels.copy():
            if channel not in self._channels or source not in self._channels[channel].users:
                channels.remove(channel)
            self._channels[channel].remove_user(source)
            try:
                self.users[source].channels.discard(channel)
            except KeyError:
                log.debug("(%s) handle_part: KeyError trying to remove %r from %r's channel list?", self.name, channel, source)

            try:
                reason = args[1]
            except IndexError:
                reason = ''

        if channels:
            return {'channels':channels,  'text':reason}

    def handle_privmsg(self, source, command, args):
        """Handles incoming PRIVMSG/NOTICE."""
        raw_target = args[0]
        server_check = None
        if '@' in raw_target:
            if not self.is_channel(raw_target.lstrip(''.join(self.prefixmodes.values()))):
                log.debug('(%s) Processing user@server message with target %s', self.name, raw_target)
                raw_target, server_check = raw_target.split('@', 1)
                if not self.is_server_name(server_check):
                    log.warning('(%s) Got user@server message with invalid server name %r (full target: %r)', self.name, server_check, args[0])
                    return
        target = self._get_UID(raw_target)
        if server_check is not None:
            not_found = False
            if target not in self.users:
                not_found = True
            else:
                log.debug('(%s) Checking if target %s/%s exists on server %s', self.name, target, raw_target, server_check)
                sid = self._get_SID(server_check)
                sid or log.debug('(%s) Failed user@server server check: %s does not exist.', self.name, server_check)
                not_found = True
        elif sid != self.get_server(target):
            log.debug("(%s) Got user@server message for %s/%s, but they aren't on the server %s/%s. (full target: %r)", self.name, target, raw_target, server_check, sid, args[0])
            not_found = True
        if not_found:
            self.numeric(self.sid, 401, source, '%s :No such nick' % args[0])
            return
        else:
            if target.startswith('='):
                target = '@' + target[1:]
            return {'target':target, 
             'text':args[1]}

    handle_notice = handle_privmsg

    def handle_quit(self, numeric, command, args):
        """Handles incoming QUIT commands."""
        userdata = self._remove_client(numeric)
        if userdata:
            return {'text':args[0],  'userdata':userdata}

    def handle_stats(self, numeric, command, args):
        """Handles the IRC STATS command."""
        return {'stats_type':args[0], 
         'target':self._get_SID(args[1])}

    def handle_topic(self, numeric, command, args):
        """Handles incoming TOPIC changes from clients."""
        channel = args[0]
        topic = args[1]
        oldtopic = self._channels[channel].topic
        self._channels[channel].topic = topic
        self._channels[channel].topicset = True
        return {'channel':channel, 
         'setter':numeric,  'text':topic,  'oldtopic':oldtopic}

    def handle_time(self, numeric, command, args):
        """Handles incoming /TIME requests."""
        return {'target': args[0]}

    def handle_whois(self, numeric, command, args):
        """Handles incoming WHOIS commands.."""
        return {'target': self._get_UID(args[(-1)])}

    def handle_version(self, numeric, command, args):
        """Handles requests for the PyLink server version."""
        return {}
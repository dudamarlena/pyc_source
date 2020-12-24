# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/protocols/ts6_common.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 11209 bytes
"""
ts6_common.py: Common base protocol class with functions shared by the UnrealIRCd, InspIRCd, and TS6 protocol modules.
"""
import string, time
from pylinkirc import conf, structures, utils
from pylinkirc.classes import *
from pylinkirc.log import log
from pylinkirc.protocols.ircs2s_common import *

class TS6SIDGenerator:
    __doc__ = '\n    TS6 SID Generator. <query> is a 3 character string with any combination of\n    uppercase letters, digits, and #\'s. it must contain at least one #,\n    which are used by the generator as a wildcard. On every next_sid() call,\n    the first available wildcard character (from the right) will be\n    incremented to generate the next SID.\n\n    When there are no more available SIDs left (SIDs are not reused, only\n    incremented), RuntimeError is raised.\n\n    Example queries:\n        "1#A" would give: 10A, 11A, 12A ... 19A, 1AA, 1BA ... 1ZA (36 total results)\n        "#BQ" would give: 0BQ, 1BQ, 2BQ ... 9BQ (10 total results)\n        "6##" would give: 600, 601, 602, ... 60Y, 60Z, 610, 611, ... 6ZZ (1296 total results)\n    '

    def __init__(self, irc):
        self.irc = irc
        try:
            self.query = query = list(irc.serverdata['sidrange'])
        except KeyError:
            raise RuntimeError('(%s) "sidrange" is missing from your server configuration block!' % irc.name)

        self.iters = self.query.copy()
        self.output = self.query.copy()
        self.allowedchars = {}
        qlen = len(query)
        if not qlen == 3:
            raise AssertionError('Incorrect length for a SID (must be 3, got %s)' % qlen)
        elif not '#' in query:
            raise AssertionError('Must be at least one wildcard (#) in query')
        for idx, char in enumerate(query):
            assert char in string.digits + string.ascii_uppercase + '#', 'Invalid character %r found.' % char
            if char == '#':
                if idx == 0:
                    self.allowedchars[idx] = string.digits
                else:
                    self.allowedchars[idx] = string.digits + string.ascii_uppercase
                self.iters[idx] = iter(self.allowedchars[idx])
                self.output[idx] = self.allowedchars[idx][0]
                next(self.iters[idx])

    def increment(self, pos=2):
        """
        Increments the SID generator to the next available SID.
        """
        if pos < 0:
            raise RuntimeError('No more available SIDs!')
        it = self.iters[pos]
        try:
            self.output[pos] = next(it)
        except TypeError:
            self.increment(pos - 1)
        except StopIteration:
            self.output[pos] = self.allowedchars[pos][0]
            self.iters[pos] = iter(self.allowedchars[pos])
            next(self.iters[pos])
            self.increment(pos - 1)

    def next_sid(self):
        """
        Returns the next unused TS6 SID for the server.
        """
        while ''.join(self.output) in self.irc.servers:
            self.increment()

        sid = ''.join(self.output)
        return sid


class TS6UIDGenerator(IncrementalUIDGenerator):
    __doc__ = 'Implements an incremental TS6 UID Generator.'

    def __init__(self, sid):
        self.allowedchars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456879'
        self.length = 6
        super().__init__(sid)


class TS6BaseProtocol(IRCS2SProtocol):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.uidgen = structures.KeyedDefaultdict(TS6UIDGenerator)
        self.sidgen = TS6SIDGenerator(self)
        self.protocol_caps |= {'has-statusmsg'}

    def kill(self, numeric, target, reason):
        """Sends a kill from a PyLink client/server."""
        if not self.is_internal_client(numeric):
            if not self.is_internal_server(numeric):
                raise LookupError('No such PyLink client/server exists.')
        elif not target in self.users:
            raise AssertionError('Unknown target %r for kill()!' % target)
        else:
            if numeric in self.users:
                userobj = self.users[numeric]
                killpath = '%s!%s' % (userobj.host, userobj.nick)
            else:
                if numeric in self.servers:
                    killpath = self.servers[numeric].name
                else:
                    log.warning('(%s) Invalid sender %s for kill(); using our server name instead.', self.name, numeric)
                    killpath = self.servers[self.sid].name
        self._send_with_prefix(numeric, 'KILL %s :%s (%s)' % (target, killpath, reason))
        self._remove_client(target)

    def nick(self, numeric, newnick):
        """Changes the nick of a PyLink client."""
        if not self.is_internal_client(numeric):
            raise LookupError('No such PyLink client exists.')
        self._send_with_prefix(numeric, 'NICK %s %s' % (newnick, int(time.time())))
        self.users[numeric].nick = newnick
        self.users[numeric].ts = int(time.time())

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
        elif not len(sid) == 3:
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
        self._send_with_prefix(uplink, 'SID %s %s %s :%s' % (name, self.servers[sid].hopcount, sid, desc))
        return sid

    def away(self, source, text):
        """Sends an AWAY message from a PyLink client. <text> can be an empty string
        to unset AWAY status."""
        if text:
            self._send_with_prefix(source, 'AWAY :%s' % text)
        else:
            self._send_with_prefix(source, 'AWAY')
        self.users[source].away = text

    def handle_knock(self, numeric, command, args):
        """Handles channel KNOCKs."""
        channel = args[0]
        try:
            text = args[1]
        except IndexError:
            text = ''

        return {'channel':channel, 
         'text':text}

    def handle_nick(self, numeric, command, args):
        """Handles incoming NICK changes."""
        oldnick = self.users[numeric].nick
        newnick = self.users[numeric].nick = args[0]
        self.users[numeric].ts = ts = int(args[1])
        return {'newnick':newnick, 
         'oldnick':oldnick,  'ts':ts}

    def handle_save(self, numeric, command, args):
        """Handles incoming SAVE messages, used to handle nick collisions."""
        user = args[0]
        oldnick = self.users[user].nick
        self.users[user].nick = user
        self.users[user].ts = 100
        return {'target':user, 
         'ts':100,  'oldnick':oldnick}

    def handle_server(self, numeric, command, args):
        """Handles the SERVER command, used for introducing older (TS5) servers."""
        servername = args[0].lower()
        sdesc = args[(-1)]
        self.servers[servername] = Server(self, numeric, servername, desc=sdesc)
        return {'name':servername,  'sid':None,  'text':sdesc}

    def handle_sid(self, numeric, command, args):
        """Handles the SID command, used for introducing remote servers by our uplink."""
        sname = args[0].lower()
        sid = args[2]
        sdesc = args[(-1)]
        self.servers[sid] = Server(self, numeric, sname, desc=sdesc)
        return {'name':sname,  'sid':sid,  'text':sdesc}

    def handle_svsnick(self, source, command, args):
        """Handles SVSNICK (forced nickname change attempts)."""
        return {'target':self._get_UID(args[0]), 
         'newnick':args[1]}
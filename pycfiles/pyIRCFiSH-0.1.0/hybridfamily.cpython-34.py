# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/ircd/hybridfamily.py
# Compiled at: 2015-10-08 05:15:33
# Size of source mod 2**32: 22689 bytes
__doc__ = 'IRC daemon-specific routines for Hybrid derivatives.\n\nThis includes Charybdis and ircd-ratbox\n'
import re
from datetime import datetime
from logging import getLogger
from PyIRC.line import Hostmask
from PyIRC.signal import event
from PyIRC.numerics import Numerics
from PyIRC.extensions.ircd.base import BaseServer, BanEntry, Extban, OperEntry, Uptime
_logger = getLogger(__name__)
_stats_ban_re = re.compile('^\n    (?:\n        # If there is a duration, this matches it.\n        # Beware the space at the end of the line!\n        Temporary\\ (?P<type>.)-line\\ (?P<duration>[0-9]+)\\ min\\.\\ -\\ \n    )?\n    (?P<reason>.+?)\n    (?:\n        # Match the date and time of setting\n        \\ \\(\n            (?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})\n            \\ (?P<hour>[0-9]{2})\\.(?P<minute>[0-9]{2})\n        \\)\n    )?\n    (?:\n        # Operator reason (and setter)\n        \\|(?P<oreason>.+?)\n        (?:\n            # Setter format is (mask!of@setter{serv or nick})\n            \\ \\(\n                (?P<settermask>.+?)\n                \\{\n                    (?P<setter>.+?)\n                \\}\n            \\)\n        )?\n    )?$', re.X)
_hybrid_oper_re = re.compile('^\n    \\[\n        (?P<flag>[AO])\n    \\]\n    (?:\n        # These may or may not occur, depending on if the oper is local or\n        # global\n        \\[\n            (?P<privs>.+?)\n        \\]\n    )?\n    \\ (?P<nick>.+?)\n    \\ \\((?P<user>.+?)@(?P<host>.+?)\\)\n    \\ Idle: (?P<idle>[0-9]+)$\n    ', re.X)
_charybdis_oper_re = re.compile('^\n    # Mind the trailing space!\n    (?P<nick>.+?) \\ \n    \\(\n        (?P<user>.+?)@(?P<host>.+?)\n    \\)$', re.X)
_uptime_re = re.compile('^\n    # Mind the trailing space\n    Server\\ up\\ (?P<days>[0-9]+)\\ days,\\ \n    (?P<hours>[0-9]{1,2}):\n    (?P<minutes>[0-9]{1,2}):\n    (?P<seconds>[0-9]{1,2})$\n    ', re.X)

class HybridServer(BaseServer):
    """HybridServer"""
    requires = [
     'ISupport']

    def provides(base):
        """Returns whether or not this extension can provide for the
        server."""
        version = base.basic_rfc.server_version[0]
        if version is None:
            return False
        if version.startswith('ircd-hybrid'):
            return True
        return False

    def generic_ban(self, ban, server, string, duration, reason):
        """Do a generic Hybrid-style ban.

        :param ban:
            Ban type to send.

        :param server:
            Server to send to.

        :param string:
            String to issue the ban with.

        :param duration:
            Duration of ban time in seconds.

        :param reason:
            The reason for the ban
        """
        params = []
        if duration:
            params.append(str(round(duration / 60)))
        if server:
            params.extend((string, 'ON', server))
        else:
            params.append(string)
        if reason:
            params.append(reason)
        self.send(ban, params)

    def global_ban(self, user, duration, reason):
        """Ban a user on the IRC network. This is often referred to as a
        "g:line" or (confusingly) as a "k:line".

        :param user:
            A :py:class:`~PyIRC.extensions.usertrack.User` instance, a
            :py:class:`~PyIRC.line.Hostmask` instance, or a string, containing
            the mask or user to ban.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.

        ..warning::
            This may have varying semantics based on IRC daemon. For example,
            on ircd-hybrid derivatives, this will be emulated as a global
            k:line, not as a g:line (which means something else entirely and
            is unlikely to be what you want outside of EFNet).

        ..note::
            This command requires IRC operator privileges, and may require
            additional privileges such as privsets or ACL's. Such documentation
            is out of scope for PyIRC. Check your IRC daemon's documentation,
            or consult a network administrator, for more information.
        """
        self.server_ban('*', user, duration, reason)

    def server_ban(self, server, user, duration, reason):
        """Ban a user on an IRC server. This is often referred to as a
        "k:line".

        :param server:
            The name of the server to apply the ban to. ``None`` sets it to
            the current server.

        :param user:
            A :py:class:`~PyIRC.extensions.usertrack.User` instance, a
            :py:class:`~PyIRC.line.Hostmask` instance, or a string, containing
            the mask or user to ban.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.
        """
        if hasattr(user, 'host'):
            user = '{}@{}'.format(user.user, user.host)
        self.generic_ban('KLINE', server, user, duration, reason)

    def global_ip_ban(self, ip, duration, reason):
        """Ban an IP or CIDR range on the IRC network. This is often referred
        to as a "z:line" or (in hybrid derivatives) as a "d:line".

        :param ip:
            A string containing the IP or CIDR to ban.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.

        ..note::
            This command requires IRC operator privileges, and may require
            additional privileges such as privsets or ACL's. Such documentation
            is out of scope for PyIRC. Check your IRC daemon's documentation,
            or consult a network administrator, for more information.
        """
        self.server_ip_ban('*', ip, duration, reason)

    def server_ip_ban(self, server, ip, duration, reason):
        """Ban an IP or CIDR range on an IRC server. This is often referred to
        as a "z:line" or (in hybrid derivatives) as a "d:line".

        :param server:
            The name of the server to apply the ban to. ``None`` sets it to
            the current server.

        :param ip:
            A string containing the IP or CIDR to ban.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.

        ..note::
            This command requires IRC operator privileges, and may require
            additional privileges such as privsets or ACL's. Such documentation
            is out of scope for PyIRC. Check your IRC daemon's documentation,
            or consult a network administrator, for more information.
        """
        self.generic_ban('DLINE', server, ip, duration, reason)

    def global_nickchan_ban(self, string, duration, reason):
        """Ban a nick on the IRC network. This is often referred to as a
        "Q:line", "q:line", or (in hybrid derivatives) as a "resv".

        :param string:
            Nickname or channel to ban as a string.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.

        ..note::
            This command requires IRC operator privileges, and may require
            additional privileges such as privsets or ACL's. Such documentation
            is out of scope for PyIRC. Check your IRC daemon's documentation,
            or consult a network administrator, for more information.
        """
        self.server_nickchan_ban('*', string, duration, reason)

    def server_nickchan_ban(self, server, string, duration, reason):
        """Ban a nick on an IRC server. This is often referred to as a
        "Q:line", "q:line", or (in hybrid derivatives) as a "resv".

        :param server:
            The name of the server to apply the ban to. ``None`` sets it to
            the current server.

        :param string:
            Nickname or channel to ban as a string.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.

        ..warning::
            This is not supported on InspIRCd, as all q:lines are global.

        ..note::
            This command requires IRC operator privileges, and may require
            additional privileges such as privsets or ACL's. Such documentation
            is out of scope for PyIRC. Check your IRC daemon's documentation,
            or consult a network administrator, for more information.
        """
        self.generic_ban('RESV', server, string, duration, reason)

    def global_gecos_ban(self, string, duration, reason):
        """Ban a gecos on the IRC network. This is often referred to as an
        "sgline", "n:line", or (in hybrid derivatives) as an "x:line".

        :param string:
            GECOS to ban as a string.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.

        ..warning::
            Not all servers support this. UnrealIRCd, notably, only supports
            permanent GECOS bans.

        ..note::
            This command requires IRC operator privileges, and may require
            additional privileges such as privsets or ACL's. Such documentation
            is out of scope for PyIRC. Check your IRC daemon's documentation,
            or consult a network administrator, for more information.
        """
        self.server_gecos_ban('*', string, duration, reason)

    def server_gecos_ban(self, server, string, duration, reason):
        """Ban a GECOS on an IRC server. This is often referred to as an
        "sgline", "n:line", or (in hybrid derivatives) as an "x:line".
 
        :param server:
            The name of the server to apply the ban to. ``None`` sets it to
            the current server.

        :param string:
            Nickname or channel to ban as a string.

        :param duration:
            How long the ban should last in seconds, or ``None`` for permanent.

        :param reason:
            The reason for the ban.

        ..warning::
            Not all servers support this. UnrealIRCd, notably, only supports
            permanent GECOS bans.

        ..note::
            This command requires IRC operator privileges, and may require
            additional privileges such as privsets or ACL's. Such documentation
            is out of scope for PyIRC. Check your IRC daemon's documentation,
            or consult a network administrator, for more information.
        """
        self.generic_ban('XLINE', server, string, duration, reason)

    def stats_global_ban(self):
        """Get a list of all global bans (often referred to as "g:lines" or,
        confusingly, as "k:lines").

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.stats_server_ban('*')

    def stats_server_ban(self, server):
        """Get a list of all server bans (often referred to as "k:lines").

        :param server:
            Server to get the list of bans on.

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.send('STATS', ['G'])
        self.send('STATS', ['K', server])
        self.send('STATS', ['K', server])

    def stats_global_ip_ban(self):
        """Get a list of all global IP bans (often referred to as "z:lines" or
        "d:lines").

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.stats_server_ip_ban('*')

    def stats_server_ip_ban(self, server):
        """Get a list of all server IP bans (often referred to as "z:lines" or
        "d:lines").

        :param server:
            Server to get the list of bans on.

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.send('STATS', ['d', server])
        self.send('STATS', ['D', server])

    def stats_global_nickchan_ban(self):
        """Get a list of all global nick/channel bans (often referred to as
        "Q:lines" or "resvs").

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.stats_server_nickchan_ban('*')

    def stats_server_nickchan_ban(self, server):
        """Get a list of all server nick/channel bans (often referred to as 
        "Q:lines", "q:lines" or "resvs").

        :param server:
            Server to get the list of bans on.

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.send('STATS', ['r', server])
        self.send('STATS', ['R', server])

    def stats_global_gecos_ban(self):
        """Get a list of all global GECOS bans (often referred to as "sglines",
        "n:lines", or "x:lines").

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.stats_server_gecos_ban('*')

    def stats_server_gecos_ban(self, server):
        """Get a list of all server GECOS bans (often referred to as "sglines",
        "n:lines", or "x:lines).

        :param server:
            Server to get the list of bans on.

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.send('STATS', ['x', server])
        self.send('STATS', ['X', server])

    def stats_opers(self, server=None):
        """Get a list of IRC operators on the network. This may return either
        all the operators, or only the active ones, depending on the IRC
        daemon.

        :param server:
            Server to get the list of opers on. ``None`` defaults to the
            current server. This usually does not matter.

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        if server is not None:
            self.send('STATS', ['p', server])
        else:
            self.send('STATS', ['p'])

    def stats_uptime(self, server=None):
        """Get the uptime of the server.

        :param server:
            Server to get the uptime of. ``None`` defaults to the current server.
        """
        if server is not None:
            self.send('STATS', ['u', server])
        else:
            self.send('STATS', ['u'])

    @staticmethod
    def _parse_ban_lines(line):
        """Parse a foo:line in Hybrid-derived servers, excluding RESV and
        X:lines."""
        params = line.params
        match = _stats_ban_re.match(params[(-1)])
        assert match, 'Bug in the stats matching regex!'
        t = match.group('type')
        if t == 'K' or t == 'G':
            mask = (params[3], params[4], params[2])
        else:
            if t == 'D':
                mask = params[2]
            else:
                _logger.warning('Unknown bantype, just guessing!')
                mask = params[:-1]
            duration = int(match.group('duration')) * 60
            year = int(match.group('year'))
            month = int(match.group('month'))
            day = int(match.group('day'))
            hour = int(match.group('hour'))
            minute = int(match.group('minute'))
            if all(x is not None for x in (year, month, day)):
                setdate = datetime(year, month, day, hour, minute)
            else:
                setdate = None
        reason = match.group('reason')
        oreason = match.group('oreason')
        settermask = Hostmask.parse(match.group('settermask'))
        setter = match.group('setter')
        return BanEntry(mask, settermask, setter, setdate, duration, reason, oreason)

    @event('commands', Numerics.RPL_STATSKLINE)
    @event('commands', Numerics.RPL_STATSDLINE)
    def parse_stats_ban(self, _, line):
        """Evaluate a stats line for a ban."""
        entry = self._parse_ban_lines(line)
        if not entry:
            return
        if line.command == Numerics.RPL_STATSKLINE.value():
            ban = 'ban'
        else:
            ban = 'ip_ban'
        return self.call_event('stats', ban, entry)

    @event('commands', Numerics.RPL_STATSQLINE)
    def parse_stats_user(self, _, line):
        """Evaluate a stats line for a RESV."""
        duration = line.params[1]
        mask = line.params[2]
        reason = line.params[3]
        entry = BanEntry(mask, None, None, None, duration, reason, None)
        return self.call_event('stats', 'nickchan_ban', entry)

    @event('commands', Numerics.RPL_STATSXLINE)
    def parse_stats_gecos(self, _, line):
        """Evaluate a stats line for an X:line."""
        duration = line.params[1]
        mask = line.params[2]
        reason = line.params[3]
        entry = BanEntry(mask, None, None, None, duration, reason, None)
        return self.call_event('stats', 'gecos_ban', entry)

    @event('commands', Numerics.RPL_STATSDEBUG)
    def parse_stats_opers(self, _, line):
        """Evaluate a stats line for an oper."""
        if line.params[1] != 'p':
            return
        match = _hybrid_oper_re(line.params[(-1)])
        if not match:
            return
        flag = match.group('flag')
        privs = match.group('privs')
        nick = match.group('nick')
        user = match.group('user')
        host = match.group('host')
        hostmask = Hostmask(nick=nick, user=user, host=host)
        idle = int(match.group('idle'))
        entry = OperEntry(flag, privs, hostmask, idle)
        return self.call_event('stats', 'oper', entry)

    @event('commands', Numerics.RPL_STATSUPTIME)
    def parse_stats_uptime(self, _, line):
        """Evaluate the server uptime."""
        uptime = _uptime_re.match(line.params[(-1)])
        days = int(uptime.group('days'))
        hours = int(uptime.group('hours'))
        minutes = int(uptime.group('minutes'))
        seconds = int(uptime.group('seconds'))
        uptime = Uptime(days, hours, minutes, seconds)
        return self.call_event('stats', 'uptime', uptime)


class RatboxServer(HybridServer):
    """RatboxServer"""

    def provides(base):
        """Returns whether or not this extension can provide for the
        server."""
        version = base.basic_rfc.server_version[0]
        if version is None:
            return False
        if version.startswith('ircd-ratbox'):
            return True
        return False


class CharybdisServer(RatboxServer):
    """CharybdisServer"""

    def provides(base):
        """Returns whether or not this extension can provide for the
        server."""
        version = base.basic_rfc.server_version[0]
        if version is None:
            return False
        if version.startswith('charybdis'):
            return True
        return False

    def extban_parse(self, string):
        if not string or string[0] != '$':
            return
        negative = string[1] == '~'
        if negative:
            ban = string[2]
            target = string[3:] if len(string) > 3 else None
        else:
            ban = string[1]
            target = string[2:] if len(string) > 2 else None
        isupport = self.base.isupport
        _, _, bans = isupport.get('EXTBAN').partition(',')
        if ban not in bans:
            _logger.warning('Unknown extban received: %s', string[1])
        return [
         Extban(negative, ban, target)]

    def stats_server_ban(self, server):
        """Get a list of all server bans (often referred to as "k:lines").

        :param server:
            Server to get the list of bans on.

        ..note::
            This may not be implemented on some servers, restricted, or even
            filtered. Unless you are an operator, take the information that is
            returned with a grain of salt.
        """
        self.send('STATS', ['g'])
        self.send('STATS', ['K', server])
        self.send('STATS', ['K', server])

    @event('commands', Numerics.RPL_STATSDEBUG)
    def parse_stats_opers(self, _, line):
        """Evaluate a stats line for an oper."""
        if line.params[1] != 'p':
            return
        match = _charybdis_oper_re.match(line.params[(-1)])
        if not match:
            return
        nick = match.group('nick')
        user = match.group('user')
        host = match.group('host')
        hostmask = Hostmask(nick=nick, user=user, host=host)
        entry = OperEntry(None, None, hostmask, None)
        return self.call_event('stats', 'oper', entry)


class IrcdSevenServer(CharybdisServer):
    """IrcdSevenServer"""

    def provides(base):
        """Returns whether or not this extension can provide for the
        server."""
        version = base.basic_rfc.server_version[0]
        if version is None:
            return False
        if version.startswith('ircd-seven'):
            return True
        return False
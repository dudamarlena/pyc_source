# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/basetrack.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 9177 bytes
"""Base tracking API.

This is not really meant for direct use; it converts commands into
events for ingestion into the other tracking components.

"""
from collections import namedtuple
from logging import getLogger
from PyIRC.signal import event
from PyIRC.auxparse import mode_parse, prefix_parse, status_prefix_parse
from PyIRC.extensions import BaseExtension
from PyIRC.line import Hostmask
from PyIRC.numerics import Numerics
_logger = getLogger(__name__)
Mode = namedtuple('Mode', 'mode param adding timestamp')

class Scope:
    __doc__ = 'A scope object passed to receivers of scope events.\n\n    :param target:\n        The :py:class:`~PyIRC.line.Hostmask` of user that is changing scope.\n\n    :param scope:\n        Scope of the change, None for global, or set to a channel.\n\n    :param leaving:\n        whether or not the user is leaving, may be ``none`` for not\n        applicable.\n\n    :param reason:\n        The reason for the change (part/kick reason).\n\n    :param gecos:\n        The GECOS of the user changing scope, may be ``none``.\n\n    :param account:\n        The account of the user changing scope, may be ``none``.\n\n    :param modes:\n        The modes of the user that are being explicitly added or removed by\n        scope change.\n\n    :param cause:\n        The user that caused this change (for kicks, etc).\n\n    '
    __slots__ = [
     'target', 'scope', 'leaving', 'reason', 'gecos', 'account',
     'modes', 'cause']

    def __init__(self, target, scope=None, leaving=None, reason=None, gecos=None, account=None, modes=None, cause=None):
        self.target = target
        self.scope = scope
        self.leaving = leaving
        self.reason = reason
        self.gecos = gecos
        self.account = account
        self.modes = [] if modes is None else modes
        self.cause = cause


class BaseTrack(BaseExtension):
    __doc__ = 'Base tracking extension, providing events for other tracking extensions.\n\n    This extension adds ``base.base_track`` as itself as an alias for\n    ``get_extension("BaseTrack").``.\n\n    '
    caps = {'extended-join': [],  'multi-prefix': [],  'userhost-in-names': []}
    mode_chars = {Numerics.RPL_BANLIST.value: 'b',  Numerics.RPL_EXCEPTLIST.value: 'e', 
     Numerics.RPL_INVITELIST.value: 'I', 
     Numerics.RPL_QUIETLIST.value: 'q', 
     Numerics.RPL_SPAMFILTERLIST.value: 'g', 
     Numerics.RPL_EXEMPTCHANOPSLIST.value: 'X', 
     Numerics.RPL_AUTOOPLIST.value: 'w', 
     Numerics.RPL_REOPLIST.value: 'R'}
    requires = [
     'ISupport']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base.base_track = self
        self.sent_protoctl = False

    @event('commands', 'JOIN')
    def join(self, _, line):
        """Fire a (scope, user_join) event for users joining channels."""
        params = line.params
        hostmask = line.hostmask
        if not hostmask:
            return
        channel = params[0]
        account = gecos = None
        if len(params) > 1:
            account = params[1]
            if len(params) > 2:
                gecos = params[2]
        scope = Scope(hostmask, channel, False, gecos=gecos, account=account)
        self.call_event('scope', 'user_join', scope)

    @event('commands', Numerics.RPL_NAMREPLY)
    def names(self, _, line):
        """Handle bursting of new users from NAMES."""
        params = line.params
        channel = params[2]
        isupport = self.base.isupport
        prefix = prefix_parse(isupport.get('PREFIX'))
        for hostmask in params[3].split(' '):
            if not hostmask:
                continue
            modes, hostmask = status_prefix_parse(hostmask, prefix)
            hostmask = Hostmask.parse(hostmask)
            modes = [(m, hostmask, True, None) for m in modes]
            scope = Scope(hostmask, channel, False, cause=line.hostmask, modes=modes)
            self.call_event('scope', 'user_burst', scope)

    @event('commands', 'PART')
    def part(self, _, line):
        """Fire a (scope, user_part) event for users leaving channels."""
        params = line.params
        channel = params[0]
        reason = params[1] if len(params) > 1 else None
        scope = Scope(line.hostmask, channel, True, reason=reason, cause=line.hostmask)
        self.call_event('scope', 'user_part', scope)

    @event('commands', 'KICK')
    def kick(self, _, line):
        """Fire a (scope, user_kick) event for users being kicked."""
        params = line.params
        channel = params[0]
        target = Hostmask(nick=params[1])
        reason = params[2]
        scope = Scope(target, channel, True, reason=reason, cause=line.hostmask)
        self.call_event('scope', 'user_kick', scope)

    @event('commands', 'QUIT')
    def quit(self, _, line):
        """Fire a (scope, user_quit) event for users leaving IRC."""
        params = line.params
        reason = params[0] if params else None
        scope = Scope(line.hostmask, None, True, reason=reason, cause=line.hostmask)
        self.call_event('scope', 'user_quit', scope)

    @event('commands', Numerics.RPL_CHANNELMODEIS)
    @event('commands', 'MODE')
    def mode(self, _, line):
        """Offer an easy to use interface for mode"""
        isupport = self.base.isupport
        modegroups = isupport.get('CHANMODES')
        prefix = prefix_parse(isupport.get('PREFIX'))
        params = line.params[:] if line.command == 'MODE' else line.params[1:]
        target = params[0]
        modes = params[1]
        params = params[2:]
        channels = tuple(isupport.get('CHANTYPES'))
        if not target.startswith(channels):
            return
        gen = mode_parse(modes, params, modegroups, prefix)
        prefix = prefix.mode_to_prefix
        for mode, param, adding in gen:
            if mode in prefix:
                mode_call = 'mode_prefix'
            else:
                if mode in modegroups[0]:
                    mode_call = ('mode_list', )
                else:
                    if mode in modegroups[1]:
                        mode_call = ('mode_key', )
                    else:
                        if mode in modegroups[2]:
                            mode_call = ('mode_param', )
                        else:
                            mode_call = 'mode_normal'
            mode = Mode(mode, param, adding, None)
            self.call_event('modes', mode_call, line.hostmask, target, mode)

    @event('commands', Numerics.RPL_ENDOFMOTD)
    @event('commands', Numerics.ERR_NOMOTD)
    def send_protoctl(self, _, line):
        """Send the PROTOCTL NAMESX/UHNAMES stuff if we have to"""
        if self.sent_protoctl:
            return
        isupport = self.base.isupport
        protoctl = []
        if isupport.get('UHNAMES'):
            protoctl.append('UHNAMES')
        if isupport.get('NAMESX'):
            protoctl.append('NAMESX')
        if protoctl:
            self.send('PROTOCTL', protoctl)
        self.sent_protoctl = True

    @event('commands', Numerics.RPL_QUIETLIST)
    def quiet_list(self, caller, line):
        isupport = self.base.isupport
        if 'q' in isupport.get('PREFIX'):
            _logger.critical('Got a quiet mode, but mode for quiet is unknown to us!')
            _logger.critical('Please report a bug to the PyIRC team with the mode your IRC daemon uses, along with its version information')
            return
        return self.handle_list(caller, line)

    @event('commands', Numerics.RPL_BANLIST)
    @event('commands', Numerics.RPL_EXCEPTLIST)
    @event('commands', Numerics.RPL_INVITELIST)
    @event('commands', Numerics.RPL_SPAMFILTERLIST)
    @event('commands', Numerics.RPL_EXEMPTCHANOPSLIST)
    @event('commands', Numerics.RPL_AUTOOPLIST)
    @event('commands', Numerics.RPL_REOPLIST)
    def handle_list(self, caller, line):
        modechar = self.mode_chars[caller.eventpair[1]]
        params = line.params
        try:
            target = params[1]
            mask = params[2]
            if len(params) > 3:
                setter = Hostmask.parse(params[3])
                if len(params) > 4:
                    timestamp = int(params[4])
            else:
                setter = line.hostmask
                timestamp = None
        except Exception as e:
            _logger.warning('Bogus list mode received: %s (exception: %s)', modechar, e)
            return

        mode = Mode(modechar, mask, True, timestamp)
        self.call_event('modes', 'mode_list', setter, target, mode)
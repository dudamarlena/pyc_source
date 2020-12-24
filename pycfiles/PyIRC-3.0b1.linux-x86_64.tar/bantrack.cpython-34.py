# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/bantrack.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 5042 bytes
"""Track IRC ban modes (+beIq)

In order to be taught about new types, this extension must know the
numerics used for ban listing.

"""
from collections import namedtuple
from logging import getLogger
from PyIRC.signal import event
from PyIRC.extensions import BaseExtension
from PyIRC.numerics import Numerics
_logger = getLogger(__name__)
BanEntry = namedtuple('BanEntry', 'string setter timestamp')

class BanTrack(BaseExtension):
    __doc__ = 'Track bans and other "list" modes.\n\n    This augments the :py:class:`~PyIRC.extensions.channeltrack.ChannelTrack`\n    extension.\n\n    Although the actual reporting is done by\n    :py:class:`~PyIRC.extensions.basetrack.BaseTrack`, this helps with\n    the actual retrieval of the modes, and setting synched states.\n\n    .. note::\n        Unless you are opped, your view of modes such as +eI may be limited\n        and incomplete.\n\n    '
    requires = [
     'ISupport', 'ChannelTrack', 'BasicRFC']
    mode_chars = {Numerics.RPL_ENDOFBANLIST.value: 'b',  Numerics.RPL_ENDOFEXCEPTLIST.value: 'e', 
     Numerics.RPL_ENDOFINVITELIST.value: 'I', 
     Numerics.RPL_ENDOFQUIETLIST.value: 'q', 
     Numerics.ERR_ENDOFSPAMFILTERLIST.value: 'g', 
     Numerics.ERR_ENDOFEXEMPTCHANOPSLIST.value: 'X', 
     Numerics.RPL_ENDOFREOPLIST.value: 'R', 
     Numerics.RPL_ENDOFAUTOOPLIST.value: 'w'}

    @event('channel', 'channel_create')
    def join(self, _, channel):
        """Initialise tracking for a new channel."""
        _logger.debug('Creating ban modes for channel %s', channel.name)
        channel.synced_list = dict()
        isupport = self.base.isupport
        modes = isupport.get('CHANMODES')[0]
        for mode in modes:
            channel.modes[mode] = list()
            channel.synced_list[mode] = False

        self.send('MODE', [channel.name, modes])

    @event('modes', 'mode_list')
    def mode_list(self, _, setter, target, mode):
        """Update a ban (or other list mode) entry."""
        if mode.param is None:
            return
        channeltrack = self.base.channel_track
        channel = channeltrack.get_channel(target)
        if not channel:
            return
        modes = channel.modes[mode.mode]
        entry = BanEntry(mode.param, setter, mode.timestamp)
        for i, (string, _, _) in enumerate(list(modes)):
            if self.casecmp(mode.param, string):
                if mode.adding:
                    _logger.debug('Replacing entry: %r -> %r', modes[i], entry)
                    modes[i] = entry
                else:
                    _logger.debug('Removing ban: %r', modes[i])
                    del modes[i]
                return

        _logger.debug('Adding entry: %r', entry)
        modes.append(entry)

    @event('modes', 'mode_prefix')
    def mode_prefix(self, _, setter, target, mode):
        if mode.mode == 'v':
            return
        basicrfc = self.base.basic_rfc
        if not self.casecmp(mode.param, basicrfc.nick):
            return
        channeltrack = self.base.channel_track
        channel = channeltrack.get_channel(target)
        if not channel:
            return
        if mode.adding:
            check = ''
            for sync, value in channel.synced_list.items():
                if not value:
                    check += sync
                    continue

            if check:
                self.send('MODE', [target, check])

    @event('commands', Numerics.RPL_ENDOFBANLIST)
    @event('commands', Numerics.RPL_ENDOFEXCEPTLIST)
    @event('commands', Numerics.RPL_ENDOFINVITELIST)
    @event('commands', Numerics.RPL_ENDOFQUIETLIST)
    @event('commands', Numerics.ERR_ENDOFSPAMFILTERLIST)
    @event('commands', Numerics.ERR_ENDOFEXEMPTCHANOPSLIST)
    @event('commands', Numerics.RPL_ENDOFREOPLIST)
    @event('commands', Numerics.RPL_ENDOFAUTOOPLIST)
    def set_synced(self, caller, line):
        """Mark a list mode as synchronised."""
        mode = self.mode_chars[caller.eventpair[1]]
        channeltrack = self.base.channel_track
        channel = channeltrack.get_channel(line.params[1])
        if not channel:
            return
        if mode not in channel.synced_list:
            _logger.warning('Got bogus/invalid end of list sync for mode %s', mode)
            return
        channel.synced_list[mode] = True
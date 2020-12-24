# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/kickrejoin.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 6467 bytes
__doc__ = 'Rejoin automatically after being kicked from a channel.\n\nThis extension is also meant to serve as an example for extension\nauthors.  It is heavily documented and designed to be very easy to\nfollow.\n\n'
from functools import partial
from logging import getLogger
from PyIRC.signal import event
from PyIRC.extensions import BaseExtension
_logger = getLogger(__name__)

class KickRejoin(BaseExtension):
    """KickRejoin"""
    requires = [
     'BasicRFC', 'ISupport']

    def __init__(self, *args, **kwargs):
        """Initialise the KickRejoin extension.

        :key rejoin_delay:
            Seconds to delay until the channel is rejoined.  This defaults to 5,
            but can be set to anything.  Some people may think you're rude if
            you set it to 0.
        :key rejoin_on_remove:
            Boolean defining whether to rejoin if you are 'removed'.  Note that
            most servers propogate REMOVE as KICK to clients so it won't always
            work (the sole exception in testing this extension was Freenode).
            Defaults to True, because REMOVE is silly anyway.

        """
        super().__init__(*args, **kwargs)
        self.rejoin_delay = kwargs.pop('rejoin_delay', 5)
        self.rejoin_on_remove = kwargs.pop('rejoin_on_remove', True)
        self.scheduled = {}
        if self.rejoin_on_remove:
            self.parts = set()

    @event('commands_out', 'PART')
    def on_part_out(self, _, line):
        """Command handler for PART's that are outgoing.

        This is used to ensure we know when we PART a channel, it's
        voluntary.

        """
        if not self.rejoin_on_remove:
            return
        isupport = self.base.isupport
        chantypes = isupport.get('CHANTYPES')
        for channel in line.params[0].split(','):
            if not channel.startswith(*chantypes):
                continue
            channel = self.casefold(channel)
            self.parts.add(channel)

    @event('commands', 'KICK')
    @event('commands', 'PART')
    def on_kick(self, _, line):
        """Command handler for KICK and PART.

        This method receives a line as its parameter, and will use it to
        determine if we were the ones kick/removed, and what action to take.

        """
        basicrfc = self.base.basic_rfc
        params = line.params
        channel = self.casefold(params[0])
        if self.casefold(params[1]) != self.casefold(basicrfc.nick):
            return
        if line.command == 'PART':
            if not self.rejoin_on_remove:
                return
            if channel in self.parts:
                self.parts.discard(channel)
                return
        if self.rejoin_on_remove:
            self.parts.discard(channel)
        if channel in self.scheduled:
            return
        future = self.schedule(self.rejoin_delay, partial(self.join, channel))
        self.scheduled[channel] = future

    def join(self, channel):
        """Join the specified channel and remove the channel from the pending
        rejoin list."""
        self.send('JOIN', [channel])
        self.parts.discard(channel)
        del self.scheduled[channel]

    @event('link', 'disconnected')
    def on_disconnected(self, _):
        """Disconnection event handler.

        We must ensure that any pending rejoins are unscheduled, so that
        we don't do something silly like sending JOIN to a closed
        socket.

        """
        for future in self.scheduled.values():
            try:
                self.unschedule(future)
            except ValueError:
                pass

        self.scheduled.clear()
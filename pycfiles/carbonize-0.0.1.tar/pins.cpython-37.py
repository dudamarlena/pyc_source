# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/contrib/pins.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 3953 bytes
__doc__ = 'This module provides the Pins contrib class'
import json, time, datetime
from ..handlers import CommandHandler, ReactionHandler
from ..dataclasses import Message, Reaction, MessageReaction
from .._i18n import _

class Pins(object):
    """Pins"""
    _db = []
    _db_file = None
    _pin_cmd = None
    _list_cmd = None
    _confirms = 0

    def __init__(self, db_file, pin_cmd='pin', list_cmd='list', confirms=0):
        self._db_file = db_file
        self._pin_cmd = pin_cmd
        self._list_cmd = list_cmd
        self._confirms = confirms
        self._load()

    def _load(self):
        with open(self._db_file) as (fd):
            self._db = json.load(fd)

    def _save(self):
        with open(self._db_file, 'w') as (fd):
            json.dump(self._db, fd)

    def add_pin(self, author, text, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self._db.append([timestamp, author, text])
        self._save()

    def _format_pin(self, pin):
        timestamp = datetime.datetime.fromtimestamp(pin[0]).strftime('%Y-%m-%d')
        out = '\n'.join([
         f"{pin[1]}, {timestamp}",
         '===',
         (f"{pin[2]}")])
        return out

    def get_page(self, n):
        pins = []
        for pin in self._db[::-1][5 * (n - 1):5 * n]:
            pins.append(self._format_pin(pin))

        return '\n\n'.join(pins)

    def _list_fn(self, message: Message, bot):
        if message.args.isnumeric():
            n = int(message.args)
        else:
            n = 1
        message.reply(self.get_page(n))

    def _pin_fn(self, message: Message, bot):
        if message.args:
            author = message.get_author_name()
            text = message.args
            timestamp = message.timestamp
        elif message.replied_to is not None:
            author = message.replied_to.get_author_name()
            text = message.replied_to.text
            timestamp = message.replied_to.timestamp
        else:
            message.reply(_('Please provide text or reply to a message to be pinned'))
            return
        if self._confirms == 0:
            self.add_pin(author, text, timestamp)
            message.reply(_('Message was pinned!'))
        else:
            mid = message.reply(_('Your pin is waiting for confirmation. ') + _('Ask {n} people to confirm it by reacting with ').format(n=(self._confirms)) + MessageReaction.YES.value)

            def _callback(reaction, bot):
                reactions = reaction.message.reactions
                if len([k for k, v in reactions.items() if v == MessageReaction.YES]) == self._confirms:
                    self.add_pin(author, text, timestamp)
                    message.reply(_('Message was pinned!'))

            bot.register(ReactionHandler(_callback, mid, timeout=120))

    def handlers(self):
        """Returns a list of handlers that need to be registered"""
        handlers = []
        handlers.append(CommandHandler(self._list_fn, self._list_cmd))
        handlers.append(CommandHandler(self._pin_fn, self._pin_cmd))
        return handlers
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/stibium/contrib/pins.py
# Compiled at: 2019-09-02 08:41:04
# Size of source mod 2**32: 3953 bytes
"""This module provides the Pins contrib class"""
import json, time, datetime
from ..handlers import CommandHandler, ReactionHandler
from ..dataclasses import Message, Reaction, MessageReaction
from .._i18n import _

class Pins(object):
    __doc__ = '\n    This class provides a system for pinning messages.\n\n    The messages can be pinned with the "pin" command by passing either\n    text as an argument, or by replying with it to a message.\n    By setting the `confirms` kwarg, this class can requre "confirmation"\n    of a pin by a set amount of reactions.\n    Pinned messages can be listed by the "list" command.\n    Both commands can be renamed with the `pin_cmd` and `list_cmd` kwargs.\n    Pinned messages are stored in json format at the location\n    specified by `db_file`.\n\n    This class provides two commands, so it has to be registered as:\n    `bot.register(*pins.handlers())`\n    '
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
        else:
            if message.replied_to is not None:
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
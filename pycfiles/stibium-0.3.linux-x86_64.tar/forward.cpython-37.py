# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/stibium/contrib/forward.py
# Compiled at: 2019-09-02 08:41:04
# Size of source mod 2**32: 3070 bytes
"""This class provides the Forward class"""
import attr
from ..handlers import CommandHandler, ReactionHandler
from ..dataclasses import Thread, ThreadType, Message, Reaction, MessageReaction
from .._i18n import _

@attr.s
class Forward(object):
    __doc__ = '\n    This class provides a system for forwarding messages to a group.\n\n    A selected account outside of a group can send a message to\n    a group, and any of the group users can respond to it.\n    The "send to group" command is by default called "send",\n    and "send to user" command is by default called "respond".\n    They can be changed by send_cmd and respond_cmd kwargs.\n\n    This class provides two commands, so it has to be registered as:\n    `bot.register(*forward.handlers())`\n    '
    _group_thread = attr.ib(converter=(Thread.from_group_uid))
    _user_thread = attr.ib(converter=(Thread.from_user_uid))
    _send_cmd = attr.ib(default='send')
    _respond_cmd = attr.ib(default='respond')

    def _send_fn(self, message: Message, bot_object):
        if message.thread != self._user_thread:
            message.reply(_("You can't use this command."))
            return
        else:
            message.args or message.reply(_('Please provide text to be sent.'))
            return
        bot_object.send(_('Message from {user}:\n{message}').format(user=(message.get_author_name()),
          message=(message.args)),
          thread=(self._group_thread))
        message.reply(_('The message was forwarded.'))

    def _respond_fn(self, message: Message, bot_object):
        if message.thread != self._group_thread:
            message.reply(_("You can't use this command."))
            return
        else:
            message.args or message.reply(_('Please provide text to be sent.'))
            return

        def _callback(reaction, bot_object):
            if reaction.uid == message.uid:
                if reaction.reaction == MessageReaction.YES:
                    bot_object.send(_('Message from {user}:\n{message}').format(user=(message.get_author_name()),
                      message=(message.args)),
                      thread=(self._user_thread))
                    message.reply(_('The message was forwarded.'))

        mid = message.reply(_('Are you sure you want to send this to {user}?\nPlease confirm by reacting {reaction}.').format(user=(bot_object.get_user_name(self._user_thread.id_)),
          reaction=(MessageReaction.YES.value)),
          reply=True)
        bot_object.register(ReactionHandler(_callback, mid, timeout=120))

    def handlers(self):
        """Returns a list of handlers that need to be registered"""
        handlers = []
        handlers.append(CommandHandler(self._send_fn, self._send_cmd))
        handlers.append(CommandHandler(self._respond_fn, self._respond_cmd))
        return handlers
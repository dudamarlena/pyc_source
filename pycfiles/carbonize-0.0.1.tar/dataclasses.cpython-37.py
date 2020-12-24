# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/dataclasses.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 3902 bytes
__doc__ = 'This module provides the data classes for Carbonium'
import attr
from fbchat.models import ThreadType, MessageReaction

@attr.s
class Thread(object):
    """Thread"""
    id_ = attr.ib(converter=str)
    type_ = attr.ib(default=(ThreadType.USER))

    @classmethod
    def fromkwargs(cls, kwargs):
        """Create a Thread class from a handler's kwargs"""
        id_ = kwargs.get('thread_id')
        if id_ is None:
            return
        return cls(id_=id_,
          type_=(kwargs.get('thread_type', ThreadType.USER)))

    @classmethod
    def from_user_uid(cls, uid):
        """
        Returns an USER Thread class, either from the argument
        or created from the passed UID.
        Can be passed either a ready Thread class or an UID.
        """
        if isinstance(uid, cls):
            return uid
        return cls(id_=uid, type_=(ThreadType.USER))

    @classmethod
    def from_group_uid(cls, uid):
        """
        Returns a GROUP Thread class, either from the argument
        or created from the passed UID.
        Can be passed either a ready Thread class or an UID.
        """
        if isinstance(uid, cls):
            return uid
        return cls(id_=uid, type_=(ThreadType.GROUP))


@attr.s
class Message(object):
    """Message"""
    mid = attr.ib()
    text = attr.ib()
    args = attr.ib(init=False)
    uid = attr.ib()
    thread = attr.ib()
    replied_to = attr.ib()
    timestamp = attr.ib()
    reactions = attr.ib()
    raw = attr.ib(repr=False)
    bot = attr.ib()

    def reply(self, text, **kwargs):
        """Send a message to a conversation that the message was received from"""
        if kwargs.get('reply', False):
            kwargs['reply'] = self.mid
        return (self.bot.send)(text, (self.thread), **kwargs)

    def get_author_name(self):
        """Get message author's name"""
        return self.bot.get_user_name(self.uid)

    @classmethod
    def fromkwargs(cls, kwargs, bot):
        """Create a Message class from a handler's kwargs"""
        return cls.from_model(model=(kwargs['message_object']),
          thread=(Thread.fromkwargs(kwargs)),
          bot=bot,
          raw=kwargs)

    @classmethod
    def from_model(cls, model, thread, bot, raw=None):
        """Create a Message class from fbchat.models.Message"""
        if model is None:
            return
        return cls(text=(model.text),
          uid=(model.author),
          mid=(model.uid),
          thread=thread,
          replied_to=(cls.from_model(model.replied_to, thread, bot)),
          timestamp=(float(model.timestamp) / 1000),
          reactions=(model.reactions),
          raw=raw,
          bot=bot)

    @classmethod
    def from_mid(cls, mid, thread, bot):
        """Create a Message class from a message ID"""
        return cls.from_model(bot.fbchat_client.fetchMessageInfo(mid, thread.id_), thread, bot)


@attr.s
class Reaction(object):
    """Reaction"""
    mid = attr.ib()
    reaction = attr.ib()
    uid = attr.ib()
    thread = attr.ib()
    raw = attr.ib()
    bot = attr.ib()
    _message = None

    @property
    def message(self):
        if self._message is None:
            self._message = Message.from_mid(self.mid, self.thread, self.bot)
        return self._message

    @classmethod
    def fromkwargs(cls, kwargs, bot):
        """Create a Reaction class from a handler's kwargs"""
        return cls(mid=(kwargs['mid']),
          reaction=(kwargs['reaction']),
          uid=(kwargs['author_id']),
          thread=(Thread.fromkwargs(kwargs)),
          raw=kwargs,
          bot=bot)
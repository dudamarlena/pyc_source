# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/handlers.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 5587 bytes
__doc__ = 'This module provides the classes for creating event handlers'
import re
from .dataclasses import Message, Reaction
from ._i18n import _

class BaseHandler(object):
    """BaseHandler"""
    event = None
    timeout = None
    handlerfn = None

    def __init__(self, handler=None, timeout=None):
        self.timeout = timeout
        if handler is not None:
            self.handlerfn = handler

    def setup(self, bot):
        pass

    def check(self, event, bot):
        return False

    def execute(self, event, bot):
        if callable(self.handlerfn):
            self.handlerfn(event, bot)


class CommandHandler(BaseHandler):
    """CommandHandler"""
    event = 'onMessage'
    command = None
    prefix = None
    regex = None
    timeout = None
    wait = False

    def __init__(self, handler, command, wait=False, timeout=None):
        super().__init__(handler=handler, timeout=timeout)
        self.command = command
        self.wait = wait

    def __repr__(self):
        return f"<{type(self).__name__} for {repr(self.command)}>"

    def setup(self, bot):
        self.prefix = bot.prefix
        self.regex = re.compile('^{prefix}\\s?{command}($|\\s(?P<args>.+))$'.format(prefix=(self.prefix),
          command=(self.command)), re.IGNORECASE)

    def check(self, event: Message, bot):
        if event.text is None:
            return False
        match = self.regex.match(event.text)
        if match is None:
            return False
        return True

    def execute(self, event, bot):
        match = self.regex.match(event.text)
        args = match.group('args') or 
        event.args = args
        if self.wait:
            event.reply(_('Please wait...'))
        super().execute(event, bot)

    @classmethod
    def create(cls, command, timeout=None, wait=False):

        def wrapper(fun):
            return cls(command=command, handler=fun, wait=wait, timeout=timeout)

        return wrapper


class ReactionHandler(BaseHandler):
    """ReactionHandler"""
    event = 'onReactionAdded'
    mid = None

    def __init__(self, handler, mid, timeout=None):
        super().__init__(handler=handler, timeout=timeout)
        self.mid = mid

    def __repr__(self):
        return f"<{type(self).__name__} mid={repr(self.mid)}>"

    def setup(self, bot):
        if isinstance(self.mid, Message):
            self.mid = self.mid.mid
        else:
            self.mid = str(self.mid)

    def check(self, event: Reaction, bot):
        if event.mid == self.mid:
            return True
        return False

    @classmethod
    def create(cls, mid, timeout=None):

        def wrapper(fun):
            return cls(handler=fun, mid=mid, timeout=timeout)

        return wrapper


class TimeoutHandler(BaseHandler):
    """TimeoutHandler"""
    event = '_timeout'

    def __init__(self, handler, timeout):
        if timeout is None:
            raise Exception(f"Timeout for {type(self).__name__} not provided")
        super().__init__(handler=handler, timeout=timeout)

    def execute(self, event, bot):
        if callable(self.handlerfn):
            self.handlerfn(event, bot)

    @classmethod
    def create(cls, timeout):

        def wrapper(fun):
            return cls(handler=fun, timeout=timeout)

        return wrapper


class RecurrentHandler(BaseHandler):
    """RecurrentHandler"""
    event = '_recurrent'

    def __init__(self, handler, nexthandler):
        super().__init__(handler=handler, timeout=None)
        if nexthandler is not None:
            self.nextfn = nexthandler

    def next_time(self, now):
        if callable(self.nextfn):
            return self.nextfn(now)

    @classmethod
    def create(cls, nexthandler):

        def wrapper(fun):
            return cls(handler=fun, nexthandler=nexthandler)

        return wrapper
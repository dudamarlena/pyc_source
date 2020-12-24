# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/routers.py
# Compiled at: 2020-04-18 16:07:01
# Size of source mod 2**32: 2075 bytes
import re
from .router import MapRouter, ListRouter
from .update import UpdateType

class CommandsRouter(MapRouter):
    __slots__ = ('_cache', )

    def __init__(self, priority=6):
        """Base priority is 6."""
        super().__init__(priority=priority)
        self._cache = None

    def _populate_cache(self, ctx):
        commands = list(self._handlers.keys())
        prefixes = ctx.config['prefixes']
        self._cache = re.compile(pattern='({prefix})({command})(?:$|\\s([\\s\\S]*))'.format(prefix=('|'.join((re.escape(p) for p in prefixes))),
          command=('|'.join((re.escape(c) for c in commands)))),
          flags=(re.IGNORECASE))

    def add_handler(self, handler, key):
        return super().add_handler(handler, key.lower())

    def _get_keys(self, update, ctx):
        if update.type != UpdateType.MSG:
            return ()
        if self._cache is None:
            self._populate_cache(ctx)
        match = self._cache.match(update.text)
        if match is None:
            return ()
        ctx.prefix = match.group(1)
        ctx.command = match.group(2)
        ctx.body = (match.group(3) or '').strip()
        ctx.match = match
        return (
         ctx.command.lower(),)


class AttachmentsRouter(MapRouter):
    __slots__ = ()

    def __init__(self, priority=3):
        """Base priority is 3."""
        super().__init__(priority=priority)

    def _get_keys(self, update, ctx):
        if update.type != UpdateType.MSG:
            return ()
        return tuple((a.type for a in update.attachments))


class AnyMessageRouter(ListRouter):
    __slots__ = ()

    def __init__(self, priority=9):
        """Base priority is 9."""
        super().__init__(priority=priority)

    def _check_update(self, update, ctx):
        return update.type == UpdateType.MSG and update.text.strip()


class AnyUnprocessedMessageRouter(AnyMessageRouter):
    __slots__ = ()

    def __init__(self, priority=-3):
        """Base priority is -3."""
        super().__init__(priority=priority)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/exception_handling.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 4929 bytes
"""
jishaku.exception_handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

Functions and classes for handling exceptions.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import asyncio, subprocess, traceback, typing, discord
from discord.ext import commands
from jishaku.flags import JISHAKU_NO_DM_TRACEBACK

async def send_traceback(destination: discord.abc.Messageable, verbosity: int, *exc_info):
    """
    Sends a traceback of an exception to a destination.
    Used when REPL fails for any reason.

    :param destination: Where to send this information to
    :param verbosity: How far back this traceback should go. 0 shows just the last stack.
    :param exc_info: Information about this exception, from sys.exc_info or similar.
    :return: The last message sent
    """
    etype, value, trace = exc_info
    traceback_content = ''.join(traceback.format_exception(etype, value, trace, verbosity)).replace('``', '`\u200b`')
    paginator = commands.Paginator(prefix='```py')
    for line in traceback_content.split('\n'):
        paginator.add_line(line)

    message = None
    for page in paginator.pages:
        message = await destination.send(page)

    return message


async def do_after_sleep(delay: float, coro, *args, **kwargs):
    """
    Performs an action after a set amount of time.

    This function only calls the coroutine after the delay,
    preventing asyncio complaints about destroyed coros.

    :param delay: Time in seconds
    :param coro: Coroutine to run
    :param args: Arguments to pass to coroutine
    :param kwargs: Keyword arguments to pass to coroutine
    :return: Whatever the coroutine returned.
    """
    await asyncio.sleep(delay)
    return await coro(*args, **kwargs)


async def attempt_add_reaction(msg: discord.Message, reaction: typing.Union[(str, discord.Emoji)]) -> typing.Optional[discord.Reaction]:
    """
    Try to add a reaction to a message, ignoring it if it fails for any reason.

    :param msg: The message to add the reaction to.
    :param reaction: The reaction emoji, could be a string or `discord.Emoji`
    :return: A `discord.Reaction` or None, depending on if it failed or not.
    """
    try:
        return await msg.add_reaction(reaction)
    except discord.HTTPException:
        pass


class ReactionProcedureTimer:
    __doc__ = '\n    Class that reacts to a message based on what happens during its lifetime.\n    '
    __slots__ = ('message', 'loop', 'handle', 'raised')

    def __init__(self, message: discord.Message, loop: typing.Optional[asyncio.BaseEventLoop]=None):
        self.message = message
        self.loop = loop or asyncio.get_event_loop()
        self.handle = None
        self.raised = False

    async def __aenter__(self):
        self.handle = self.loop.create_task(do_after_sleep(1, attempt_add_reaction, self.message, '▶'))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.handle:
            self.handle.cancel()
        elif not exc_val:
            await attempt_add_reaction(self.message, '✅')
            return
        else:
            self.raised = True
            if isinstance(exc_val, (asyncio.TimeoutError, subprocess.TimeoutExpired)):
                await attempt_add_reaction(self.message, '⏰')
            else:
                if isinstance(exc_val, SyntaxError):
                    await attempt_add_reaction(self.message, '❗')
                else:
                    await attempt_add_reaction(self.message, '‼')


class ReplResponseReactor(ReactionProcedureTimer):
    __doc__ = '\n    Extension of the ReactionProcedureTimer that absorbs errors, sending tracebacks.\n    '

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        if not exc_val:
            return
        else:
            if isinstance(exc_val, (SyntaxError, asyncio.TimeoutError, subprocess.TimeoutExpired)):
                await send_traceback(self.message.channel, 0, exc_type, exc_val, exc_tb)
            else:
                await send_traceback(self.message.channel if JISHAKU_NO_DM_TRACEBACK else self.message.author, 8, exc_type, exc_val, exc_tb)
            return True
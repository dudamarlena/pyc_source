# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/functools.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 3188 bytes
"""
jishaku.functools
~~~~~~~~~~~~~~~~~

Function-related tools for Jishaku.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import asyncio, functools, typing

def executor_function(sync_function: typing.Callable):
    """A decorator that wraps a sync function in an executor, changing it into an async function.

    This allows processing functions to be wrapped and used immediately as an async function.

    Examples
    ---------

    Pushing processing with the Python Imaging Library into an executor:

    .. code-block:: python3

        from io import BytesIO
        from PIL import Image

        from jishaku.functools import executor_function

        @executor_function
        def color_processing(color: discord.Color):
            with Image.new('RGB', (64, 64), color.to_rgb()) as im:
                buff = BytesIO()
                im.save(buff, 'png')

            buff.seek(0)
            return buff

        @bot.command()
        async def color(ctx: commands.Context, color: discord.Color=None):
            color = color or ctx.author.color
            buff = await color_processing(color=color)

            await ctx.send(file=discord.File(fp=buff, filename='color.png'))
    """

    @functools.wraps(sync_function)
    async def sync_wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        internal_function = (functools.partial)(sync_function, *args, **kwargs)
        return await loop.run_in_executor(None, internal_function)

    return sync_wrapper


class AsyncSender:
    __doc__ = '\n    Storage and control flow class that allows prettier value sending to async iterators.\n\n    Example\n    --------\n\n    .. code:: python3\n\n        async def foo():\n            print("foo yielding 1")\n            x = yield 1\n            print(f"foo received {x}")\n            yield 3\n\n        async for send, result in AsyncSender(foo()):\n            print(f"asyncsender received {result}")\n            send(2)\n\n    Produces:\n\n    .. code::\n\n        foo yielding 1\n        asyncsender received 1\n        foo received 2\n        asyncsender received 3\n    '
    __slots__ = ('iterator', 'send_value')

    def __init__(self, iterator):
        self.iterator = iterator
        self.send_value = None

    def __aiter__(self):
        return self._internal(self.iterator.__aiter__())

    async def _internal(self, base):
        try:
            while True:
                value = await base.asend(self.send_value)
                self.send_value = None
                yield (
                 self.set_send_value, value)

        except StopAsyncIteration:
            pass

    def set_send_value(self, value):
        """
        Sets the next value to be sent to the iterator.

        This is provided by iteration of this class and should
        not be called directly.
        """
        self.send_value = value
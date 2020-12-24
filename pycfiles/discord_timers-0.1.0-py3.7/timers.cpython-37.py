# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/discord/ext/timers/timers.py
# Compiled at: 2019-08-14 10:47:57
# Size of source mod 2**32: 7483 bytes
import collections.abc, datetime
from .utils import ListBasedQueue, chunked_sleep

class ChildTimer:
    __doc__ = 'A slimmed down timer class meant for internal use.'

    def __init__(self, name, expires, args=None, kwargs=None):
        if not isinstance(args, collections.abc.Iterable):
            if args is not None:
                raise TypeError('args must be an iterable, got {0!r}'.format(args.__class__.__name__))
        else:
            if kwargs is not None:
                if not isinstance(kwargs, dict):
                    raise TypeError('kwargs must be of type dict, got {0!r}'.format(args.__class__.__name__))
            if kwargs is not None and not all((isinstance(key, str) for key in kwargs.keys())):
                raise TypeError('kwargs keys must all be str')
        self._expires = self._convert_to_expires(expires)
        self.name = name
        self._args = args or tuple()
        self._kwargs = kwargs or {}

    def _convert_to_expires(self, expires):
        if isinstance(expires, (float, int)):
            return datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)
        if isinstance(expires, datetime.timedelta):
            return datetime.datetime.utcnow() + expires
        if isinstance(expires, datetime.datetime):
            return expires
        raise TypeError('expires must be one of int, float, datetime.datetime or datetime.timedelta. Got {0!r}'.format(expires.__class__.__name__))


class Timer(ChildTimer):
    __doc__ = 'A timer that spawns his own task.\n\n    Parameters\n    ----------\n    bot: :class:`discord.Client`\n        A discord.py client instance.\n    name: :class:`str`\n        Same as in :meth:`TimerManager.create_timer`.\n    expires: Union[:class:`float`, :class:`int`, :class:`datetime.datetime`, :class:`datetime.timedelta`]\n        Same as in :meth:`TimerManager.create_timer`.\n    args: :class:`~collections.abc.Iterable`\n        Same as in :meth:`TimerManager.create_timer`.\n    kwargs: Mapping[:class:`str`, Any]\n        Same as in :meth:`TimerManager.create_timer`.\n    '

    def __init__(self, bot, name, expires, args=None, kwargs=None):
        super().__init__(name, expires, args, kwargs)
        self._bot = bot
        self._task = None

    async def internal_task(self):
        await chunked_sleep((self._expires - datetime.datetime.utcnow()).total_seconds())
        (self._bot.dispatch)(self.name, *(self._args), **self._kwargs)

    @property
    def done(self):
        """::class:`bool` Whether the timer is done."""
        return self._task is not None and self._task.done()

    def start(self):
        """Start the timer.

        Returns
        -------
        :class:`Timer`
            The Timer started."""
        self._task = self._bot.loop.create_task(self.internal_task())
        return self

    def _check_task(self):
        if self._task is None:
            raise RuntimeError('Timer was never started.')
        if self._task.done():
            raise RuntimeError('Timer is already done.')

    def cancel(self):
        """Cancel the timer.

        Raises
        ------
        RuntimeError
            The timer was not launched or is already done."""
        self._check_task()
        self._task.cancel()

    @property
    def remaining(self):
        """::class:`int` The amount of seconds before the timer is done."""
        return (self._expires - datetime.datetime.utcnow()).total_seconds()

    async def join(self):
        """Wait until the timer is done.

        Raises
        ------
        RuntimeError
            The timer was not launched or is already done."""
        self._check_task()
        await self._task


class TimerManager:
    __doc__ = 'A class that manages timer dispatching with a single task.\n\n    Parameters\n    ----------\n    bot: :class:`discord.Client`\n        A discord.py client instance.'

    def __init__(self, bot):
        self._bot = bot
        self._TimerManager__timers = ListBasedQueue(loop=(bot.loop))
        self._current_timer = None
        self._task = self._bot.loop.create_task(self.poll_timers())

    async def poll_timers(self):
        while True:
            self._current_timer = timer = await self._TimerManager__timers.get()
            self._TimerManager__timers.task_done()
            time = (timer._expires - datetime.datetime.utcnow()).total_seconds()
            await chunked_sleep(time)
            (self._bot.dispatch)(timer.name, *(timer._args), **timer._kwargs)

    def create_timer(self, name, expires, args=None, kwargs=None):
        """Create a timer to be scheduled for dispatching

        Arguments
        ---------
        name: :class:`str`
            The name under which an event will be dispatched when the timer is complete.
        expires: Union[:class:`float`, :class:`int`, :class:`datetime.datetime`, :class:`datetime.timedelta`]
            If a :class:`float` or :class:`int`, the amount of seconds to sleep.
            If a :class:`datetime.datetime`, the UTC date at which the timer will finish.
            If a :class:`datetime.timedelta`, the delta relative to the current UTC date at which the timer will finish.
        args: :class:`~collections.abc.Iterable`
            An iterable of positional arguments passed to the dispatched event.
        kwargs: Mapping[:class:`str`, Any]
            A mapping of keyword arguments passed to the dispatched event.
        """
        timer = ChildTimer(name, expires, args, kwargs)
        if self._current_timer is not None and self._current_timer._expires > timer._expires:
            self._task.cancel()
            self._TimerManager__timers.put_nowait(self._current_timer)
            self._TimerManager__timers.put_nowait(timer)
            self._TimerManager__timers._queue.sort(key=(lambda x: x._expires))
            self._task = self._bot.loop.create_task(self.poll_timers())
        else:
            self._TimerManager__timers.put_nowait(timer)
            self._TimerManager__timers._queue.sort(key=(lambda x: x._expires))

    @property
    def done(self):
        """::class:`bool` Whether or not the enternal task is done."""
        return self._task.done()

    def cancel(self):
        """Cancel the internal task.

        Raises
        ------
        RuntimeError
            The manager is already done.
        """
        if self._task.done():
            raise RuntimeError('The manager is already done.')
        self._task.cancel()

    def clear(self):
        """Clear the timer queue and restart the internal task."""
        if not self._task.done():
            self._task.cancel()
        self._TimerManager__timers = ListBasedQueue(loop=(self._bot.loop))
        self._task = self._bot.loop.create_task(self.poll_timers())

    async def join(self):
        """Wait until there are no more timers to dispatch."""
        await self._TimerManager__timers.join()
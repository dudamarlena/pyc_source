# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\custom_clocks.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 16409 bytes
"""
Custom clocks used by cocos to perform special tasks, like:
    - recording a cocos app as a sequence of snapshots with an exact, fixed framerate
    - jump in a predefined sequence of timestamps taking snapshots

dev notes:
There's code duplication here, but having separated codepaths would help to
follow changes in pyglet 1.2dev. When released, we could refactor this with
some confidence.

References to the classes defined here are discouraged in code outside this
module because of possible changes.

The public interface should be
    - get_recorder_clock
    - set_app_clock
"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import pyglet, pyglet.clock

def get_recorder_clock(framerate, template, duration=0):
    """
    Returns a clock object suitable to be used as a pyglet app clock, which
    will provide a steady framerate, and saves a snapshot for each frame from
    time=0 to time=duration

    The clock object class depends on the pyglet version, and is set automatically

    :Parameters:
        `framerate` : int
            the number of frames per second
        `template` : str
            snapshot filenames will be template%frame_number (ex: "s%d.png" -> s0.png, s1.png...)
        `duration` : float
            the amount of seconds to record, or 0 for infinite
    """
    if pyglet.version.startswith('1.1'):
        clock = ScreenReaderClock(framerate, template, duration)
    else:
        clock = ScreenReaderClock_12dev(framerate, template, duration)
    return clock


def get_autotest_clock(sampler):
    """
    Returns a clock object suitable to be used as a pyglet app clock, which
    will follow a test plan to advance time and take snapshots.

    The clock object class depends on the pyglet version, and is determined automatically.

    :Parameters:
        `sampler` : obj
            obj with interface sampler.next(last_app_time) -> next_app_time
            Drives the app trough the desired states, take snapshots and handles
            the app termination conditions.
    """
    if pyglet.version.startswith('1.1'):
        clock = AutotestClock(sampler)
    else:
        clock = AutotestClock_12dev(sampler)
    return clock


def set_app_clock(clock):
    """
    Sets the cocos (or pyglet) app clock to a custom one
    """
    if pyglet.version.startswith('1.1'):
        pyglet.clock._default = clock
    else:
        pyglet.app.event_loop.clock = clock
        pyglet.clock._default = clock
        pyglet.app.event_loop._run_estimated = pyglet.app.event_loop._run


class ScreenReaderClock(pyglet.clock.Clock):
    __doc__ = ' Make frames happen every 1/framerate and takes screenshots\n\n        This class is compatible with pyglet 1.1.4release, it is not compatible\n        with pyglet 1.2dev\n    '

    def __init__(self, framerate, template, duration):
        super(ScreenReaderClock, self).__init__()
        self.framerate = float(framerate)
        self.template = template
        self.duration = duration
        self.frameno = 0
        self.fake_time = 0

    def tick(self, poll=False):
        """Signify that one frame has passed.

        """
        self._screenshot_logic()
        ts = self._get_ts()
        if self.last_ts is None:
            delta_t = 0
        else:
            delta_t = ts - self.last_ts
            self.times.insert(0, delta_t)
            if len(self.times) > self.window_size:
                self.cumulative_time -= self.times.pop()
        self.cumulative_time += delta_t
        self.last_ts = ts
        for item in list(self._schedule_items):
            (item.func)(delta_t, *(item.args), **item.kwargs)

        need_resort = False
        for item in list(self._schedule_interval_items):
            if item.next_ts > ts:
                break
            (item.func)(ts - item.last_ts, *(item.args), **item.kwargs)
            if item.interval:
                item.next_ts = item.last_ts + item.interval
                item.last_ts = ts
                if item.next_ts <= ts:
                    if ts - item.next_ts < 0.05:
                        item.next_ts = ts + item.interval
                    else:
                        item.next_ts = self._get_soft_next_ts(ts, item.interval)
                        item.last_ts = item.next_ts - item.interval
                need_resort = True

        self._schedule_interval_items = [item for item in self._schedule_interval_items if item.next_ts > ts]
        if need_resort:
            self._schedule_interval_items.sort(key=(lambda a: a.next_ts))
        return delta_t

    def _screenshot_logic(self):
        """takes screenshots, handles end of screenshot session"""
        pyglet.image.get_buffer_manager().get_color_buffer().save(self.template % self.frameno)
        self.frameno += 1
        if self.duration:
            if self.fake_time > self.duration:
                raise SystemExit()

    def _get_ts(self):
        """handles the time progression"""
        ts = self.fake_time
        self.fake_time = self.frameno / self.framerate
        return ts


class ScreenReaderClock_12dev(pyglet.clock.Clock):
    __doc__ = ' Make frames happen every 1/framerate and takes screenshots\n\n        This class is compatible with pyglet 1.2dev, it is not compatible\n        with pyglet 1.1.4release\n    '

    def __init__(self, framerate, template, duration):
        super(ScreenReaderClock_12dev, self).__init__()
        self.framerate = float(framerate)
        self.template = template
        self.duration = duration
        self.frameno = 0
        self.fake_time = 0.0

    def update_time(self):
        """Get the (fake) elapsed time since the last call to `update_time`
            Additionally, take snapshots.

        :rtype: float
        :return: The number of seconds since the last `update_time`, or 0
            if this was the first time it was called.
        """
        self._screenshot_logic()
        ts = self._get_ts()
        if self.last_ts is None:
            delta_t = 0
        else:
            delta_t = ts - self.last_ts
            self.times.insert(0, delta_t)
            if len(self.times) > self.window_size:
                self.cumulative_time -= self.times.pop()
        self.cumulative_time += delta_t
        self.last_ts = ts
        return delta_t

    def get_sleep_time(self, sleep_idle):
        """sleep time between frames; 0.0 as as we want to run as fast as possible"""
        return 0.0

    def _screenshot_logic(self):
        """takes screenshots, handles end of screenshot session"""
        pyglet.image.get_buffer_manager().get_color_buffer().save(self.template % self.frameno)
        self.frameno += 1
        if self.duration:
            if self.fake_time > self.duration:
                raise SystemExit()

    def _get_ts(self):
        """handles the time progression"""
        ts = self.fake_time
        self.fake_time = self.frameno / self.framerate
        return ts


class AutotestClock(pyglet.clock.Clock):
    __doc__ = 'Make frames follow a test plan\n\n        This class is compatible with pyglet 1.1.4release, it is not compatible\n        with pyglet 1.2dev\n    '

    def __init__(self, screen_sampler):
        super(AutotestClock, self).__init__()
        self.screen_sampler = screen_sampler

    def tick(self, poll=False):
        ts = self.screen_sampler.next(self.last_ts)
        if self.last_ts is None:
            delta_t = 0
        else:
            delta_t = ts - self.last_ts
            self.times.insert(0, delta_t)
            if len(self.times) > self.window_size:
                self.cumulative_time -= self.times.pop()
        self.cumulative_time += delta_t
        self.last_ts = ts
        for item in list(self._schedule_items):
            (item.func)(delta_t, *(item.args), **item.kwargs)

        need_resort = False
        for item in list(self._schedule_interval_items):
            if item.next_ts > ts:
                break
            (item.func)(ts - item.last_ts, *(item.args), **item.kwargs)
            if item.interval:
                item.next_ts = item.last_ts + item.interval
                item.last_ts = ts
                if item.next_ts <= ts:
                    if ts - item.next_ts < 0.05:
                        item.next_ts = ts + item.interval
                    else:
                        item.next_ts = self._get_soft_next_ts(ts, item.interval)
                        item.last_ts = item.next_ts - item.interval
                need_resort = True

        self._schedule_interval_items = [item for item in self._schedule_interval_items if item.next_ts > ts]
        if need_resort:
            self._schedule_interval_items.sort(key=(lambda a: a.next_ts))
        return delta_t

    def get_sleep_time(self, sleep_idle):
        return 0


class AutotestClock_12dev(pyglet.clock.Clock):
    __doc__ = 'Make frames follow a test plan\n\n        This class is compatible with pyglet 1.2dev, it is not compatible\n        with pyglet 1.1.4release\n    '

    def __init__(self, screen_sampler):
        super(AutotestClock_12dev, self).__init__()
        self.screen_sampler = screen_sampler

    def update_time(self):
        """Get the (fake) elapsed time since the last call to `update_time`
            Additionally, take snapshots.

        :rtype: float
        :return: The number of seconds since the last `update_time`, or 0
            if this was the first time it was called.
        """
        ts = self.screen_sampler.next(self.last_ts)
        if self.last_ts is None:
            delta_t = 0
        else:
            delta_t = ts - self.last_ts
            self.times.insert(0, delta_t)
            if len(self.times) > self.window_size:
                self.cumulative_time -= self.times.pop()
        self.cumulative_time += delta_t
        self.last_ts = ts
        return delta_t

    def get_sleep_time(self, sleep_idle):
        """sleep time between frames; 0.0 as as we want to run as fast as possible"""
        return 0.0
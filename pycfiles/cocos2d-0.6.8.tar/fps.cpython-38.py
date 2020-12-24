# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../..\cocos\fps.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 9897 bytes
"""
Support to collect and display fps stats.

The default fps support calculates very simple stats and provides a view for director to display.
This is enough most of the time, if more functionality is desired then

    - Define your own FpsStatsABC subclass with the desired behavior.
    - Define a callable that returns an instance of your custom subclass.
    - Assign the callable to `director.fps_display_provider`.
    - If other stats handler is running, do `director.show_FPS=False` or ctrl + X to cleanly terminate it.
    - re-enable stats collection with ctrl + X (interactive) or by `director.show_FPS=True` (programatically).
    - your subclass instance will be called as described in :class:FpsStatsABC.
"""
from __future__ import division, print_function, unicode_literals
import abc, sys, time, six
try:
    from pyglet.clock import ClockDisplay
except ImportError:
    import pyglet.window as ClockDisplay
else:
    import pyglet.font
    __docformat__ = 'restructuredtext'

    @six.add_metaclass(abc.ABCMeta)
    class FpsStatsABC(object):
        __doc__ = 'Interface to collect fps stats, optionally maintains a view\n\n    Methods are called by director at appropriate times.\n    '

        @abc.abstractmethod
        def init(self):
            """Called once before any other method; performs initialization.

        The window and the associated OpenGL context is guaranteed to exist
        at the time of calling.

        Usually used to create the Label to display fps stats.
        """
            pass

        @abc.abstractmethod
        def tick(self):
            """Called each time the active scene has been draw; updates the stats

        If there is a view its data can be eventually updated.
        """
            pass

        @abc.abstractmethod
        def draw(self):
            """Opportunity to draw stats on top of the active scene, called after tick.

        Normally it draws itself in the window, but can be implemented with a
        'pass' if the object is designed to gather stats and not display them.
        """
            pass

        @abc.abstractmethod
        def terminate(self):
            """last call to this object, opportunity to cleanup / store data."""
            pass


    class FpsDisplay(FpsStatsABC):
        __doc__ = "Calculates fps and min fps, maintains a Label view for director to display them.\n\n    Arguments:\n        fn_time : function\n            Provides time in seconds to calculate deltas\n            Assumes fn_time minimum dt < dt between frames, usually time.perf_counter (needs python 3.3+)\n\n    min fps capped at 5000, it can also be 5000 if no frame has rendered in the refresh interval\n\n    Don't use time.clock as fn_time in platforms other than windows: it will flow\n    slower than wall time.\n    "
        template = 'fps {0:4d} minfps {1:4d}'

        def __init__(self, fn_time):
            self.fn_time = fn_time
            self.dt_refresh = 0.25
            self.label = None
            self.fps = 0
            self.min_fps = 1
            t = self.fn_time()
            self.complete_refresh(t)

        def init(self):
            """Creates the label used to display fps info."""
            self.label = InfoLabel(self.template)

        def tick(self):
            """Called after the active scene was drawn. Updates stats."""
            t = self.fn_time()
            dt = t - self.prev_time
            self.prev_time = t
            self.cnt_frames += 1
            if self.max_dt < dt:
                self.max_dt = dt
            if t > self.next_refresh_time:
                self.fps = int(self.cnt_frames / (t - self.start_refresh_time))
                self.min_fps = int(1.0 / self.max_dt)
                self.complete_refresh(t)
                self.label.update_info(self.fps, self.min_fps)

        def complete_refresh(self, t):
            """re-initializes data for the next stats time interval."""
            self.prev_time = t
            self.start_refresh_time = t
            self.next_refresh_time = t + self.dt_refresh
            self.cnt_frames = 0
            self.max_dt = 0.0002

        def draw(self):
            """Draws the fps view."""
            self.label.draw()

        def terminate(self):
            """Nothing needed, so nothing done."""
            pass


    class FpsDisplaySimple(FpsStatsABC):
        __doc__ = "Calculates fps, creates and maintains a Label view for director to display it.\n\n    Arguments:\n        fn_time (function): provide time in seconds to calculate deltas; usually time.time is used\n\n    Don't use time.clock as fn_time in platforms other than windows: it will flow\n    slower than wall time.\n    "
        template = 'fps {0:4d}'

        def __init__(self, fn_time):
            self.fn_time = fn_time
            self.dt_refresh = 0.25
            self.label = None
            self.fps = 0
            t = self.fn_time()
            self.complete_refresh(t)

        def init(self):
            """Creates the label used to display fps"""
            self.label = InfoLabel(self.template)

        def tick(self):
            """Called after the active scene was drawn. Updates stats"""
            t = self.fn_time()
            if t > self.next_refresh_time:
                self.fps = int(self.cnt_frames / (t - self.start_refresh_time))
                self.complete_refresh(t)
                self.label.update_info(self.fps)
            else:
                self.cnt_frames += 1

        def complete_refresh(self, t):
            """re-initializes data for the next stats time interval"""
            self.start_refresh_time = t
            self.next_refresh_time = t + self.dt_refresh
            self.cnt_frames = 0

        def draw(self):
            """Draws the fps view"""
            self.label.draw()

        def terminate(self):
            """Nothing needed, so nothing done"""
            pass


    class FpsDisplayDeprecatedPygletOldStyle(FpsStatsABC):
        __doc__ = 'Calculates fps and maintains a view (not recommended for new code)\n\n    Delegates to (deprecated) pyglet.clock.ClockDisplay.\n\n    Measurements are comparable to the ones obtained in cocos <= 0.6.3\n    '

        def init(self):
            self.fps_display = ClockDisplay()

        def tick(self):
            pass

        def draw(self):
            self.fps_display.draw()

        def terminate(self):
            self.fps_display.unschedule()
            self.fps_display = None


    class InfoLabel(object):
        __doc__ = 'Used to draw one liners on top of the scene drawing'

        def __init__(self, template, font=None, color=(0.5, 0.5, 0.5, 0.5)):
            raise


    class InfoLabel(object):
        __doc__ = 'Used to draw one liners on top of the scene drawing'

        def __init__(self, template, font_name=None, font_size=36, color=(128, 128, 128, 128)):
            if not font_name is not None or isinstance(font_name, six.string_types):
                if isinstance(font_size, int):
                    if not (isinstance(color, tuple) and isinstance(color[0], int)):
                        raise TypeError('Bad type(s) in call to cocos.fps.InfoLabel, correct caller code or use cocos version <= 0.6.5 and pyglet version <= 1.3.2 ')
            self.template = template
            self.label = pyglet.text.Label('', font_name=font_name, font_size=font_size, color=color, x=10, y=10)

        def update_info(self, *args):
            self.label.text = (self.template.format)(*args)

        def draw(self):
            self.label.draw()


    def get_default_fpsdisplay():
        """returns an FpsStatsABC instance used to collect and display fps information."""
        major, minor = tuple(sys.version_info[:2])
        if not (major > 3 or major) == 3 or minor >= 3:
            fps_display = FpsDisplay(time.perf_counter)
        else:
            fn_time = time.clock if sys.platform.startswith('win32') else time.time
            fps_display = FpsDisplaySimple(fn_time)
        return fps_display
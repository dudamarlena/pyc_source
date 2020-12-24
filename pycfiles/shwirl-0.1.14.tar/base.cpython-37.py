# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/app/base.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 10322 bytes
from ..util import SimpleBunch
import time
from timeit import default_timer

class BaseApplicationBackend(object):
    __doc__ = 'BaseApplicationBackend()\n\n    Abstract class that provides an interface between backends and Application.\n    Each backend must implement a subclass of ApplicationBackend, and\n    implement all its _vispy_xxx methods.\n    '

    def _vispy_get_backend_name(self):
        raise NotImplementedError()

    def _vispy_process_events(self):
        raise NotImplementedError()

    def _vispy_run(self):
        raise NotImplementedError()

    def _vispy_reuse(self):
        pass

    def _vispy_quit(self):
        raise NotImplementedError()

    def _vispy_get_native_app(self):
        return self

    def _vispy_sleep(self, duration_sec):
        time.sleep(duration_sec)


class BaseCanvasBackend(object):
    __doc__ = "BaseCanvasBackend(vispy_canvas, capability, context_type)\n\n    Abstract class that provides an interface between backends and Canvas.\n    Each backend must implement a subclass of CanvasBackend, and\n    implement all its _vispy_xxx methods. Also, also a backend must\n    make sure to generate the following events: 'initialize', 'resize',\n    'draw', 'mouse_press', 'mouse_release', 'mouse_move',\n    'mouse_wheel', 'key_press', 'key_release'. When a backend detects\n    that the canvas should be closed, the backend should call\n    'self._vispy_canvas.close', because the close event is handled within\n    the canvas itself.\n    "

    def __init__(self, vispy_canvas):
        from .canvas import Canvas
        assert isinstance(vispy_canvas, Canvas)
        self._vispy_canvas = vispy_canvas
        self._last_time = 0
        vispy_canvas._backend = self
        self._vispy_mouse_data = {'buttons':[],  'press_event':None, 
         'last_event':None, 
         'last_mouse_press':None}

    def _process_backend_kwargs(self, kwargs):
        """ Simple utility to retrieve kwargs in predetermined order.
        Also checks whether the values of the backend arguments do not
        violate the backend capabilities.
        """
        app = self._vispy_canvas.app
        capability = app.backend_module.capability
        if kwargs['context'].shared.name:
            if not capability['context']:
                raise RuntimeError('Cannot share context with this backend')
        for key in [key for key, val in capability.items() if not val]:
            if key in ('context', 'multi_window', 'scroll'):
                continue
            invert = key in ('resizable', 'decorate')
            if bool(kwargs[key]) - invert:
                raise RuntimeError('Config %s is not supported by backend %s' % (
                 key, app.backend_name))

        out = SimpleBunch()
        keys = ['title', 'size', 'position', 'show', 'vsync', 'resizable',
         'decorate', 'fullscreen', 'parent', 'context', 'always_on_top']
        for key in keys:
            out[key] = kwargs[key]

        return out

    def _vispy_set_current(self):
        raise NotImplementedError()

    def _vispy_swap_buffers(self):
        raise NotImplementedError()

    def _vispy_set_title(self, title):
        raise NotImplementedError()

    def _vispy_set_size(self, w, h):
        raise NotImplementedError()

    def _vispy_set_position(self, x, y):
        raise NotImplementedError()

    def _vispy_set_visible(self, visible):
        raise NotImplementedError()

    def _vispy_set_fullscreen(self, fullscreen):
        raise NotImplementedError()

    def _vispy_update(self):
        raise NotImplementedError()

    def _vispy_close(self):
        raise NotImplementedError()

    def _vispy_get_size(self):
        raise NotImplementedError()

    def _vispy_get_physical_size(self):
        return self._vispy_get_size()

    def _vispy_get_position(self):
        raise NotImplementedError()

    def _vispy_get_fullscreen(self):
        raise NotImplementedError()

    def _vispy_get_geometry(self):
        x, y = self._vispy_get_position()
        w, h = self._vispy_get_size()
        return (x, y, w, h)

    def _vispy_get_native_canvas(self):
        return self

    def _vispy_mouse_press(self, **kwargs):
        kwargs.update(self._vispy_mouse_data)
        ev = (self._vispy_canvas.events.mouse_press)(**kwargs)
        if self._vispy_mouse_data['press_event'] is None:
            self._vispy_mouse_data['press_event'] = ev
        self._vispy_mouse_data['buttons'].append(ev.button)
        self._vispy_mouse_data['last_event'] = ev
        if not getattr(self, '_double_click_supported', False):
            self._vispy_detect_double_click(ev)
        return ev

    def _vispy_mouse_move(self, **kwargs):
        if default_timer() - self._last_time < 0.01:
            return
            self._last_time = default_timer()
            kwargs.update(self._vispy_mouse_data)
            if self._vispy_mouse_data['press_event'] is None:
                last_event = self._vispy_mouse_data['last_event']
                if last_event is not None:
                    last_event._forget_last_event()
        else:
            kwargs['button'] = self._vispy_mouse_data['press_event'].button
        ev = (self._vispy_canvas.events.mouse_move)(**kwargs)
        self._vispy_mouse_data['last_event'] = ev
        return ev

    def _vispy_mouse_release(self, **kwargs):
        kwargs.update(self._vispy_mouse_data)
        ev = (self._vispy_canvas.events.mouse_release)(**kwargs)
        if self._vispy_mouse_data['press_event']:
            if self._vispy_mouse_data['press_event'].button == ev.button:
                self._vispy_mouse_data['press_event'] = None
        if ev.button in self._vispy_mouse_data['buttons']:
            self._vispy_mouse_data['buttons'].remove(ev.button)
        self._vispy_mouse_data['last_event'] = ev
        return ev

    def _vispy_mouse_double_click(self, **kwargs):
        kwargs.update(self._vispy_mouse_data)
        ev = (self._vispy_canvas.events.mouse_double_click)(**kwargs)
        self._vispy_mouse_data['last_event'] = ev
        return ev

    def _vispy_detect_double_click(self, ev, **kwargs):
        dt_max = 0.3
        lastev = self._vispy_mouse_data['last_mouse_press']
        if lastev is None:
            self._vispy_mouse_data['last_mouse_press'] = ev
            return
        assert lastev.type == 'mouse_press'
        assert ev.type == 'mouse_press'
        if (ev.time - lastev.time <= dt_max) & (lastev.pos[0] - ev.pos[0] == 0) & (lastev.pos[1] - ev.pos[1] == 0) & (lastev.button == ev.button):
            (self._vispy_mouse_double_click)(**kwargs)
        self._vispy_mouse_data['last_mouse_press'] = ev


class BaseTimerBackend(object):
    __doc__ = 'BaseTimerBackend(vispy_timer)\n\n    Abstract class that provides an interface between backends and Timer.\n    Each backend must implement a subclass of TimerBackend, and\n    implement all its _vispy_xxx methods.\n    '

    def __init__(self, vispy_timer):
        self._vispy_timer = vispy_timer

    def _vispy_start(self, interval):
        raise NotImplementedError

    def _vispy_stop(self):
        raise NotImplementedError

    def _vispy_get_native_timer(self):
        return self
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/progressbar.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 9547 bytes
"""Main ProgressBar class."""
from __future__ import division
import math, os, signal, sys, time
try:
    from fcntl import ioctl
    from array import array
    import termios
except ImportError:
    pass
else:
    from .compat import *
    from . import widgets

    class UnknownLength:
        pass


    class ProgressBar(object):
        __doc__ = "The ProgressBar class which updates and prints the bar.\n\n    A common way of using it is like:\n    >>> pbar = ProgressBar().start()\n    >>> for i in range(100):\n    ...    # do something\n    ...    pbar.update(i+1)\n    ...\n    >>> pbar.finish()\n\n    You can also use a ProgressBar as an iterator:\n    >>> progress = ProgressBar()\n    >>> for i in progress(some_iterable):\n    ...    # do something\n    ...\n\n    Since the progress bar is incredibly customizable you can specify\n    different widgets of any type in any order. You can even write your own\n    widgets! However, since there are already a good number of widgets you\n    should probably play around with them before moving on to create your own\n    widgets.\n\n    The term_width parameter represents the current terminal width. If the\n    parameter is set to an integer then the progress bar will use that,\n    otherwise it will attempt to determine the terminal width falling back to\n    80 columns if the width cannot be determined.\n\n    When implementing a widget's update method you are passed a reference to\n    the current progress bar. As a result, you have access to the\n    ProgressBar's methods and attributes. Although there is nothing preventing\n    you from changing the ProgressBar you should treat it as read only.\n\n    Useful methods and attributes include (Public API):\n     - currval: current progress (0 <= currval <= maxval)\n     - maxval: maximum (and final) value\n     - finished: True if the bar has finished (reached 100%)\n     - start_time: the time when start() method of ProgressBar was called\n     - seconds_elapsed: seconds elapsed since start_time and last call to\n                        update\n     - percentage(): progress in percent [0..100]\n    "
        __slots__ = ('currval', 'fd', 'finished', 'last_update_time', 'left_justify',
                     'maxval', 'next_update', 'num_intervals', 'poll', 'seconds_elapsed',
                     'signal_set', 'start_time', 'term_width', 'update_interval',
                     'widgets', '_time_sensitive', '__iterable')
        _DEFAULT_MAXVAL = 100
        _DEFAULT_TERMSIZE = 80
        _DEFAULT_WIDGETS = [widgets.Percentage(), ' ', widgets.Bar()]

        def __init__(self, maxval=None, widgets=None, term_width=None, poll=1, left_justify=True, fd=sys.stderr):
            """Initializes a progress bar with sane defaults."""
            if widgets is None:
                widgets = list(self._DEFAULT_WIDGETS)
            self.maxval = maxval
            self.widgets = widgets
            self.fd = fd
            self.left_justify = left_justify
            self.signal_set = False
            if term_width is not None:
                self.term_width = term_width
            else:
                try:
                    self._handle_resize()
                    signal.signal(signal.SIGWINCH, self._handle_resize)
                    self.signal_set = True
                except (SystemExit, KeyboardInterrupt):
                    raise
                except:
                    self.term_width = self._env_size()
                else:
                    self._ProgressBar__iterable = None
                    self._update_widgets()
                    self.currval = 0
                    self.finished = False
                    self.last_update_time = None
                    self.poll = poll
                    self.seconds_elapsed = 0
                    self.start_time = None
                    self.update_interval = 1
                    self.next_update = 0

        def __call__(self, iterable):
            """Use a ProgressBar to iterate through an iterable."""
            try:
                self.maxval = len(iterable)
            except:
                if self.maxval is None:
                    self.maxval = UnknownLength
            else:
                self._ProgressBar__iterable = iter(iterable)
                return self

        def __iter__(self):
            return self

        def __next__--- This code section failed: ---

 L. 154         0  SETUP_FINALLY        54  'to 54'

 L. 155         2  LOAD_GLOBAL              next
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _ProgressBar__iterable
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'value'

 L. 156        12  LOAD_FAST                'self'
               14  LOAD_ATTR                start_time
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 157        22  LOAD_FAST                'self'
               24  LOAD_METHOD              start
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
               30  JUMP_FORWARD         48  'to 48'
             32_0  COME_FROM            20  '20'

 L. 159        32  LOAD_FAST                'self'
               34  LOAD_METHOD              update
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                currval
               40  LOAD_CONST               1
               42  BINARY_ADD       
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
             48_0  COME_FROM            30  '30'

 L. 160        48  LOAD_FAST                'value'
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L. 161        54  DUP_TOP          
               56  LOAD_GLOBAL              StopIteration
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   100  'to 100'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 162        68  LOAD_FAST                'self'
               70  LOAD_ATTR                start_time
               72  LOAD_CONST               None
               74  COMPARE_OP               is
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 163        78  LOAD_FAST                'self'
               80  LOAD_METHOD              start
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          
             86_0  COME_FROM            76  '76'

 L. 164        86  LOAD_FAST                'self'
               88  LOAD_METHOD              finish
               90  CALL_METHOD_0         0  ''
               92  POP_TOP          

 L. 165        94  RAISE_VARARGS_0       0  'reraise'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            60  '60'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'

Parse error at or near `POP_TOP' instruction at offset 64

        next = __next__

        def _env_size(self):
            """Tries to find the term_width from the environment."""
            return int(os.environ.get('COLUMNS', self._DEFAULT_TERMSIZE)) - 1

        def _handle_resize(self, signum=None, frame=None):
            """Tries to catch resize signals sent from the terminal."""
            h, w = array('h', ioctl(self.fd, termios.TIOCGWINSZ, '\x00\x00\x00\x00\x00\x00\x00\x00'))[:2]
            self.term_width = w

        def percentage(self):
            """Returns the progress as a percentage."""
            if self.currval >= self.maxval:
                return 100.0
            if self.maxval:
                return self.currval * 100.0 / self.maxval
            return 100.0

        percent = property(percentage)

        def _format_widgets(self):
            result = []
            expanding = []
            width = self.term_width
            for index, widget in enumerate(self.widgets):
                if isinstance(widget, widgets.WidgetHFill):
                    result.appendwidget
                    expanding.insert(0, index)
                else:
                    widget = widgets.format_updatable(widget, self)
                    result.appendwidget
                    width -= len(widget)
            else:
                count = len(expanding)
                while count:
                    portion = max(int(math.ceil(width * 1.0 / count)), 0)
                    index = expanding.pop()
                    count -= 1
                    widget = result[index].update(self, portion)
                    width -= len(widget)
                    result[index] = widget

                return result

        def _format_line(self):
            """Joins the widgets and justifies the line."""
            widgets = ''.joinself._format_widgets()
            if self.left_justify:
                return widgets.ljustself.term_width
            return widgets.rjustself.term_width

        def _need_update(self):
            """Returns whether the ProgressBar should redraw the line."""
            if self.currval >= self.next_update or self.finished:
                return True
            delta = time.time() - self.last_update_time
            return self._time_sensitive and delta > self.poll

        def _update_widgets(self):
            """Checks all widgets for the time sensitive bit."""
            self._time_sensitive = any((getattr(w, 'TIME_SENSITIVE', False) for w in self.widgets))

        def update(self, value=None):
            """Updates the ProgressBar to a new value."""
            if value is not None:
                if value is not UnknownLength:
                    if self.maxval is not UnknownLength:
                        if not 0 <= value <= self.maxval:
                            raise ValueError('Value out of range')
                    self.currval = value
            else:
                return self._need_update() or None
            if self.start_time is None:
                raise RuntimeError('You must call "start" before calling "update"')
            now = time.time()
            self.seconds_elapsed = now - self.start_time
            self.next_update = self.currval + self.update_interval
            self.fd.write(self._format_line() + '\r')
            self.fd.flush()
            self.last_update_time = now

        def start(self):
            """Starts measuring time, and prints the bar at 0%.

        It returns self so you can use it like this:
        >>> pbar = ProgressBar().start()
        >>> for i in range(100):
        ...    # do something
        ...    pbar.update(i+1)
        ...
        >>> pbar.finish()
        """
            if self.maxval is None:
                self.maxval = self._DEFAULT_MAXVAL
            self.num_intervals = max(100, self.term_width)
            self.next_update = 0
            if self.maxval is not UnknownLength:
                if self.maxval < 0:
                    raise ValueError('Value out of range')
                self.update_interval = self.maxval / self.num_intervals
            self.start_time = self.last_update_time = time.time()
            self.update0
            return self

        def finish(self):
            """Puts the ProgressBar bar in the finished state."""
            if self.finished:
                return
            self.finished = True
            self.updateself.maxval
            self.fd.write'\n'
            if self.signal_set:
                signal.signal(signal.SIGWINCH, signal.SIG_DFL)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/widgets.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 11224 bytes
"""Default ProgressBar widgets."""
from __future__ import division
import datetime, math
try:
    from abc import ABCMeta, abstractmethod
except ImportError:
    AbstractWidget = object
    abstractmethod = lambda fn: fn
else:
    AbstractWidget = ABCMeta('AbstractWidget', (object,), {})

def format_updatable(updatable, pbar):
    if hasattr(updatable, 'update'):
        return updatable.update(pbar)
    return updatable


class Widget(AbstractWidget):
    __doc__ = "The base class for all widgets.\n\n    The ProgressBar will call the widget's update value when the widget should\n    be updated. The widget's size may change between calls, but the widget may\n    display incorrectly if the size changes drastically and repeatedly.\n\n    The boolean TIME_SENSITIVE informs the ProgressBar that it should be\n    updated more often because it is time sensitive.\n    "
    TIME_SENSITIVE = False
    __slots__ = ()

    @abstractmethod
    def update(self, pbar):
        """Updates the widget.

        pbar - a reference to the calling ProgressBar
        """
        pass


class WidgetHFill(Widget):
    __doc__ = 'The base class for all variable width widgets.\n\n    This widget is much like the \\hfill command in TeX, it will expand to\n    fill the line. You can use more than one in the same line, and they will\n    all have the same width, and together will fill the line.\n    '

    @abstractmethod
    def update(self, pbar, width):
        """Updates the widget providing the total width the widget must fill.

        pbar - a reference to the calling ProgressBar
        width - The total width the widget must fill
        """
        pass


class Timer(Widget):
    __doc__ = 'Widget which displays the elapsed seconds.'
    __slots__ = ('format_string', )
    TIME_SENSITIVE = True

    def __init__(self, format='Elapsed Time: %s'):
        self.format_string = format

    @staticmethod
    def format_time(seconds):
        """Formats time as the string "HH:MM:SS"."""
        return str(datetime.timedelta(seconds=(int(seconds))))

    def update(self, pbar):
        """Updates the widget to show the elapsed time."""
        return self.format_string % self.format_time(pbar.seconds_elapsed)


class ETA(Timer):
    __doc__ = 'Widget which attempts to estimate the time of arrival.'
    TIME_SENSITIVE = True

    def update(self, pbar):
        """Updates the widget to show the ETA or total time when finished."""
        if pbar.currval == 0:
            return 'ETA:  --:--:--'
        if pbar.finished:
            return 'Time: %s' % self.format_time(pbar.seconds_elapsed)
        elapsed = pbar.seconds_elapsed
        eta = elapsed * pbar.maxval / pbar.currval - elapsed
        return 'ETA:  %s' % self.format_time(eta)


class AdaptiveETA(Timer):
    __doc__ = 'Widget which attempts to estimate the time of arrival.\n\n    Uses a weighted average of two estimates:\n      1) ETA based on the total progress and time elapsed so far\n      2) ETA based on the progress as per the last 10 update reports\n\n    The weight depends on the current progress so that to begin with the\n    total progress is used and at the end only the most recent progress is\n    used.\n    '
    TIME_SENSITIVE = True
    NUM_SAMPLES = 10

    def _update_samples(self, currval, elapsed):
        sample = (
         currval, elapsed)
        if not hasattr(self, 'samples'):
            self.samples = [
             sample] * (self.NUM_SAMPLES + 1)
        else:
            self.samples.append(sample)
        return self.samples.pop(0)

    def _eta(self, maxval, currval, elapsed):
        return elapsed * maxval / float(currval) - elapsed

    def update(self, pbar):
        """Updates the widget to show the ETA or total time when finished."""
        if pbar.currval == 0:
            return 'ETA:  --:--:--'
        if pbar.finished:
            return 'Time: %s' % self.format_time(pbar.seconds_elapsed)
        elapsed = pbar.seconds_elapsed
        currval1, elapsed1 = self._update_samples(pbar.currval, elapsed)
        eta = self._eta(pbar.maxval, pbar.currval, elapsed)
        if pbar.currval > currval1:
            etasamp = self._eta(pbar.maxval - currval1, pbar.currval - currval1, elapsed - elapsed1)
            weight = (pbar.currval / float(pbar.maxval)) ** 0.5
            eta = (1 - weight) * eta + weight * etasamp
        return 'ETA:  %s' % self.format_time(eta)


class FileTransferSpeed(Widget):
    __doc__ = 'Widget for showing the transfer speed (useful for file transfers).'
    FORMAT = '%6.2f %s%s/s'
    PREFIXES = ' kMGTPEZY'
    __slots__ = ('unit', )

    def __init__(self, unit='B'):
        self.unit = unit

    def update(self, pbar):
        """Updates the widget with the current SI prefixed speed."""
        if pbar.seconds_elapsed < 2e-06 or pbar.currval < 2e-06:
            scaled = power = 0
        else:
            speed = pbar.currval / pbar.seconds_elapsed
            power = int(math.log(speed, 1000))
            scaled = speed / 1000.0 ** power
        return self.FORMAT % (scaled, self.PREFIXES[power], self.unit)


class AnimatedMarker(Widget):
    __doc__ = 'An animated marker for the progress bar which defaults to appear as if\n    it were rotating.\n    '
    __slots__ = ('markers', 'curmark')

    def __init__(self, markers='|/-\\'):
        self.markers = markers
        self.curmark = -1

    def update(self, pbar):
        """Updates the widget to show the next marker or the first marker when
        finished"""
        if pbar.finished:
            return self.markers[0]
        self.curmark = (self.curmark + 1) % len(self.markers)
        return self.markers[self.curmark]


RotatingMarker = AnimatedMarker

class Counter(Widget):
    __doc__ = 'Displays the current count.'
    __slots__ = ('format_string', )

    def __init__(self, format='%d'):
        self.format_string = format

    def update(self, pbar):
        return self.format_string % pbar.currval


class Percentage(Widget):
    __doc__ = 'Displays the current percentage as a number with a percent sign.'

    def update(self, pbar):
        return '%3d%%' % pbar.percentage()


class FormatLabel(Timer):
    __doc__ = 'Displays a formatted label.'
    mapping = {'elapsed':(
      'seconds_elapsed', Timer.format_time), 
     'finished':('finished', None), 
     'last_update':('last_update_time', None), 
     'max':('maxval', None), 
     'seconds':('seconds_elapsed', None), 
     'start':('start_time', None), 
     'value':('currval', None)}
    __slots__ = ('format_string', )

    def __init__(self, format):
        self.format_string = format

    def update(self, pbar):
        context = {}
        for name, (key, transform) in self.mapping.items():
            try:
                value = getattr(pbar, key)
                if transform is None:
                    context[name] = value
                else:
                    context[name] = transform(value)
            except:
                pass

        return self.format_string % context


class SimpleProgress(Widget):
    __doc__ = 'Returns progress as a count of the total (e.g.: "5 of 47").'
    __slots__ = ('sep', )

    def __init__(self, sep=' of '):
        self.sep = sep

    def update(self, pbar):
        return '%d%s%d' % (pbar.currval, self.sep, pbar.maxval)


class Bar(WidgetHFill):
    __doc__ = 'A progress bar which stretches to fill the line.'
    __slots__ = ('marker', 'left', 'right', 'fill', 'fill_left')

    def __init__(self, marker='#', left='|', right='|', fill=' ', fill_left=True):
        """Creates a customizable progress bar.

        marker - string or updatable object to use as a marker
        left - string or updatable object to use as a left border
        right - string or updatable object to use as a right border
        fill - character to use for the empty part of the progress bar
        fill_left - whether to fill from the left or the right
        """
        self.marker = marker
        self.left = left
        self.right = right
        self.fill = fill
        self.fill_left = fill_left

    def update(self, pbar, width):
        """Updates the progress bar and its subcomponents."""
        left, marked, right = (format_updatable(i, pbar) for i in (
         self.left, self.marker, self.right))
        width -= len(left) + len(right)
        if pbar.maxval:
            marked *= int(pbar.currval / pbar.maxval * width)
        else:
            marked = ''
        if self.fill_left:
            return '%s%s%s' % (left, marked.ljust(width, self.fill), right)
        return '%s%s%s' % (left, marked.rjust(width, self.fill), right)


class ReverseBar(Bar):
    __doc__ = 'A bar which has a marker which bounces from side to side.'

    def __init__(self, marker='#', left='|', right='|', fill=' ', fill_left=False):
        """Creates a customizable progress bar.

        marker - string or updatable object to use as a marker
        left - string or updatable object to use as a left border
        right - string or updatable object to use as a right border
        fill - character to use for the empty part of the progress bar
        fill_left - whether to fill from the left or the right
        """
        self.marker = marker
        self.left = left
        self.right = right
        self.fill = fill
        self.fill_left = fill_left


class BouncingBar(Bar):

    def update(self, pbar, width):
        """Updates the progress bar and its subcomponents."""
        left, marker, right = (format_updatable(i, pbar) for i in (
         self.left, self.marker, self.right))
        width -= len(left) + len(right)
        if pbar.finished:
            return '%s%s%s' % (left, width * marker, right)
        position = int(pbar.currval % (width * 2 - 1))
        if position > width:
            position = width * 2 - position
        lpad = self.fill * (position - 1)
        rpad = self.fill * (width - len(marker) - len(lpad))
        if not self.fill_left:
            rpad, lpad = lpad, rpad
        return '%s%s%s%s%s' % (left, lpad, marker, rpad, right)
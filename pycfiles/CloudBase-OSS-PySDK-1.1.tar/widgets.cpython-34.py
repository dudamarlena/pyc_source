# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/chibiegg/.pyenv/versions/cloudbackup/lib/python3.4/site-packages/cloudbackup/progressbar/widgets.py
# Compiled at: 2014-12-28 14:20:28
# Size of source mod 2**32: 11763 bytes
__doc__ = 'Default ProgressBar widgets.'
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
    else:
        return updatable


class Widget(AbstractWidget):
    """Widget"""
    TIME_SENSITIVE = False
    __slots__ = ()

    @abstractmethod
    def update(self, pbar):
        """Updates the widget.

        pbar - a reference to the calling ProgressBar
        """
        pass


class WidgetHFill(Widget):
    """WidgetHFill"""

    @abstractmethod
    def update(self, pbar, width):
        """Updates the widget providing the total width the widget must fill.

        pbar - a reference to the calling ProgressBar
        width - The total width the widget must fill
        """
        pass


class Timer(Widget):
    """Timer"""
    __slots__ = ('format_string', )
    TIME_SENSITIVE = True

    def __init__(self, format='Elapsed Time: %s'):
        self.format_string = format

    @staticmethod
    def format_time(seconds):
        """Formats time as the string "HH:MM:SS"."""
        return str(datetime.timedelta(seconds=int(seconds)))

    def update(self, pbar):
        """Updates the widget to show the elapsed time."""
        return self.format_string % self.format_time(pbar.seconds_elapsed)


class ETA(Timer):
    """ETA"""
    TIME_SENSITIVE = True

    def update(self, pbar):
        """Updates the widget to show the ETA or total time when finished."""
        if pbar.currval == 0:
            return 'ETA:  --:--:--'
        else:
            if pbar.finished:
                return 'Time: %s' % self.format_time(pbar.seconds_elapsed)
            elapsed = pbar.seconds_elapsed
            eta = elapsed * pbar.maxval / pbar.currval - elapsed
            return 'ETA:  %s' % self.format_time(eta)


class AdaptiveETA(Timer):
    """AdaptiveETA"""
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
        else:
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
    """FileTransferSpeed"""
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


class FileTransferSize(Widget):
    """FileTransferSize"""
    FORMAT = '%6.2f %s%s'
    PREFIXES = ' kMGTPEZY'
    __slots__ = ('unit', )

    def __init__(self, unit='B'):
        self.unit = unit

    def update(self, pbar):
        """Updates the widget with the current SI prefixed speed."""
        size = pbar.currval
        if size > 0:
            power = int(math.log(size, 1000))
        else:
            power = 1
        scaled = size / 1000.0 ** power
        return self.FORMAT % (scaled, self.PREFIXES[power], self.unit)


class AnimatedMarker(Widget):
    """AnimatedMarker"""
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
    """Counter"""
    __slots__ = ('format_string', )

    def __init__(self, format='%d'):
        self.format_string = format

    def update(self, pbar):
        return self.format_string % pbar.currval


class Percentage(Widget):
    """Percentage"""

    def update(self, pbar):
        return '%3d%%' % pbar.percentage()


class FormatLabel(Timer):
    """FormatLabel"""
    mapping = {'elapsed': (
                 'seconds_elapsed', Timer.format_time), 
     'finished': ('finished', None), 
     'last_update': ('last_update_time', None), 
     'max': ('maxval', None), 
     'seconds': ('seconds_elapsed', None), 
     'start': ('start_time', None), 
     'value': ('currval', None)}
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
    """SimpleProgress"""
    __slots__ = ('sep', )

    def __init__(self, sep=' of '):
        self.sep = sep

    def update(self, pbar):
        return '%d%s%d' % (pbar.currval, self.sep, pbar.maxval)


class Bar(WidgetHFill):
    """Bar"""
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
        else:
            return '%s%s%s' % (left, marked.rjust(width, self.fill), right)


class ReverseBar(Bar):
    """ReverseBar"""

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
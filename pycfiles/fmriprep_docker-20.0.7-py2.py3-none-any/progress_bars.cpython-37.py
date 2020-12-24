# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/cli/progress_bars.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 9031 bytes
from __future__ import division
import itertools, sys
from signal import SIGINT, default_int_handler, signal
from pip._vendor import six
from pip._vendor.progress.bar import Bar, FillingCirclesBar, IncrementalBar
from pip._vendor.progress.spinner import Spinner
from pip._internal.utils.compat import WINDOWS
from pip._internal.utils.logging import get_indentation
from pip._internal.utils.misc import format_size
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Any, Dict, List
try:
    from pip._vendor import colorama
except Exception:
    colorama = None

def _select_progress_class(preferred, fallback):
    encoding = getattr(preferred.file, 'encoding', None)
    if not encoding:
        return fallback
    characters = [
     getattr(preferred, 'empty_fill', six.text_type()),
     getattr(preferred, 'fill', six.text_type())]
    characters += list(getattr(preferred, 'phases', []))
    try:
        six.text_type().join(characters).encode(encoding)
    except UnicodeEncodeError:
        return fallback
    else:
        return preferred


_BaseBar = _select_progress_class(IncrementalBar, Bar)

class InterruptibleMixin(object):
    __doc__ = "\n    Helper to ensure that self.finish() gets called on keyboard interrupt.\n\n    This allows downloads to be interrupted without leaving temporary state\n    (like hidden cursors) behind.\n\n    This class is similar to the progress library's existing SigIntMixin\n    helper, but as of version 1.2, that helper has the following problems:\n\n    1. It calls sys.exit().\n    2. It discards the existing SIGINT handler completely.\n    3. It leaves its own handler in place even after an uninterrupted finish,\n       which will have unexpected delayed effects if the user triggers an\n       unrelated keyboard interrupt some time after a progress-displaying\n       download has already completed, for example.\n    "

    def __init__(self, *args, **kwargs):
        (super(InterruptibleMixin, self).__init__)(*args, **kwargs)
        self.original_handler = signal(SIGINT, self.handle_sigint)
        if self.original_handler is None:
            self.original_handler = default_int_handler

    def finish(self):
        super(InterruptibleMixin, self).finish()
        signal(SIGINT, self.original_handler)

    def handle_sigint(self, signum, frame):
        """
        Call self.finish() before delegating to the original SIGINT handler.

        This handler should only be in place while the progress display is
        active.
        """
        self.finish()
        self.original_handler(signum, frame)


class SilentBar(Bar):

    def update(self):
        pass


class BlueEmojiBar(IncrementalBar):
    suffix = '%(percent)d%%'
    bar_prefix = ' '
    bar_suffix = ' '
    phases = ('🔹', '🔷', '🔵')


class DownloadProgressMixin(object):

    def __init__(self, *args, **kwargs):
        (super(DownloadProgressMixin, self).__init__)(*args, **kwargs)
        self.message = ' ' * (get_indentation() + 2) + self.message

    @property
    def downloaded(self):
        return format_size(self.index)

    @property
    def download_speed(self):
        if self.avg == 0.0:
            return '...'
        return format_size(1 / self.avg) + '/s'

    @property
    def pretty_eta(self):
        if self.eta:
            return 'eta {}'.format(self.eta_td)
        return ''

    def iter(self, it):
        for x in it:
            yield x
            self.next(len(x))

        self.finish()


class WindowsMixin(object):

    def __init__(self, *args, **kwargs):
        if WINDOWS:
            if self.hide_cursor:
                self.hide_cursor = False
        (super(WindowsMixin, self).__init__)(*args, **kwargs)
        if WINDOWS:
            if colorama:
                self.file = colorama.AnsiToWin32(self.file)
                self.file.isatty = lambda : self.file.wrapped.isatty()
                self.file.flush = lambda : self.file.wrapped.flush()


class BaseDownloadProgressBar(WindowsMixin, InterruptibleMixin, DownloadProgressMixin):
    file = sys.stdout
    message = '%(percent)d%%'
    suffix = '%(downloaded)s %(download_speed)s %(pretty_eta)s'


class DefaultDownloadProgressBar(BaseDownloadProgressBar, _BaseBar):
    pass


class DownloadSilentBar(BaseDownloadProgressBar, SilentBar):
    pass


class DownloadBar(BaseDownloadProgressBar, Bar):
    pass


class DownloadFillingCirclesBar(BaseDownloadProgressBar, FillingCirclesBar):
    pass


class DownloadBlueEmojiProgressBar(BaseDownloadProgressBar, BlueEmojiBar):
    pass


class DownloadProgressSpinner(WindowsMixin, InterruptibleMixin, DownloadProgressMixin, Spinner):
    file = sys.stdout
    suffix = '%(downloaded)s %(download_speed)s'

    def next_phase(self):
        if not hasattr(self, '_phaser'):
            self._phaser = itertools.cycle(self.phases)
        return next(self._phaser)

    def update(self):
        message = self.message % self
        phase = self.next_phase()
        suffix = self.suffix % self
        line = ''.join([
         message,
         ' ' if message else '',
         phase,
         ' ' if suffix else '',
         suffix])
        self.writeln(line)


BAR_TYPES = {'off':(
  DownloadSilentBar, DownloadSilentBar), 
 'on':(
  DefaultDownloadProgressBar, DownloadProgressSpinner), 
 'ascii':(
  DownloadBar, DownloadProgressSpinner), 
 'pretty':(
  DownloadFillingCirclesBar, DownloadProgressSpinner), 
 'emoji':(
  DownloadBlueEmojiProgressBar, DownloadProgressSpinner)}

def DownloadProgressProvider(progress_bar, max=None):
    if max is None or max == 0:
        return BAR_TYPES[progress_bar][1]().iter
    return BAR_TYPES[progress_bar][0](max=max).iter
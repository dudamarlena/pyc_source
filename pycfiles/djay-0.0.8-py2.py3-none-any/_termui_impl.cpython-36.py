# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/click/click/_termui_impl.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 19611 bytes
"""
click._termui_impl
~~~~~~~~~~~~~~~~~~

This module contains implementations for the termui module. To keep the
import time of Click down, some infrequently used functionality is
placed in this module and only imported as needed.

:copyright: © 2014 by the Pallets team.
:license: BSD, see LICENSE.rst for more details.
"""
import os, sys, time, math, contextlib
from ._compat import _default_text_stdout, range_type, PY2, isatty, open_stream, strip_ansi, term_len, get_best_encoding, WIN, int_types, CYGWIN
from .utils import echo
from .exceptions import ClickException
if os.name == 'nt':
    BEFORE_BAR = '\r'
    AFTER_BAR = '\n'
else:
    BEFORE_BAR = '\r\x1b[?25l'
    AFTER_BAR = '\x1b[?25h\n'

def _length_hint(obj):
    """Returns the length hint of an object."""
    try:
        return len(obj)
    except (AttributeError, TypeError):
        try:
            get_hint = type(obj).__length_hint__
        except AttributeError:
            return
        else:
            try:
                hint = get_hint(obj)
            except TypeError:
                return
            else:
                if hint is NotImplemented or not isinstance(hint, int_types) or hint < 0:
                    return
        return hint


class ProgressBar(object):

    def __init__(self, iterable, length=None, fill_char='#', empty_char=' ', bar_template='%(bar)s', info_sep='  ', show_eta=True, show_percent=None, show_pos=False, item_show_func=None, label=None, file=None, color=None, width=30):
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.bar_template = bar_template
        self.info_sep = info_sep
        self.show_eta = show_eta
        self.show_percent = show_percent
        self.show_pos = show_pos
        self.item_show_func = item_show_func
        self.label = label or ''
        if file is None:
            file = _default_text_stdout()
        self.file = file
        self.color = color
        self.width = width
        self.autowidth = width == 0
        if length is None:
            length = _length_hint(iterable)
        if iterable is None:
            if length is None:
                raise TypeError('iterable or length is required')
            iterable = range_type(length)
        self.iter = iter(iterable)
        self.length = length
        self.length_known = length is not None
        self.pos = 0
        self.avg = []
        self.start = self.last_eta = time.time()
        self.eta_known = False
        self.finished = False
        self.max_width = None
        self.entered = False
        self.current_item = None
        self.is_hidden = not isatty(self.file)
        self._last_line = None
        self.short_limit = 0.5

    def __enter__(self):
        self.entered = True
        self.render_progress()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.render_finish()

    def __iter__(self):
        if not self.entered:
            raise RuntimeError('You need to use progress bars in a with block.')
        self.render_progress()
        return self.generator()

    def is_fast(self):
        return time.time() - self.start <= self.short_limit

    def render_finish(self):
        if self.is_hidden or self.is_fast():
            return
        self.file.write(AFTER_BAR)
        self.file.flush()

    @property
    def pct(self):
        if self.finished:
            return 1.0
        else:
            return min(self.pos / (float(self.length) or 1), 1.0)

    @property
    def time_per_iteration(self):
        if not self.avg:
            return 0.0
        else:
            return sum(self.avg) / float(len(self.avg))

    @property
    def eta(self):
        if self.length_known:
            if not self.finished:
                return self.time_per_iteration * (self.length - self.pos)
        return 0.0

    def format_eta(self):
        if self.eta_known:
            t = int(self.eta)
            seconds = t % 60
            t //= 60
            minutes = t % 60
            t //= 60
            hours = t % 24
            t //= 24
            if t > 0:
                days = t
                return '%dd %02d:%02d:%02d' % (days, hours, minutes, seconds)
            return '%02d:%02d:%02d' % (hours, minutes, seconds)
        else:
            return ''

    def format_pos(self):
        pos = str(self.pos)
        if self.length_known:
            pos += '/%s' % self.length
        return pos

    def format_pct(self):
        return ('% 4d%%' % int(self.pct * 100))[1:]

    def format_bar(self):
        if self.length_known:
            bar_length = int(self.pct * self.width)
            bar = self.fill_char * bar_length
            bar += self.empty_char * (self.width - bar_length)
        else:
            if self.finished:
                bar = self.fill_char * self.width
            else:
                bar = list(self.empty_char * (self.width or 1))
                if self.time_per_iteration != 0:
                    bar[int((math.cos(self.pos * self.time_per_iteration) / 2.0 + 0.5) * self.width)] = self.fill_char
                bar = ''.join(bar)
        return bar

    def format_progress_line(self):
        show_percent = self.show_percent
        info_bits = []
        if self.length_known:
            if show_percent is None:
                show_percent = not self.show_pos
        if self.show_pos:
            info_bits.append(self.format_pos())
        if show_percent:
            info_bits.append(self.format_pct())
        if self.show_eta:
            if self.eta_known:
                if not self.finished:
                    info_bits.append(self.format_eta())
        if self.item_show_func is not None:
            item_info = self.item_show_func(self.current_item)
            if item_info is not None:
                info_bits.append(item_info)
        return (self.bar_template % {'label':self.label, 
         'bar':self.format_bar(), 
         'info':self.info_sep.join(info_bits)}).rstrip()

    def render_progress(self):
        from .termui import get_terminal_size
        if self.is_hidden:
            return
        buf = []
        if self.autowidth:
            old_width = self.width
            self.width = 0
            clutter_length = term_len(self.format_progress_line())
            new_width = max(0, get_terminal_size()[0] - clutter_length)
            if new_width < old_width:
                buf.append(BEFORE_BAR)
                buf.append(' ' * self.max_width)
                self.max_width = new_width
            self.width = new_width
        clear_width = self.width
        if self.max_width is not None:
            clear_width = self.max_width
        buf.append(BEFORE_BAR)
        line = self.format_progress_line()
        line_len = term_len(line)
        if self.max_width is None or self.max_width < line_len:
            self.max_width = line_len
        buf.append(line)
        buf.append(' ' * (clear_width - line_len))
        line = ''.join(buf)
        if line != self._last_line and not self.is_fast():
            self._last_line = line
            echo(line, file=(self.file), color=(self.color), nl=False)
            self.file.flush()

    def make_step(self, n_steps):
        self.pos += n_steps
        if self.length_known:
            if self.pos >= self.length:
                self.finished = True
        else:
            if time.time() - self.last_eta < 1.0:
                return
            self.last_eta = time.time()
            if self.pos:
                step = (time.time() - self.start) / self.pos
            else:
                step = time.time() - self.start
        self.avg = self.avg[-6:] + [step]
        self.eta_known = self.length_known

    def update(self, n_steps):
        self.make_step(n_steps)
        self.render_progress()

    def finish(self):
        self.eta_known = 0
        self.current_item = None
        self.finished = True

    def generator(self):
        """
        Returns a generator which yields the items added to the bar during
        construction, and updates the progress bar *after* the yielded block
        returns.
        """
        if not self.entered:
            raise RuntimeError('You need to use progress bars in a with block.')
        else:
            if self.is_hidden:
                for rv in self.iter:
                    yield rv

            else:
                for rv in self.iter:
                    self.current_item = rv
                    yield rv
                    self.update(1)

                self.finish()
                self.render_progress()


def pager(generator, color=None):
    """Decide what method to use for paging through text."""
    stdout = _default_text_stdout()
    if not isatty(sys.stdin) or not isatty(stdout):
        return _nullpager(stdout, generator, color)
    pager_cmd = (os.environ.get('PAGER', None) or '').strip()
    if pager_cmd:
        if WIN:
            return _tempfilepager(generator, pager_cmd, color)
        else:
            return _pipepager(generator, pager_cmd, color)
    if os.environ.get('TERM') in ('dumb', 'emacs'):
        return _nullpager(stdout, generator, color)
    if WIN or sys.platform.startswith('os2'):
        return _tempfilepager(generator, 'more <', color)
    if hasattr(os, 'system'):
        if os.system('(less) 2>/dev/null') == 0:
            return _pipepager(generator, 'less', color)
    import tempfile
    fd, filename = tempfile.mkstemp()
    os.close(fd)
    try:
        if hasattr(os, 'system') and os.system('more "%s"' % filename) == 0:
            return _pipepager(generator, 'more', color)
        return _nullpager(stdout, generator, color)
    finally:
        os.unlink(filename)


def _pipepager(generator, cmd, color):
    """Page through text by feeding it to another program.  Invoking a
    pager through this might support colors.
    """
    import subprocess
    env = dict(os.environ)
    cmd_detail = cmd.rsplit('/', 1)[(-1)].split()
    if color is None:
        if cmd_detail[0] == 'less':
            less_flags = os.environ.get('LESS', '') + ' '.join(cmd_detail[1:])
            env['LESS'] = less_flags or '-R'
            color = True
        elif 'r' in less_flags or 'R' in less_flags:
            color = True
    c = subprocess.Popen(cmd, shell=True, stdin=(subprocess.PIPE), env=env)
    encoding = get_best_encoding(c.stdin)
    try:
        for text in generator:
            if not color:
                text = strip_ansi(text)
            c.stdin.write(text.encode(encoding, 'replace'))

    except (IOError, KeyboardInterrupt):
        pass
    else:
        c.stdin.close()
    while True:
        try:
            c.wait()
        except KeyboardInterrupt:
            pass
        else:
            break


def _tempfilepager(generator, cmd, color):
    """Page through text by invoking a program on a temporary file."""
    import tempfile
    filename = tempfile.mktemp()
    text = ''.join(generator)
    if not color:
        text = strip_ansi(text)
    encoding = get_best_encoding(sys.stdout)
    with open_stream(filename, 'wb')[0] as (f):
        f.write(text.encode(encoding))
    try:
        os.system(cmd + ' "' + filename + '"')
    finally:
        os.unlink(filename)


def _nullpager(stream, generator, color):
    """Simply print unformatted text.  This is the ultimate fallback."""
    for text in generator:
        if not color:
            text = strip_ansi(text)
        stream.write(text)


class Editor(object):

    def __init__(self, editor=None, env=None, require_save=True, extension='.txt'):
        self.editor = editor
        self.env = env
        self.require_save = require_save
        self.extension = extension

    def get_editor(self):
        if self.editor is not None:
            return self.editor
        else:
            for key in ('VISUAL', 'EDITOR'):
                rv = os.environ.get(key)
                if rv:
                    return rv

            if WIN:
                return 'notepad'
            for editor in ('vim', 'nano'):
                if os.system('which %s >/dev/null 2>&1' % editor) == 0:
                    return editor

            return 'vi'

    def edit_file(self, filename):
        import subprocess
        editor = self.get_editor()
        if self.env:
            environ = os.environ.copy()
            environ.update(self.env)
        else:
            environ = None
        try:
            c = subprocess.Popen(('%s "%s"' % (editor, filename)), env=environ,
              shell=True)
            exit_code = c.wait()
            if exit_code != 0:
                raise ClickException('%s: Editing failed!' % editor)
        except OSError as e:
            raise ClickException('%s: Editing failed: %s' % (editor, e))

    def edit(self, text):
        import tempfile
        text = text or ''
        if text:
            if not text.endswith('\n'):
                text += '\n'
        fd, name = tempfile.mkstemp(prefix='editor-', suffix=(self.extension))
        try:
            if WIN:
                encoding = 'utf-8-sig'
                text = text.replace('\n', '\r\n')
            else:
                encoding = 'utf-8'
            text = text.encode(encoding)
            f = os.fdopen(fd, 'wb')
            f.write(text)
            f.close()
            timestamp = os.path.getmtime(name)
            self.edit_file(name)
            if self.require_save:
                if os.path.getmtime(name) == timestamp:
                    return
            f = open(name, 'rb')
            try:
                rv = f.read()
            finally:
                f.close()

            return rv.decode('utf-8-sig').replace('\r\n', '\n')
        finally:
            os.unlink(name)


def open_url(url, wait=False, locate=False):
    import subprocess

    def _unquote_file(url):
        try:
            import urllib
        except ImportError:
            import urllib

        if url.startswith('file://'):
            url = urllib.unquote(url[7:])
        return url

    if sys.platform == 'darwin':
        args = [
         'open']
        if wait:
            args.append('-W')
        if locate:
            args.append('-R')
        args.append(_unquote_file(url))
        null = open('/dev/null', 'w')
        try:
            return subprocess.Popen(args, stderr=null).wait()
        finally:
            null.close()

    else:
        if WIN:
            if locate:
                url = _unquote_file(url)
                args = 'explorer /select,"%s"' % _unquote_file(url.replace('"', ''))
            else:
                args = 'start %s "" "%s"' % (
                 wait and '/WAIT' or '', url.replace('"', ''))
            return os.system(args)
        if CYGWIN:
            if locate:
                url = _unquote_file(url)
                args = 'cygstart "%s"' % os.path.dirname(url).replace('"', '')
            else:
                args = 'cygstart %s "%s"' % (
                 wait and '-w' or '', url.replace('"', ''))
            return os.system(args)
        try:
            if locate:
                url = os.path.dirname(_unquote_file(url)) or '.'
            else:
                url = _unquote_file(url)
            c = subprocess.Popen(['xdg-open', url])
            if wait:
                return c.wait()
            return 0
        except OSError:
            if url.startswith(('http://', 'https://')):
                if not locate:
                    if not wait:
                        import webbrowser
                        webbrowser.open(url)
                        return 0
            return 1


def _translate_ch_to_exc(ch):
    if ch == '\x03':
        raise KeyboardInterrupt()
    else:
        if ch == '\x04':
            if not WIN:
                raise EOFError()
        if ch == '\x1a':
            if WIN:
                raise EOFError()


if WIN:
    import msvcrt

    @contextlib.contextmanager
    def raw_terminal():
        yield


    def getchar(echo):
        if echo:
            func = msvcrt.getwche
        else:
            func = msvcrt.getwch
        rv = func()
        if rv in ('\x00', 'à'):
            rv += func()
        _translate_ch_to_exc(rv)
        return rv


else:
    import tty, termios

    @contextlib.contextmanager
    def raw_terminal():
        if not isatty(sys.stdin):
            f = open('/dev/tty')
            fd = f.fileno()
        else:
            fd = sys.stdin.fileno()
            f = None
        try:
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                yield fd
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                sys.stdout.flush()
                if f is not None:
                    f.close()

        except termios.error:
            pass


    def getchar(echo):
        with raw_terminal() as (fd):
            ch = os.read(fd, 32)
            ch = ch.decode(get_best_encoding(sys.stdin), 'replace')
            if echo:
                if isatty(sys.stdout):
                    sys.stdout.write(ch)
            _translate_ch_to_exc(ch)
            return ch
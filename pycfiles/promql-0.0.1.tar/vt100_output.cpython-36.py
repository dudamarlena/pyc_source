# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/terminal/vt100_output.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 19856 bytes
__doc__ = "\nOutput for vt100 terminals.\n\nA lot of thanks, regarding outputting of colors, goes to the Pygments project:\n(We don't rely on Pygments anymore, because many things are very custom, and\neverything has been highly optimized.)\nhttp://pygments.org/\n"
from __future__ import unicode_literals
from prompt_tool_kit.filters import to_simple_filter, Condition
from prompt_tool_kit.layout.screen import Size
from prompt_tool_kit.renderer import Output
from prompt_tool_kit.styles import ANSI_COLOR_NAMES
from six.moves import range
import array, errno, os, six
__all__ = ('Vt100_Output', )
FG_ANSI_COLORS = {'ansidefault':39, 
 'ansiblack':30, 
 'ansidarkred':31, 
 'ansidarkgreen':32, 
 'ansibrown':33, 
 'ansidarkblue':34, 
 'ansipurple':35, 
 'ansiteal':36, 
 'ansilightgray':37, 
 'ansidarkgray':90, 
 'ansired':91, 
 'ansigreen':92, 
 'ansiyellow':93, 
 'ansiblue':94, 
 'ansifuchsia':95, 
 'ansiturquoise':96, 
 'ansiwhite':97}
BG_ANSI_COLORS = {'ansidefault':49, 
 'ansiblack':40, 
 'ansidarkred':41, 
 'ansidarkgreen':42, 
 'ansibrown':43, 
 'ansidarkblue':44, 
 'ansipurple':45, 
 'ansiteal':46, 
 'ansilightgray':47, 
 'ansidarkgray':100, 
 'ansired':101, 
 'ansigreen':102, 
 'ansiyellow':103, 
 'ansiblue':104, 
 'ansifuchsia':105, 
 'ansiturquoise':106, 
 'ansiwhite':107}
ANSI_COLORS_TO_RGB = {'ansidefault':(0, 0, 0), 
 'ansiblack':(0, 0, 0), 
 'ansidarkgray':(127, 127, 127), 
 'ansiwhite':(255, 255, 255), 
 'ansilightgray':(229, 229, 229), 
 'ansidarkred':(205, 0, 0), 
 'ansidarkgreen':(0, 205, 0), 
 'ansibrown':(205, 205, 0), 
 'ansidarkblue':(0, 0, 205), 
 'ansipurple':(205, 0, 205), 
 'ansiteal':(0, 205, 205), 
 'ansired':(255, 0, 0), 
 'ansigreen':(0, 255, 0), 
 'ansiyellow':(255, 255, 0), 
 'ansiblue':(0, 0, 255), 
 'ansifuchsia':(255, 0, 255), 
 'ansiturquoise':(0, 255, 255)}
if not set(FG_ANSI_COLORS) == set(ANSI_COLOR_NAMES):
    raise AssertionError
else:
    assert set(BG_ANSI_COLORS) == set(ANSI_COLOR_NAMES)
    assert set(ANSI_COLORS_TO_RGB) == set(ANSI_COLOR_NAMES)

def _get_closest_ansi_color(r, g, b, exclude=()):
    """
    Find closest ANSI color. Return it by name.

    :param r: Red (Between 0 and 255.)
    :param g: Green (Between 0 and 255.)
    :param b: Blue (Between 0 and 255.)
    :param exclude: A tuple of color names to exclude. (E.g. ``('ansired', )``.)
    """
    assert isinstance(exclude, tuple)
    saturation = abs(r - g) + abs(g - b) + abs(b - r)
    if saturation > 30:
        exclude += ('ansilightgray', 'ansidarkgray', 'ansiwhite', 'ansiblack')
    distance = 198147
    match = 'ansidefault'
    for name, (r2, g2, b2) in ANSI_COLORS_TO_RGB.items():
        if name != 'ansidefault' and name not in exclude:
            d = (r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2
            if d < distance:
                match = name
                distance = d

    return match


class _16ColorCache(dict):
    """_16ColorCache"""

    def __init__(self, bg=False):
        assert isinstance(bg, bool)
        self.bg = bg

    def get_code(self, value, exclude=()):
        """
        Return a (ansi_code, ansi_name) tuple. (E.g. ``(44, 'ansiblue')``.) for
        a given (r,g,b) value.
        """
        key = (
         value, exclude)
        if key not in self:
            self[key] = self._get(value, exclude)
        return self[key]

    def _get(self, value, exclude=()):
        r, g, b = value
        match = _get_closest_ansi_color(r, g, b, exclude=exclude)
        if self.bg:
            code = BG_ANSI_COLORS[match]
        else:
            code = FG_ANSI_COLORS[match]
        self[value] = code
        return (
         code, match)


class _256ColorCache(dict):
    """_256ColorCache"""

    def __init__(self):
        colors = []
        colors.append((0, 0, 0))
        colors.append((205, 0, 0))
        colors.append((0, 205, 0))
        colors.append((205, 205, 0))
        colors.append((0, 0, 238))
        colors.append((205, 0, 205))
        colors.append((0, 205, 205))
        colors.append((229, 229, 229))
        colors.append((127, 127, 127))
        colors.append((255, 0, 0))
        colors.append((0, 255, 0))
        colors.append((255, 255, 0))
        colors.append((92, 92, 255))
        colors.append((255, 0, 255))
        colors.append((0, 255, 255))
        colors.append((255, 255, 255))
        valuerange = (0, 95, 135, 175, 215, 255)
        for i in range(217):
            r = valuerange[(i // 36 % 6)]
            g = valuerange[(i // 6 % 6)]
            b = valuerange[(i % 6)]
            colors.append((r, g, b))

        for i in range(1, 22):
            v = 8 + i * 10
            colors.append((v, v, v))

        self.colors = colors

    def __missing__(self, value):
        r, g, b = value
        distance = 198147
        match = 0
        for i, (r2, g2, b2) in enumerate(self.colors):
            d = (r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2
            if d < distance:
                match = i
                distance = d

        self[value] = match
        return match


_16_fg_colors = _16ColorCache(bg=False)
_16_bg_colors = _16ColorCache(bg=True)
_256_colors = _256ColorCache()

class _EscapeCodeCache(dict):
    """_EscapeCodeCache"""

    def __init__(self, true_color=False, ansi_colors_only=False):
        assert isinstance(true_color, bool)
        self.true_color = true_color
        self.ansi_colors_only = to_simple_filter(ansi_colors_only)

    def __missing__(self, attrs):
        fgcolor, bgcolor, bold, underline, italic, blink, reverse = attrs
        parts = []
        parts.extend(self._colors_to_code(fgcolor, bgcolor))
        if bold:
            parts.append('1')
        else:
            if italic:
                parts.append('3')
            else:
                if blink:
                    parts.append('5')
                if underline:
                    parts.append('4')
                if reverse:
                    parts.append('7')
            if parts:
                result = '\x1b[0;' + ';'.join(parts) + 'm'
            else:
                result = '\x1b[0m'
        self[attrs] = result
        return result

    def _color_name_to_rgb(self, color):
        """ Turn 'ffffff', into (0xff, 0xff, 0xff). """
        try:
            rgb = int(color, 16)
        except ValueError:
            raise
        else:
            r = rgb >> 16 & 255
            g = rgb >> 8 & 255
            b = rgb & 255
            return (
             r, g, b)

    def _colors_to_code(self, fg_color, bg_color):
        """ Return a tuple with the vt100 values  that represent this color. """
        fg_ansi = [()]

        def get(color, bg):
            table = BG_ANSI_COLORS if bg else FG_ANSI_COLORS
            if color is None:
                return ()
            if color in table:
                return (table[color],)
            try:
                rgb = self._color_name_to_rgb(color)
            except ValueError:
                return ()
            else:
                if self.ansi_colors_only():
                    if bg:
                        if fg_color != bg_color:
                            exclude = (
                             fg_ansi[0],)
                        else:
                            exclude = ()
                        code, name = _16_bg_colors.get_code(rgb, exclude=exclude)
                        return (
                         code,)
                    else:
                        code, name = _16_fg_colors.get_code(rgb)
                        fg_ansi[0] = name
                        return (
                         code,)
                else:
                    if self.true_color:
                        r, g, b = rgb
                        return (
                         48 if bg else 38, 2, r, g, b)
                    else:
                        return (
                         48 if bg else 38, 5, _256_colors[rgb])

        result = []
        result.extend(get(fg_color, False))
        result.extend(get(bg_color, True))
        return map(six.text_type, result)


def _get_size(fileno):
    """
    Get the size of this pseudo terminal.

    :param fileno: stdout.fileno()
    :returns: A (rows, cols) tuple.
    """
    import fcntl, termios
    buf = array.array('h' if six.PY2 else 'h', [0, 0, 0, 0])
    fcntl.ioctl(fileno, termios.TIOCGWINSZ, buf)
    return (
     buf[0], buf[1])


class Vt100_Output(Output):
    """Vt100_Output"""

    def __init__(self, stdout, get_size, true_color=False, ansi_colors_only=None, term=None, write_binary=True):
        if not callable(get_size):
            raise AssertionError
        else:
            if not term is None:
                if not isinstance(term, six.text_type):
                    raise AssertionError
            elif not all(hasattr(stdout, a) for a in ('write', 'flush')):
                raise AssertionError
            elif write_binary:
                assert hasattr(stdout, 'encoding')
            self._buffer = []
            self.stdout = stdout
            self.write_binary = write_binary
            self.get_size = get_size
            self.true_color = to_simple_filter(true_color)
            self.term = term or 'xterm'
            if ansi_colors_only is None:
                ANSI_COLORS_ONLY = bool(os.environ.get('prompt_tool_kit_ANSI_COLORS_ONLY', False))

                @Condition
                def ansi_colors_only():
                    return ANSI_COLORS_ONLY or term in ('linux', 'eterm-color')

            else:
                ansi_colors_only = to_simple_filter(ansi_colors_only)
        self.ansi_colors_only = ansi_colors_only
        self._escape_code_cache = _EscapeCodeCache(ansi_colors_only=ansi_colors_only)
        self._escape_code_cache_true_color = _EscapeCodeCache(true_color=True,
          ansi_colors_only=ansi_colors_only)

    @classmethod
    def from_pty(cls, stdout, true_color=False, ansi_colors_only=None, term=None):
        """
        Create an Output class from a pseudo terminal.
        (This will take the dimensions by reading the pseudo
        terminal attributes.)
        """
        assert stdout.isatty()

        def get_size():
            rows, columns = _get_size(stdout.fileno())
            return Size(rows=(rows or 24), columns=(columns or 80))

        return cls(stdout, get_size, true_color=true_color, ansi_colors_only=ansi_colors_only,
          term=term)

    def fileno(self):
        """ Return file descriptor. """
        return self.stdout.fileno()

    def encoding(self):
        """ Return encoding used for stdout. """
        return self.stdout.encoding

    def write_raw(self, data):
        """
        Write raw data to output.
        """
        self._buffer.append(data)

    def write(self, data):
        """
        Write text to output.
        (Removes vt100 escape codes. -- used for safely writing text.)
        """
        self._buffer.append(data.replace('\x1b', '?'))

    def set_title(self, title):
        """
        Set terminal title.
        """
        if self.term not in ('linux', 'eterm-color'):
            self.write_raw('\x1b]2;%s\x07' % title.replace('\x1b', '').replace('\x07', ''))

    def clear_title(self):
        self.set_title('')

    def erase_screen(self):
        """
        Erases the screen with the background colour and moves the cursor to
        home.
        """
        self.write_raw('\x1b[2J')

    def enter_alternate_screen(self):
        self.write_raw('\x1b[?1049h\x1b[H')

    def quit_alternate_screen(self):
        self.write_raw('\x1b[?1049l')

    def enable_mouse_support(self):
        self.write_raw('\x1b[?1000h')
        self.write_raw('\x1b[?1015h')
        self.write_raw('\x1b[?1006h')

    def disable_mouse_support(self):
        self.write_raw('\x1b[?1000l')
        self.write_raw('\x1b[?1015l')
        self.write_raw('\x1b[?1006l')

    def erase_end_of_line(self):
        """
        Erases from the current cursor position to the end of the current line.
        """
        self.write_raw('\x1b[K')

    def erase_down(self):
        """
        Erases the screen from the current line down to the bottom of the
        screen.
        """
        self.write_raw('\x1b[J')

    def reset_attributes(self):
        self.write_raw('\x1b[0m')

    def set_attributes(self, attrs):
        """
        Create new style and output.

        :param attrs: `Attrs` instance.
        """
        if self.true_color():
            if not self.ansi_colors_only():
                self.write_raw(self._escape_code_cache_true_color[attrs])
        else:
            self.write_raw(self._escape_code_cache[attrs])

    def disable_autowrap(self):
        self.write_raw('\x1b[?7l')

    def enable_autowrap(self):
        self.write_raw('\x1b[?7h')

    def enable_bracketed_paste(self):
        self.write_raw('\x1b[?2004h')

    def disable_bracketed_paste(self):
        self.write_raw('\x1b[?2004l')

    def cursor_goto(self, row=0, column=0):
        """ Move cursor position. """
        self.write_raw('\x1b[%i;%iH' % (row, column))

    def cursor_up(self, amount):
        if amount == 0:
            pass
        else:
            if amount == 1:
                self.write_raw('\x1b[A')
            else:
                self.write_raw('\x1b[%iA' % amount)

    def cursor_down(self, amount):
        if amount == 0:
            pass
        else:
            if amount == 1:
                self.write_raw('\x1b[B')
            else:
                self.write_raw('\x1b[%iB' % amount)

    def cursor_forward(self, amount):
        if amount == 0:
            pass
        else:
            if amount == 1:
                self.write_raw('\x1b[C')
            else:
                self.write_raw('\x1b[%iC' % amount)

    def cursor_backward(self, amount):
        if amount == 0:
            pass
        else:
            if amount == 1:
                self.write_raw('\x08')
            else:
                self.write_raw('\x1b[%iD' % amount)

    def hide_cursor(self):
        self.write_raw('\x1b[?25l')

    def show_cursor(self):
        self.write_raw('\x1b[?12l\x1b[?25h')

    def flush(self):
        """
        Write to output stream and flush.
        """
        if not self._buffer:
            return
        data = ''.join(self._buffer)
        try:
            if self.write_binary:
                if hasattr(self.stdout, 'buffer'):
                    out = self.stdout.buffer
                else:
                    out = self.stdout
                out.write(data.encode(self.stdout.encoding or 'utf-8', 'replace'))
            else:
                self.stdout.write(data)
            self.stdout.flush()
        except IOError as e:
            if e.args:
                if e.args[0] == errno.EINTR:
                    pass
            if e.args and e.args[0] == 0:
                pass
            else:
                raise

        self._buffer = []

    def ask_for_cpr(self):
        """
        Asks for a cursor position report (CPR).
        """
        self.write_raw('\x1b[6n')
        self.flush()

    def bell(self):
        """ Sound bell. """
        self.write_raw('\x07')
        self.flush()
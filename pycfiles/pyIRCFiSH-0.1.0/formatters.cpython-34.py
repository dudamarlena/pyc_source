# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/formatting/formatters.py
# Compiled at: 2015-10-08 05:15:48
# Size of source mod 2**32: 14978 bytes
__doc__ = 'IRC message formatting classes.\n\nThis module contains reformatting classes to handle IRC formatting codes.\n\nBold, italic, underline, reverse, and colours are handled.\n\n'
try:
    from enum import Enum, unique
except ImportError:
    from PyIRC.util.enum import Enum, unique

import os, sys
try:
    import curses
except ImportError:
    curses = None

import re
from PyIRC.formatting.colours import Colours, ColoursRGB, ColoursANSI, ColoursXTerm256

@unique
class FormattingCodes(Enum):
    """FormattingCodes"""
    bold = '\x02'
    colour = '\x03'
    normal = '\x0f'
    reverse = '\x16'
    italic = '\x1d'
    underline = '\x1f'


class Formatter:
    """Formatter"""
    cmatch = re.compile('^([0-9]+)(?:,([0-9]+)?)?')

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all colours.

        You should not need to override this.

        """
        self.bold = False
        self.foreground = None
        self.background = None
        self.reverse = False
        self.italic = False
        self.underline = False

    def format(self, string):
        """Convert a given IRC string.

        Returns the final formatted string.

        Special formatting is done by using callbacks. All callbacks are
        called after the state is updated to reflect the new status, except
        for normal which cannot work in any other way (due to needing to know
        what formatters to reset).

        :param string:
            String to reformat.

        """
        ret = list()
        index = 0
        l = len(string)
        while index < l:
            char = string[index]
            if char == FormattingCodes.bold.value:
                self.bold = not self.bold
                ret.append(self.do_bold())
            else:
                if char == FormattingCodes.colour.value:
                    if self.foreground or self.background:
                        self.foreground = self.background = None
                        ret.append(self.do_colour())
                    if index + 1 > l:
                        break
                    match = self.cmatch.match(string[index + 1:])
                    if not match:
                        index += 1
                        continue
                    self.foreground = Colours(int(match.group(1)) % 16) if match.group(1) is not None else None
                    self.background = Colours(int(match.group(2)) % 16) if match.group(2) is not None else None
                    index += match.end()
                    ret.append(self.do_colour())
                else:
                    if char == FormattingCodes.normal.value:
                        ret.append(self.do_normal())
                        self.reset()
                    else:
                        if char == FormattingCodes.reverse.value:
                            self.reverse = not self.reverse
                            ret.append(self.do_reverse())
                        else:
                            if char == FormattingCodes.italic.value:
                                self.italic = not self.italic
                                ret.append(self.do_italic())
                            else:
                                if char == FormattingCodes.underline.value:
                                    self.underline = not self.underline
                                    ret.append(self.do_underline())
                                else:
                                    ret.append(char)
            index += 1

        ret.append(self.do_normal())
        self.reset()
        return ''.join(ret)

    def do_bold(self):
        """Callback to do bold formatting."""
        raise NotImplementedError()

    def do_colour(self):
        """Callback to do colour formatting."""
        raise NotImplementedError()

    def do_normal(self):
        """Callback to remove all formatting."""
        raise NotImplementedError()

    def do_reverse(self):
        """Callback to do reversal formatting (reverse colours)"""
        raise NotImplementedError()

    def do_italic(self):
        """Callback to do italic formatting."""
        raise NotImplementedError()

    def do_underline(self):
        """Callback to do underline formatting."""
        raise NotImplementedError()


class NullFormatter(Formatter):
    """NullFormatter"""
    do_bold = lambda self: ''
    do_colour = lambda self: ''
    do_normal = lambda self: ''
    do_reverse = lambda self: ''
    do_italic = lambda self: ''
    do_underline = lambda self: ''


class HTMLFormatter(Formatter):
    """HTMLFormatter"""

    def do_bold(self):
        if self.bold:
            return '<b>'
        return '</b>'

    def do_colour(self):
        if not (self.background or self.foreground):
            return '</span>'
        string = '<span style="'
        if self.foreground is not None:
            value = ColoursRGB[self.foreground.name].value.html
            string += 'color:{};'.format(value)
        if self.background is not None:
            value = ColoursRGB[self.background.name].value.html
            string += 'background-color:{};'.format(value)
        string += '">'
        return string

    def do_italic(self):
        if self.italic:
            return '<i>'
        return '</i>'

    def do_normal(self):
        ret = []
        if self.bold:
            ret.append('</b>')
        if self.foreground or self.background:
            ret.append('</span>')
        if self.italic:
            ret.append('</i>')
        if self.underline:
            ret.append('</u>')
        return ''.join(ret)

    def do_reverse(self):
        if self.reverse:
            return '<span style="filter: invert(100%);-webkit-filter: invert(100%);">'
        else:
            return '</span>'

    def do_underline(self):
        if self.underline:
            return '<u>'
        return '</u>'


class ANSIFormatter(Formatter):
    """ANSIFormatter"""
    fmt_normal = '0'
    fmt_bold = ('22', '1')
    fmt_italic = ('23', '3')
    fmt_underline = ('24', '4')
    fmt_reverse = '7'
    fmt_resetforeground = '39'
    fmt_resetbackground = '49'
    sgr = '\x1b[{}m'

    def do_bold(self):
        return self.sgr.format(self.fmt_bold[self.bold])

    def do_colour(self):
        ret = []
        if not (self.foreground and self.background):
            ret.extend((self.fmt_resetforeground, self.fmt_resetbackground))
            if self.bold:
                ret.append(self.fmt_bold[1])
            else:
                ret.append(self.fmt_bold[0])
        else:
            if self.foreground is not None:
                fg = ColoursANSI[self.foreground.name].value
                if self.bold and not fg.intense:
                    ret.append(self.fmt_bold[0])
                elif not self.bold and fg.intense:
                    ret.append(self.fmt_bold[1])
                ret.append(str(fg.foreground))
            else:
                ret.append(self.fmt_resetforeground)
                if self.bold:
                    ret.append(self.fmt_bold[1])
                if self.background is not None:
                    bg = ColoursANSI[self.background.name].value
                    ret.append(str(bg.background))
                else:
                    ret.append(self.fmt_resetbackground)
        return self.sgr.format(';'.join(ret))

    def do_italic(self):
        return self.sgr.format(self.fmt_italic[self.italic])

    def do_normal(self):
        return self.sgr.format(self.fmt_normal)

    def do_reverse(self):
        return self.sgr.format(self.fmt_reverse)

    def do_underline(self):
        return self.sgr.format(self.fmt_underline[self.underline])


VT100Formatter = ANSIFormatter

class XTerm16ColourFormatter(ANSIFormatter):
    """XTerm16ColourFormatter"""

    def do_colour(self):
        ret = []
        if not (self.foreground and self.background):
            ret.extend((self.fmt_resetforeground, self.fmt_resetbackground))
        else:
            if self.foreground is not None:
                fg = ColoursANSI[self.foreground.name].value
                ret.append(str(fg.foreground_16))
            else:
                ret.append(self.fmt_resetforeground)
            if self.background is not None:
                bg = ColoursANSI[self.background.name].value
                ret.append(str(fg.background_16))
            else:
                ret.append(self.fmt_resetbackground)
        return self.sgr.format(';'.join(ret))


class XTerm256ColourFormatter(ANSIFormatter):
    """XTerm256ColourFormatter"""
    format_bg = ('48', '5')
    format_fg = ('38', '5')

    def do_colour(self):
        ret = []
        if not (self.foreground and self.background):
            ret.extend((self.fmt_resetforeground, self.fmt_resetbackground))
        else:
            if self.foreground is not None:
                ret.extend(self.format_fg)
                colour = ColoursXTerm256[self.foreground.name].value
                ret.append(str(colour))
            else:
                ret.append(self.fmt_resetforeground)
            if self.background is not None:
                ret.extend(self.format_bg)
                colour = ColoursXTerm256[self.background.name].value
                ret.append(str(colour))
            else:
                ret.append(self.fmt_resetbackground)
        return self.sgr.format(';'.join(ret))


class XTermTrueColourFormatter(ANSIFormatter):
    """XTermTrueColourFormatter"""
    format_bg = ('48', '2')
    format_fg = ('38', '2')

    def do_colour(self):
        ret = []
        if not (self.foreground and self.background):
            ret.extend((self.fmt_resetforeground, self.fmt_resetbackground))
        else:
            if self.foreground is not None:
                ret.extend(self.format_fg)
                colour = ColoursRGB[self.foreground.name].value
                ret.append(str(colour.red))
                ret.append(str(colour.green))
                ret.append(str(colour.blue))
            else:
                ret.append(self.fmt_resetforeground)
            if self.background is not None:
                ret.extend(self.format_bg)
                colour = ColoursRGB[self.background.name].value
                ret.append(str(colour.red))
                ret.append(str(colour.green))
                ret.append(str(colour.blue))
            else:
                ret.append(self.fmt_resetbackground)
        return self.sgr.format(';'.join(ret))


def select_formatter():
    """Heuristically choose the best formatter. It may not be correct in all
    cases; this is for simple applications such as a bot.

    If Curses is found, it will check if stdout is a terminal. If it isn't,
    :py:class:`~PyIRC.formatting.formatters.NullFormatter` is chosen. If it
    is, the number of colours the terminal supports is probed, which
    determines which formatter will be used.

    If the platform is Windows, the
    :py:class:`~PyIRC.formatting.formatters.ANSIFormatter` will be chosen.

    If your environment supports ≥ 256 colours, set the environmental
    variable ``TRUECOLOUR`` or ``TRUECOLOR`` to any value but 0 to try
    full-colour support using the 
    :py:class:`~PyIRC.formatting.formatters.XTermTrueColourFormatter``.
    """
    if curses is not None:
        if hasattr(os, 'isatty') and not os.isatty(sys.stdout.fileno()):
            return NullFormatter
        curses.setupterm()
        colors = curses.tigetnum('colors')
        if colors >= 256:
            t = os.environ.get('TRUECOLOR', os.environ.get('TRUECOLOUR'), False)
            if t and t != '0':
                return XTermTrueColourFormatter
            return XTerm256ColourFormatter
        if colours >= 16:
            return XTerm16ColourFormatter
        return ANSIFormatter
    else:
        if sys.platform.startswith('win32'):
            return ANSIFormatter
        return NullFormatter
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /botfly/ui.py
# Compiled at: 2019-11-10 20:54:18
# Size of source mod 2**32: 10982 bytes
__doc__ = '\nUser Interface base classes.\n'
__all__ = [
 'UserInterface']
import os, sys, time, textwrap
from pprint import PrettyPrinter
from prompt_toolkit import ANSI
from prompt_toolkit.completion import DummyCompleter
from .fsm import FSM, ANY
RESET = NORMAL = '\x1b[0m'
BLACK = '\x1b[30m'
RED = '\x1b[31m'
GREEN = '\x1b[32m'
YELLOW = '\x1b[33m'
BLUE = '\x1b[34m'
MAGENTA = '\x1b[35m'
CYAN = '\x1b[36m'
GREY = '\x1b[37m'
LT_RED = '\x1b[31;01m'
LT_GREEN = '\x1b[32;01m'
LT_YELLOW = '\x1b[33;01m'
LT_BLUE = '\x1b[34;01m'
LT_MAGENTA = '\x1b[35;01m'
LT_CYAN = '\x1b[36;01m'
LT_GREY = '\x1b[37;01m'
BRIGHT = '\x1b[01m'
UNDERSCORE = '\x1b[4m'
BLINK = '\x1b[5m'
DEFAULT = '\x1b[39;49m'

class Theme:
    NORMAL = RESET
    DEFAULT = DEFAULT
    BOLD = BRIGHT
    BRIGHT = BRIGHT
    BLACK = BLACK
    RED = RED
    GREEN = GREEN
    YELLOW = YELLOW
    BLUE = BLUE
    MAGENTA = MAGENTA
    CYAN = CYAN
    WHITE = GREY
    GREY = GREY
    BRIGHTRED = LT_RED
    BRIGHTGREEN = LT_GREEN
    BRIGHTYELLOW = LT_YELLOW
    BRIGHTBLUE = LT_BLUE
    BRIGHTMAGENTA = LT_MAGENTA
    BRIGHTCYAN = LT_CYAN
    BRIGHTWHITE = LT_GREY
    UNDERSCORE = UNDERSCORE
    BLINK = BLINK
    HELP_TEXT = BRIGHTWHITE

    def __init__(self, ps1='%gDebug%N:%y%S>%N ', ps2='more> ', ps3='choose', ps4='-> '):
        self._ps1 = ps1
        self._ps2 = ps2
        self._ps3 = ps3
        self._ps4 = ps4

    def _set_ps1(self, new):
        self._ps1 = str(new)

    def _set_ps2(self, new):
        self._ps2 = str(new)

    def _set_ps3(self, new):
        self._ps3 = str(new)

    def _set_ps4(self, new):
        self._ps4 = str(new)

    ps1 = property(lambda s: s._ps1, _set_ps1, None, 'primary prompt')
    ps2 = property(lambda s: s._ps2, _set_ps2, None, 'more input needed')
    ps3 = property(lambda s: s._ps3, _set_ps3, None, 'choose prompt')
    ps4 = property(lambda s: s._ps4, _set_ps4, None, 'text input prompt')


class UserInterface:
    """UserInterface"""

    def __init__(self, io, env=None):
        self._io = io
        self._theme = theme = Theme()
        self.environ = env or 
        self.environ['_'] = None
        self.environ['PS1'] = theme.ps1
        self.environ['PS2'] = theme.ps2
        self.environ['PS3'] = theme.ps3
        self.environ['PS4'] = theme.ps4
        self._cache = {}
        self._initfsm()
        self._printer = PrettyPrinter(indent=1, width=(self._io.columns), depth=None,
          stream=(self._io),
          compact=False)

    @property
    def columns(self):
        return self._io.columns

    @property
    def rows(self):
        return self._io.rows

    def close(self):
        if self._io is not None:
            self._io.close()
            self._io = None

    def clone(self):
        return self.__class__(self._io, self.environ.copy())

    def print(self, *objs, **kwargs):
        (self._io.print)(*objs, **kwargs)

    def pprint(self, obj):
        self._printer.pprint(obj)

    def print_obj(self, obj, nl=1):
        self._io.write(str(obj))
        if nl:
            self._io.write('\n')
        self._io.flush()

    def write(self, text):
        return self._io.write(text)

    def writeerror(self, text):
        return self._io.error(text)

    def printf(self, text):
        """Print text run through the expansion formatter."""
        self._io.print((self.prompt_format(text)), end='')

    def error(self, text):
        self.printf('%r{}%N\n'.format(text))

    def warning(self, text):
        self.printf('%Y{}%N\n'.format(text))

    def _get_prompt(self, name, prompt=None):
        return ANSI(self._input_prompt_format(prompt or ))

    def _input_prompt_format(self, ps):
        self._fsm.process_string(ps)
        return self._getarg()

    def user_input(self, prompt=None, completer=None):
        return self._io.input((self._get_prompt('PS1', prompt)), completer=(completer or ))

    def more_user_input(self):
        return self._io.input(self._get_prompt('PS2'))

    def yes_no(self, prompt, default=True):
        while True:
            yesno = get_input(self.prompt_format(prompt), 'Y' if default else 'N', self._io.input)
            yesno = yesno.upper()
            if yesno.startswith('Y'):
                return True
            if yesno.startswith('N'):
                return False
            self.print('Please enter yes or no.')

    def _format_doc(self, s, color):
        i = s.find('\n')
        if i > 0:
            return color + s[:i] + self._theme.NORMAL + textwrap.indent(textwrap.dedent(self.prompt_format(s[i:])), '  ') + '\n'
        return color + s + self._theme.NORMAL + '\n'

    def print_doc(self, doc):
        self.print(self._format_doc(doc, self._theme.HELP_TEXT))

    def prompt_format(self, ps):
        """Expand percent-exansions in a string and return the result."""
        self._ffsm.process_string(ps)
        if self._ffsm.arg:
            arg = self._ffsm.arg
            self._ffsm.arg = ''
            return arg
        return

    def register_expansion(self, key, func):
        """Register a percent-expansion function.
        The function must take one argument, and return a string. The argument is
        the character expanded on.
        """
        key = str(key)[0]
        if key not in self._PROMPT_EXPANSIONS:
            self._PROMPT_EXPANSIONS[key] = func
        else:
            raise ValueError('expansion key !r{} already exists.'.format(key))

    def unregister_expansion(self, key):
        key = str(key)[0]
        try:
            del self._PROMPT_EXPANSIONS[key]
        except KeyError:
            pass

    def _initfsm(self):
        theme = self._theme
        self._PROMPT_EXPANSIONS = {'I':theme.BRIGHT, 
         'N':theme.NORMAL, 
         'D':theme.DEFAULT, 
         'R':theme.BRIGHTRED, 
         'G':theme.BRIGHTGREEN, 
         'Y':theme.BRIGHTYELLOW, 
         'B':theme.BRIGHTBLUE, 
         'M':theme.BRIGHTMAGENTA, 
         'C':theme.BRIGHTCYAN, 
         'W':theme.BRIGHTWHITE, 
         'r':theme.RED, 
         'g':theme.GREEN, 
         'y':theme.YELLOW, 
         'b':theme.BLUE, 
         'm':theme.MAGENTA, 
         'c':theme.CYAN, 
         'w':theme.WHITE, 
         'n':'\n', 
         'h':self._hostname, 
         'u':self._username, 
         'd':self._cwd, 
         'L':self._shlvl, 
         't':self._time, 
         'T':self._date}
        fp = FSM(0)
        self._fsmstates(fp)
        self._fsm = fp
        ff = FSM(0)
        self._fsmstates(ff)
        self._ffsm = ff

    def _fsmstates(self, fsm):
        fsm.add_default_transition(self._error, 0)
        fsm.add_transition(ANY, 0, self._addtext, 0)
        fsm.add_transition('%', 0, None, 1)
        fsm.add_transition('%', 1, self._addtext, 0)
        fsm.add_transition('{', 1, self._startvar, 2)
        fsm.add_transition('}', 2, self._endvar, 0)
        fsm.add_transition('[', 1, None, 3)
        fsm.add_transition('F', 3, self._startfg, 4)
        fsm.add_transition('B', 3, self._startbg, 5)
        fsm.add_transitions('0123456789', 3, self._startfgd, 4)
        fsm.add_transitions('0123456789', 4, self._fgnum, 4)
        fsm.add_transitions('0123456789', 5, self._bgnum, 5)
        fsm.add_transition(']', 4, self._setfg, 0)
        fsm.add_transition(']', 5, self._setbg, 0)
        fsm.add_transition(ANY, 2, self._vartext, 2)
        fsm.add_transition(ANY, 1, self._prompt_expand, 0)
        fsm.arg = ''

    def _startvar(self, c, fsm):
        fsm.varname = ''

    def _vartext(self, c, fsm):
        fsm.varname += c

    def _endvar(self, c, fsm):
        fsm.arg += str(self.environ.get(fsm.varname, fsm.varname))

    def _startbg(self, c, fsm):
        fsm.bgcol = ''

    def _startfg(self, c, fsm):
        fsm.fgcol = ''

    def _startfgd(self, c, fsm):
        fsm.fgcol = c

    def _fgnum(self, c, fsm):
        fsm.fgcol += c

    def _bgnum(self, c, fsm):
        fsm.bgcol += c

    def _setfg(self, c, fsm):
        fsm.arg += '\x1b[38;5;' + fsm.fgcol + 'm'

    def _setbg(self, c, fsm):
        fsm.arg += '\x1b[48;5;' + fsm.bgcol + 'm'

    def _prompt_expand(self, c, fsm):
        return self._expand(c, fsm, self._PROMPT_EXPANSIONS)

    def _expand(self, c, fsm, mapping):
        try:
            arg = self._cache[c]
        except KeyError:
            try:
                arg = mapping[c]
            except KeyError:
                arg = c
            else:
                if callable(arg):
                    arg = str(arg(c))

        fsm.arg += arg

    def _username(self, c):
        un = os.environ.get('USERNAME') or 
        if un:
            self._cache[c] = un
        return un

    def _shlvl(self, c):
        return str(self.environ.get('SHLVL', ''))

    def _hostname(self, c):
        hn = os.uname()[1]
        self._cache[c] = hn
        return hn

    def _cwd(self, c):
        return os.getcwd()

    def _time(self, c):
        return time.strftime('%H:%M:%S', time.localtime())

    def _date(self, c):
        return time.strftime('%m/%d/%Y', time.localtime())

    def _error(self, input_symbol, fsm):
        print(('Prompt string error: {}\n{!r}'.format(input_symbol)), file=(sys.stderr))
        fsm.reset()

    def _addtext(self, c, fsm):
        fsm.arg += c

    def _getarg(self):
        if self._fsm.arg:
            arg = self._fsm.arg
            self._fsm.arg = ''
            return arg
        return


def get_input(prompt='', default=None, input=input):
    """Get user input with an optional default value."""
    if default is not None:
        ri = input('{} [{}]> '.format(prompt, default))
        if not ri:
            return default
        return ri
    else:
        return input('{}> '.format(prompt))
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/tqdm/tqdm/_utils.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 7868 bytes
import os, subprocess
from platform import system as _curos
import re
CUR_OS = _curos()
IS_WIN = CUR_OS in ('Windows', 'cli')
IS_NIX = not IS_WIN and any(CUR_OS.startswith(i) for i in ('CYGWIN', 'MSYS', 'Linux',
                                                           'Darwin', 'SunOS', 'FreeBSD',
                                                           'NetBSD', 'OpenBSD'))
RE_ANSI = re.compile('\\x1b\\[[;\\d]*[A-Za-z]')
try:
    _range = xrange
except NameError:
    _range = range

try:
    _unich = unichr
except NameError:
    _unich = chr

try:
    _unicode = unicode
except NameError:
    _unicode = str

try:
    if IS_WIN:
        import colorama
        colorama.init()
    else:
        colorama = None
except ImportError:
    colorama = None

try:
    from weakref import WeakSet
except ImportError:
    WeakSet = set

try:
    _basestring = basestring
except NameError:
    _basestring = str

try:
    from collections import OrderedDict as _OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict as _OrderedDict
    except ImportError:
        from collections import MutableMapping

        class _OrderedDict(dict, MutableMapping):

            def __init__(self, *args, **kwds):
                if len(args) > 1:
                    raise TypeError('expected at 1 argument, got %d', len(args))
                if not hasattr(self, '_keys'):
                    self._keys = []
                (self.update)(*args, **kwds)

            def clear(self):
                del self._keys[:]
                dict.clear(self)

            def __setitem__(self, key, value):
                if key not in self:
                    self._keys.append(key)
                dict.__setitem__(self, key, value)

            def __delitem__(self, key):
                dict.__delitem__(self, key)
                self._keys.remove(key)

            def __iter__(self):
                return iter(self._keys)

            def __reversed__(self):
                return reversed(self._keys)

            def popitem(self):
                if not self:
                    raise KeyError
                key = self._keys.pop()
                value = dict.pop(self, key)
                return (key, value)

            def __reduce__(self):
                items = [[k, self[k]] for k in self]
                inst_dict = vars(self).copy()
                inst_dict.pop('_keys', None)
                return (self.__class__, (items,), inst_dict)

            setdefault = MutableMapping.setdefault
            update = MutableMapping.update
            pop = MutableMapping.pop
            keys = MutableMapping.keys
            values = MutableMapping.values
            items = MutableMapping.items

            def __repr__(self):
                pairs = ', '.join(map('%r: %r'.__mod__, self.items()))
                return '%s({%s})' % (self.__class__.__name__, pairs)

            def copy(self):
                return self.__class__(self)

            @classmethod
            def fromkeys(cls, iterable, value=None):
                d = cls()
                for key in iterable:
                    d[key] = value

                return d


class Comparable(object):
    __doc__ = 'Assumes child has self._comparable attr/@property'

    def __lt__(self, other):
        return self._comparable < other._comparable

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        return self._comparable == other._comparable

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other


class SimpleTextIOWrapper(object):
    __doc__ = "\n    Change only `.write()` of the wrapped object by encoding the passed\n    value and passing the result to the wrapped object's `.write()` method.\n    "

    def __init__(self, wrapped, encoding):
        object.__setattr__(self, '_wrapped', wrapped)
        object.__setattr__(self, 'encoding', encoding)

    def write(self, s):
        """
        Encode `s` and pass to the wrapped object's `.write()` method.
        """
        return getattr(self, '_wrapped').write(s.encode(getattr(self, 'encoding')))

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        return setattr(self._wrapped, name, value)


def _is_utf(encoding):
    try:
        '█▉'.encode(encoding)
    except UnicodeEncodeError:
        return False
    except Exception:
        try:
            return encoding.lower().startswith('utf-') or 'U8' == encoding
        except:
            return False

        return True


def _supports_unicode(fp):
    try:
        return _is_utf(fp.encoding)
    except AttributeError:
        return False


def _is_ascii(s):
    if isinstance(s, str):
        for c in s:
            if ord(c) > 255:
                return False

        return True
    else:
        return _supports_unicode(s)


def _environ_cols_wrapper():
    """
    Return a function which gets width and height of console
    (linux,osx,windows,cygwin).
    """
    _environ_cols = None
    if IS_WIN:
        _environ_cols = _environ_cols_windows
        if _environ_cols is None:
            _environ_cols = _environ_cols_tput
    if IS_NIX:
        _environ_cols = _environ_cols_linux
    return _environ_cols


def _environ_cols_windows(fp):
    try:
        from ctypes import windll, create_string_buffer
        import struct
        from sys import stdin, stdout
        io_handle = -12
        if fp == stdin:
            io_handle = -10
        else:
            if fp == stdout:
                io_handle = -11
        h = windll.kernel32.GetStdHandle(io_handle)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            _bufx, _bufy, _curx, _cury, _wattr, left, _top, right, _bottom, _maxx, _maxy = struct.unpack('hhhhHhhhhhh', csbi.raw)
            return right - left
    except:
        pass


def _environ_cols_tput(*_):
    """cygwin xterm (windows)"""
    try:
        import shlex
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        return cols
    except:
        pass


def _environ_cols_linux(fp):
    try:
        from termios import TIOCGWINSZ
        from fcntl import ioctl
        from array import array
    except ImportError:
        return
    else:
        try:
            return array('h', ioctl(fp, TIOCGWINSZ, '\x00\x00\x00\x00\x00\x00\x00\x00'))[1]
        except:
            try:
                return int(os.environ['COLUMNS']) - 1
            except KeyError:
                return


def _term_move_up():
    if os.name == 'nt':
        if colorama is None:
            return ''
    return '\x1b[A'
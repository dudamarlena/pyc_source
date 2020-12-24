# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/console.py
# Compiled at: 2007-01-21 20:27:15
"""
console.py

Linux console goodies.

Copyright (c) 2005 Drew Smathers
See LICENSE for details.

"""
__author__ = 'Drew Smathers'
__copyright__ = '(c) 2005 Drew Smathers'
__revision__ = '$Revision: 399 $'
__license__ = 'MIT'
from xix.utils.python import setAll
globs = globals()
RESET = 0
BOLD = 1
HALF_BRIGHT = 2
UNDERSCRORE = 4
BLINK = 5
REVERSE_VIDEO = 7
RESET_MAPPING = 10
SELECT_NULL_MAPPING1 = 11
SELECT_NULL_MAPPING2 = 12
NORMAL_INTENSITY = 22
UNDERLINE_OFF = 24
BLINK_OFF = 25
UNSET_REVERSE_VIDEO = 27
FOREGROUND = dict(BLACK=30, RED=31, GREEN=32, BROWN=33, BLUE=34, MAGENTA=35, CYAN=36, WHITE=37, DEFAULT1=38, DEFAULT2=39)
for (k, v) in FOREGROUND.items():
    globs['FG' + k] = v

BACKGROUND = dict(BLACK=40, GRED=41, GREEN=42, BROWN=43, BLUE=44, MAGENTA=45, CYAN=46, WHITE=47, DEFAULT=49)
for (k, v) in BACKGROUND.items():
    globs['BG' + k] = v

class Format:
    __module__ = __name__
    format_on = True

    def __call__(self, message, *codes):
        return self.format(message, *codes)

    def format(self, message, *codes):
        r"""Format meessage give list of codes defined as globals in this module.
        
        Example usage:
         
        >>> from xix.utils.console import format
        >>> s = format('console test', FGBROWN, BGBLUE, BOLD)
        >>> s
        '\x1b[33;44;1mconsole test\x1b[0m'
       
        Supressing format in application:
            
        >>> format.format_on = False
        >>> s = format('console test')
        >>> s
        'console test'
        
        """
        if not self.format_on:
            return message
        code_string = (';').join([ str(code) for code in codes ])
        return '\x1b[%sm%s\x1b[%sm' % (code_string, message, RESET)


class FormatFactory:
    """Example Usage:

    >>> factory = FormatFactory()
    >>> factory['a'] = Format() 
    >>> factory['b'] = Format()
    >>> factory['a'].format_on = False
    >>> print int(factory['a'].format_on), int(factory['b'].format_on)
    0 1
    """
    __module__ = __name__

    def __init__(self):
        self._reg = {}

    def __getitem__(self, name):
        return self._reg[name]

    def __setitem__(self, name, fmt):
        if self._reg.has_key(name):
            raise ValueError, 'Format named %s already registered' % name
        self._reg[name] = fmt


format = Format()
formatFactory = FormatFactory()
__all__ = setAll([], locals(), 'setAll', 'k', 'v')
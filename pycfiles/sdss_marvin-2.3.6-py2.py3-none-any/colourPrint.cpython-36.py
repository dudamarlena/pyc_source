# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/marvin_brain/python/brain/core/colourPrint.py
# Compiled at: 2018-01-12 14:08:14
# Size of source mod 2**32: 6522 bytes
"""
colourPrint.py

Created by José Sánchez-Gallego on 19 Nov 2013.
Copyright (c) 2013. All rights reserved.
Licensed under a 3-clause BSD license.

This module includes astropy-based functions for colour printing.

"""
from __future__ import absolute_import, division, print_function, unicode_literals
__ALL__ = [
 'colourPrint']
import sys, multiprocessing, threading, codecs, locale
try:
    get_ipython()
except NameError:
    OutStream = None
    stdio = sys
else:
    try:
        from IPython.zmq.iostream import OutStream
        from IPython.utils import io
        stdio = io
    except ImportError:
        OutStream = None
        stdio = sys

    IS_PY3 = sys.version_info[0] == 3
    _DEFAULT_ENCODING = 'utf-8'

    def _write_with_fallback(s, write, fileobj):
        """Write the supplied string with the given write function like
    ``write(s)``, but use a writer for the locale's preferred encoding in case
    of a UnicodeEncodeError.  Failing that attempt to write with 'utf-8' or
    'latin-1'.
    """
        try:
            write(s)
            return write
        except UnicodeEncodeError:
            pass

        enc = locale.getpreferredencoding()
        try:
            Writer = codecs.getwriter(enc)
        except LookupError:
            Writer = codecs.getwriter(_DEFAULT_ENCODING)

        f = Writer(fileobj)
        write = f.write
        try:
            write(s)
            return write
        except UnicodeEncodeError:
            Writer = codecs.getwriter('latin-1')
            f = Writer(fileobj)
            write = f.write

        write(s)
        return write


    def isatty(file):
        """
    Returns `True` if `file` is a tty.

    Most built-in Python file-like objects have an `isatty` member,
    but some user-defined types may not, so this assumes those are not
    ttys.
    """
        if multiprocessing.current_process().name != 'MainProcess' or threading.current_thread().getName() != 'MainThread':
            return False
        else:
            if OutStream is not None:
                if isinstance(file, OutStream):
                    if file.name == 'stdout':
                        return True
            if hasattr(file, 'isatty'):
                return file.isatty()
            return False


    def _color_text(text, color):
        """
    Returns a string wrapped in ANSI color codes for coloring the
    text in a terminal::

        colored_text = color_text('Here is a message', 'blue')

    This won't actually effect the text until it is printed to the
    terminal.

    Parameters
    ----------
    text : str
        The string to return, bounded by the color codes.
    color : str
        An ANSI terminal color name. Must be one of:
        black, red, green, brown, blue, magenta, cyan, lightgrey,
        default, darkgrey, lightred, lightgreen, yellow, lightblue,
        lightmagenta, lightcyan, white, or '' (the empty string).
    """
        color_mapping = {'black':'0;30', 
         'red':'0;31', 
         'green':'0;32', 
         'brown':'0;33', 
         'blue':'0;34', 
         'magenta':'0;35', 
         'cyan':'0;36', 
         'lightgrey':'0;37', 
         'default':'0;39', 
         'darkgrey':'1;30', 
         'lightred':'1;31', 
         'lightgreen':'1;32', 
         'yellow':'1;33', 
         'lightblue':'1;34', 
         'lightmagenta':'1;35', 
         'lightcyan':'1;36', 
         'white':'1;37'}
        if sys.platform == 'win32':
            if OutStream is None:
                return text
        color_code = color_mapping.get(color, '0;39')
        return '\x1b[{0}m{1}\x1b[0m'.format(color_code, text)


    def _decode_preferred_encoding(s):
        """Decode the supplied byte string using the preferred encoding
    for the locale (`locale.getpreferredencoding`) or, if the default encoding
    is invalid, fall back first on utf-8, then on latin-1 if the message cannot
    be decoded with utf-8.
    """
        enc = locale.getpreferredencoding()
        try:
            try:
                return s.decode(enc)
            except LookupError:
                enc = _DEFAULT_ENCODING

            return s.decode(enc)
        except UnicodeDecodeError:
            return s.decode('latin-1')


    def colourPrint(*args, **kwargs):
        r"""
    Prints colors and styles to the terminal uses ANSI escape
    sequences.

    ::

       color_print('This is the color ', 'default', 'GREEN', 'green')

    Parameters
    ----------
    positional args : strings
        The positional arguments come in pairs (*msg*, *color*), where
        *msg* is the string to display and *color* is the color to
        display it in.

        *color* is an ANSI terminal color name.  Must be one of:
        black, red, green, brown, blue, magenta, cyan, lightgrey,
        default, darkgrey, lightred, lightgreen, yellow, lightblue,
        lightmagenta, lightcyan, white, or '' (the empty string).

    file : writeable file-like object, optional
        Where to write to.  Defaults to `sys.stdout`.  If file is not
        a tty (as determined by calling its `isatty` member, if one
        exists), no coloring will be included.

    end : str, optional
        The ending of the message.  Defaults to ``\n``.  The end will
        be printed after resetting any color or font state.
    """
        file = kwargs.get('file', stdio.stdout)
        end = kwargs.get('end', '\n')
        write = file.write
        if isatty(file):
            for i in range(0, len(args), 2):
                msg = args[i]
                if i + 1 == len(args):
                    color = ''
                else:
                    color = args[(i + 1)]
                if color:
                    msg = _color_text(msg, color)
                if not IS_PY3:
                    if isinstance(msg, bytes):
                        msg = _decode_preferred_encoding(msg)
                write = _write_with_fallback(msg, write, file)

            write(end)
        else:
            for i in range(0, len(args), 2):
                msg = args[i]
                if not IS_PY3:
                    if isinstance(msg, bytes):
                        msg = _decode_preferred_encoding(msg)
                write(msg)

            write(end)
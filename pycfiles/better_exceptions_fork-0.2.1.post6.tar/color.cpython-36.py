# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\adrie\Desktop\Programmation\better-exceptions\better_exceptions\color.py
# Compiled at: 2018-01-24 17:26:56
# Size of source mod 2**32: 2566 bytes
"""Checks if the current terminal supports colors.

Also specifies the stream to write to. On Windows, this is a wrapped
stream.
"""
from __future__ import absolute_import
import errno, os, struct, sys
STREAM = sys.stderr
SUPPORTS_COLOR = False

def get_terminfo_file():
    term = os.getenv('TERM', None)
    if term is None:
        return
    else:
        terminfo_dirs = [
         os.path.expanduser('~/.terminfo'),
         '/etc/terminfo',
         '/lib/terminfo',
         '/usr/share/terminfo',
         '/usr/lib/terminfo',
         '/usr/share/lib/terminfo',
         '/usr/local/lib/terminfo',
         '/usr/local/share/terminfo']
        subdirs = [
         '%0.2X' % ord(term[0]),
         term[0]]
        f = None
        for terminfo_dir in terminfo_dirs:
            for subdir in subdirs:
                terminfo_path = os.path.join(terminfo_dir, subdir, term)
                try:
                    f = open(terminfo_path, 'rb')
                    break
                except IOError as e:
                    if e.errno != errno.ENOENT:
                        raise

        return f


force_color = os.getenv('FORCE_COLOR', None)
if force_color == '1':
    SUPPORTS_COLOR = True
else:
    if force_color == '0':
        SUPPORTS_COLOR = False
    else:
        if os.name == 'nt':
            from colorama import init as init_colorama, AnsiToWin32
            init_colorama(wrap=False)
            STREAM = AnsiToWin32(sys.stderr).stream
            SUPPORTS_COLOR = True
        else:
            try:
                is_tty = os.isatty(2)
            except OSError:
                is_tty = False

if is_tty:
    f = get_terminfo_file()
    if f is not None:
        with f:
            magic_number = struct.unpack('<h', f.read(2))[0]
            if magic_number == 282:
                offset = 12
                offset += struct.unpack('<h', f.read(2))[0]
                offset += struct.unpack('<h', f.read(2))[0]
                offset += offset % 2
                offset += 26
                f.seek(offset)
                max_colors = struct.unpack('<h', f.read(2))[0]
                if max_colors >= 8:
                    SUPPORTS_COLOR = True
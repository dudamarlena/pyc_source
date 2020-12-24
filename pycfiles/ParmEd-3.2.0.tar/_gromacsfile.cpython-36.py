# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/gromacs/_gromacsfile.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 3941 bytes
"""
Provides a class for reading GROMACS-style files. The key component to these
files is that the ; character is a comment character and everything after ; is
ignored.
"""
from __future__ import division, print_function, absolute_import
from parmed.gromacs._cpp import CPreProcessor

class GromacsFile(object):
    __doc__ = '\n    A GROMACS file that recognizes the ";" character as a \'comment\' token. It\n    can be iterated over and generally treated like a file object, but only\n    spits out strings that have been truncated at its first comment character.\n    \n    There is currently no way to recognize a ; as a _non_ comment character,\n    since allowing an escape character does not seem to be common practice and\n    would likely introduce negative performance implications.\n\n    Parameters\n    ----------\n    fname : str or file-like\n        Name of the file to parse or file-like object to parse\n    defines : dict{str : str}, optional\n        List of defines for the preprocessed file, if any\n    includes : list of str, optional\n        List of include files. Default is taken from environment variables\n        GMXDATA or GMXBIN if they are set. Otherwise, it is looked for in /usr,\n        /usr/local, /opt, or /opt/local. If it is still not found, it is looked\n        for relative to whatever ``mdrun`` executable is in your path\n    notfound_fatal : bool, optional\n        If True, missing include files are fatal. If False, they are a warning.\n        Default is True\n    '

    def __init__(self, fname, **kwargs):
        self._handle = CPreProcessor(fname, **kwargs)
        self.closed = False
        self.line_number = 0

    def __iter__(self):
        parts = []
        for line in self._handle:
            try:
                idx = line.index(';')
                if not parts:
                    yield '%s\n' % line[:idx]
                else:
                    parts.append('%s' % line[:idx])
                    yield '%s\n' % ''.join(parts)
                    parts = []
            except ValueError:
                if line.rstrip('\r\n').endswith('\\'):
                    chars = list(reversed(line.rstrip('\r\n')))
                    del chars[chars.index('\\')]
                    parts.append('%s ' % ''.join(reversed(chars)))
                else:
                    if parts:
                        parts.append(line)
                        yield ''.join(parts)
                        parts = []
                    else:
                        yield line

    @property
    def included_files(self):
        return self._handle.included_files

    def readline(self):
        parts = []
        self.line_number += 1
        line = True
        while line:
            line = self._handle.readline()
            try:
                idx = line.index(';')
                if not parts:
                    return '%s\n' % line[:idx]
                else:
                    parts.append('%s' % line[:idx])
                    return '%s\n' % ''.join(parts)
            except ValueError:
                if line.rstrip('\r\n').endswith('\\'):
                    chars = list(reversed(line.rstrip('\r\n')))
                    del chars[chars.index('\\')]
                    parts.append('%s ' % ''.join(reversed(chars)))
                else:
                    if parts:
                        parts.append(line)
                        return ''.join(parts)
                    else:
                        return line

    def readlines(self):
        return [line for line in self]

    def read(self):
        return ''.join(self.readlines())

    def close(self):
        self._handle.close()
        self.closed = True

    def __del__(self):
        try:
            self.closed or self._handle.close()
        except AttributeError:
            pass
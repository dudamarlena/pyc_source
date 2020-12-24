# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/nlreadline.py
# Compiled at: 2009-12-08 17:43:28
"""
File wrapper that changes the semantics of the readline function
to never return a non-empty line without a line terminator.
"""
__rcsid__ = '$Id: nlreadline.py 22911 2008-06-03 05:06:10Z dang $'
__author__ = 'Dan Gunter'

class BufferedReadline:
    """Change semantics of file.readline() to return either 
    a complete line with a newline terminator or an empty line.
    Partial lines are buffered between calls until the newline
    is found.
    """

    def __init__(self, fileobj):
        self._f = fileobj
        self._buf = ''

    def __getattr__(self, x):
        """Delegate all public methods except readline()."""
        if x and x[0] == '_':
            try:
                return self.__dict__[x]
            except KeyError:
                raise AttributeError("'%s' object has no attribute '%s'" % (
                 self.__class__.__name__, x))

        return getattr(self._f, x)

    def readline(self):
        """Override readline() to get new semantics."""
        if self._f is None:
            return ''
        else:
            line = self._f.readline()
            if line == '':
                pass
            elif line[(-1)] == '\n':
                if self._buf:
                    line = self._buf + line
                    self._buf = ''
            else:
                self._buf += line
                line = ''
            return line

    def readlines(self):
        """Override readlines() so it calls our readline()."""
        if self._f is None:
            return ''
        else:
            return [ line for line in self.readline() ]

    def xreadlines(self):
        """Override xreadlines() so it calls our readline()."""
        while 1:
            line = self.readline()
            if line:
                yield line
            else:
                raise StopIteration

    def close(self):
        if self._f is not None:
            self._f.close()
        self._f = None
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/flexirest/util.py
# Compiled at: 2009-11-13 06:00:08
from __future__ import with_statement
import os, sys
from cStringIO import StringIO
__docformat__ = 'reStructuredText'

class StdoutConsole(object):
    """
    Vaguely file-like object that immediately writes it output to
    `sys.stdout` followed by an os-appropriate `EOL`.
    """

    def __init__(self):
        self.out = sys.stdout

    def write(self, msg):
        self.out.write(msg + os.linesep)


class Duck(object):
    """Quack!"""

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        """
        Thanks to Chris Jones!
        """
        a = (', ').join(('%s=%r' % i for i in self.__dict__.items()))
        return '<%s object at 0x%x%s%s>' % (
         type(self).__name__, id(self), ': ' if a else '', a)


class BufferedFile(file):
    """
    File-like object that writes to an internal buffer. It will only
    write to the file system when it's `.close()` method is called
    **and** it has actually written something to itself.

    Inspired by `tempfile.SpooledTemporaryFile`, but with far less
    features (yagni.. for now it only supports writing, for example).
    """

    def __init__(self, path):
        self._buf = StringIO()
        self.path = path
        super(BufferedFile, self).__init__(os.devnull, 'wb')

    def write(self, data):
        self._buf.write(data)

    def flush(self):
        curdata = self._buf.getvalue()
        if len(curdata) > 0:
            with open(self.path, 'wb') as (fp):
                fp.write(curdata)

    def close(self):
        self.flush()
        super(BufferedFile, self).close()
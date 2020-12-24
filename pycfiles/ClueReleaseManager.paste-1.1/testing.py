# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/clue/tools/testing.py
# Compiled at: 2008-06-29 13:53:17
from clue.tools import fileio
import atexit

class Mock(object):
    """A mock class.

      >>> m = Mock(a=1)
      >>> m.a
      1
    """

    def __init__(self, **kw):
        self.__dict__.update(kw)


class MockDict(Mock):

    def __getitem__(self, k):
        return getattr(self, k)


_tracker = fileio.TempTracker()
gen_tempfile = _tracker.gen_tempfile
gen_tempdir = _tracker.gen_tempdir
atexit.register(_tracker.cleanup)
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/searcher/stub.py
# Compiled at: 2018-12-29 12:21:47
from pysmi.searcher.base import AbstractSearcher
from pysmi import debug
from pysmi import error

class StubSearcher(AbstractSearcher):
    """Figures out if given MIB module is present in a fixed list of modules.
    """
    __module__ = __name__

    def __init__(self, *mibnames):
        """Create an instance of *StubSearcher* initialized with a fixed list
           or MIB modules names.

           Args:
               mibnames (str): blacklisted MIB names
        """
        self._mibnames = mibnames

    def __str__(self):
        return '%s' % self.__class__.__name__

    def fileExists(self, mibname, mtime, rebuild=False):
        if mibname in self._mibnames:
            debug.logger & debug.flagSearcher and debug.logger('pretend compiled %s exists and is very new' % mibname)
            raise error.PySmiFileNotModifiedError('compiled file %s is among %s' % (mibname, (', ').join(self._mibnames)), searcher=self)
        raise error.PySmiFileNotFoundError('no compiled file %s found among %s' % (mibname, (', ').join(self._mibnames)), searcher=self)
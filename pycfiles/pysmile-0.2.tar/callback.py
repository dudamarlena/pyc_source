# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/writer/callback.py
# Compiled at: 2018-12-29 12:21:47
import sys
from pysmi.writer.base import AbstractWriter
from pysmi import debug
from pysmi import error

class CallbackWriter(AbstractWriter):
    """Invokes user-specified callable and passes transformed
       MIB module to it.

       Note: user callable object signature must be as follows

       .. function:: cbFun(mibname, contents, cbCtx)

    """
    __module__ = __name__

    def __init__(self, cbFun, cbCtx=None):
        """Creates an instance of *CallbackWriter* class.

        Args:
            cbFun (callable): user-supplied callable
        Keyword Args:
            cbCtx: user-supplied object passed intact to user callback
        """
        self._cbFun = cbFun
        self._cbCtx = cbCtx

    def __str__(self):
        return '%s{"%s"}' % (self.__class__.__name__, self._cbFun)

    def putData(self, mibname, data, comments=(), dryRun=False):
        if dryRun:
            debug.logger & debug.flagWriter and debug.logger('dry run mode')
            return
        try:
            self._cbFun(mibname, data, self._cbCtx)
        except Exception:
            raise error.PySmiWriterError('user callback %s failure writing %s: %s' % (self._cbFun, mibname, sys.exc_info()[1]), writer=self)

        debug.logger & debug.flagWriter and debug.logger('user callback for %s succeeded' % mibname)

    def getData(self, filename):
        return ''
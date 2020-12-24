# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/change_SuperChange.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 4120 bytes
import sys, os, os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin

from os.path import getmtime, exists
import time, types
import Cheetah.Version as RequiredCheetahVersion
import Cheetah.Version as RequiredCheetahVersionTuple
import Cheetah.Template as Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
import Cheetah.CacheRegion as CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Cheetah.compat import unicode
import javatools.cheetah.change_Change as change_Change
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/change_SuperChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class change_SuperChange(change_Change):

    def __init__(self, *args, **KWs):
        (super(change_SuperChange, self).__init__)(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v

            (self._initCheetahInstance)(**cheetahKWArgs)

    def writeBody(self, **KWS):
        trans = KWS.get('trans')
        if not trans:
            if not self._CHEETAH__isBuffering:
                if not callable(self.transaction):
                    trans = self.transaction
        elif not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else:
            _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        write('\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_change_SuperChange = 'writeBody'


if not hasattr(change_SuperChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(change_SuperChange, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(change_SuperChange)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(change_SuperChange())).run()
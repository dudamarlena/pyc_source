# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/change_Change.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 8321 bytes
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
import javatools.cheetah as escape
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/change_Change.tmpl'
__CHEETAH_srcLastModified__ = 'Mon Aug 11 11:39:00 2014'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class change_Change(Template):

    def __init__(self, *args, **KWs):
        (super(change_Change, self).__init__)(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v

            (self._initCheetahInstance)(**cheetahKWArgs)

    def description(self, **KWS):
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
        write('\n<!-- START BLOCK: description -->\n<div class="description">\n')
        _v = VFFSL(SL, 'escape', False)(VFFSL(SL, 'change.label', True))
        if _v is not None:
            write(_filter(_v, rawExpr='$escape($change.label)'))
        write('\n</div>\n')
        write('\n<!-- END BLOCK: description -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def details(self, **KWS):
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
        write('\n<!-- START BLOCK: details -->\n')
        write('\n<!-- END BLOCK: details -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def collect(self, **KWS):
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
        write('\n<!-- START BLOCK: collect -->\n')
        if VFN(VFFSL(SL, 'change', True), 'collect', False)():
            write('<div class="collect">\n')
            for child in VFN(VFFSL(SL, 'change', True), 'collect', False)():
                _v = VFFSL(SL, 'render_change', False)(child)
                if _v is not None:
                    write(_filter(_v, rawExpr='$render_change(child)'))
                write('\n')

            write('</div>\n')
        write('\n<!-- END BLOCK: collect -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def respond(self, trans=None):
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
            write('\n\n')
            ch = getattr(self, 'change')
            opts = getattr(self, 'options')
            cl = [
             'Change']
            cl.append(type(ch).__name__)
            if ch.is_change():
                cl.append('is_changed')
                if ch.is_ignored(opts):
                    cl.append('is_ignored')
        else:
            cl.append('is_unchanged')
        cl = ' '.join(cl)
        write('\n\n\n<div class="')
        write(_filter(cl))
        write('">\n\n')
        self.description(trans=trans)
        write('\n\n')
        self.details(trans=trans)
        write('\n\n')
        self.collect(trans=trans)
        write('\n</div>\n\n\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_change_Change = 'respond'


if not hasattr(change_Change, '_initCheetahAttributes'):
    templateAPIClass = getattr(change_Change, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(change_Change)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(change_Change())).run()
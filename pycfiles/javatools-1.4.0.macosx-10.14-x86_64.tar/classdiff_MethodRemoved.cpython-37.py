# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/classdiff_MethodRemoved.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 11525 bytes
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
import javatools.cheetah as escape
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_MethodRemoved.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class classdiff_MethodRemoved(change_Change):

    def __init__(self, *args, **KWs):
        (super(classdiff_MethodRemoved, self).__init__)(*args, **KWs)
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
        write('\n<!-- START BLOCK: description -->\n')
        change = getattr(self, 'change')
        info = change.get_ldata()
        a = info.get_name()
        b = ', '.join(info.pretty_arg_types())
        c = info.pretty_type()
        write('\n<h3>')
        write(_filter(escape('%s(%s):%s' % (a, b, c))))
        write('</h3>\n<div class="description">Method Removed</div>\n')
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
        write('\n<!-- START BLOCK: details -->\n<div class="details">\n<div class="lrdata">\n')
        _v = VFFSL(SL, 'method_table', False)(VFN(VFFSL(SL, 'change', True), 'get_ldata', False)())
        if _v is not None:
            write(_filter(_v, rawExpr='$method_table($change.get_ldata())'))
        write('\n</div>\n</div>\n')
        write('\n<!-- END BLOCK: details -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def method_table(self, info, **KWS):
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
        write('<table class="left-headers">\n')
        _v = VFFSL(SL, 'row', False)('Method Name', info.get_name())
        if _v is not None:
            write(_filter(_v, rawExpr='$row("Method Name", info.get_name())'))
        write('\n')
        _v = VFFSL(SL, 'row', False)('Return Type', info.pretty_type())
        if _v is not None:
            write(_filter(_v, rawExpr='$row("Return Type", info.pretty_type())'))
        write('\n')
        _v = VFFSL(SL, 'row', False)('Argument Types', '(%s)' % ', '.join(info.pretty_arg_types()))
        if _v is not None:
            write(_filter(_v, rawExpr='$row("Argument Types", "(%s)" % ", ".join(info.pretty_arg_types()))'))
        write('\n')
        _v = VFFSL(SL, 'row', False)('Method Flags', '0x%04x: %s' % (
         info.access_flags, ' '.join(info.pretty_access_flags())))
        if _v is not None:
            write(_filter(_v, rawExpr='$row("Method Flags", "0x%04x: %s" %\n      (info.access_flags, " ".join(info.pretty_access_flags())))'))
        write('\n\n')
        if info.get_signature():
            _v = VFFSL(SL, 'row', False)('Generics Signature', info.get_signature())
            if _v is not None:
                write(_filter(_v, rawExpr='$row("Generics Signature", info.get_signature())'))
            write('\n')
        write('\n')
        if info.get_exceptions():
            _v = VFFSL(SL, 'row', False)('Exceptions', ', '.join(info.pretty_exceptions()))
            if _v is not None:
                write(_filter(_v, rawExpr='$row("Exceptions", ", ".join(info.pretty_exceptions()))'))
            write('\n')
        write('\n')
        if not info.get_code():
            _v = VFFSL(SL, 'row', False)('Abstract', 'True')
            if _v is not None:
                write(_filter(_v, rawExpr='$row("Abstract", "True")'))
            write('\n')
        write('\n')
        if info.is_deprecated():
            _v = VFFSL(SL, 'row', False)('Deprecated', 'True')
            if _v is not None:
                write(_filter(_v, rawExpr='$row("Deprecated", "True")'))
            write('\n')
        write('\n</table>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def row(self, label, data, **KWS):
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
        write('<tr>\n<th>')
        _v = VFFSL(SL, 'label', True)
        if _v is not None:
            write(_filter(_v, rawExpr='$label'))
        write('</th>\n<td>')
        write(_filter(escape(data)))
        write('</td>\n</tr>\n')
        return _dummyTrans and trans.response().getvalue() or ''

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
        write('\n\n\n')
        self.description(trans=trans)
        write('\n\n\n')
        self.details(trans=trans)
        write('\n\n\n\n\n\n\n\n\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_classdiff_MethodRemoved = 'writeBody'


if not hasattr(classdiff_MethodRemoved, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_MethodRemoved, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_MethodRemoved)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(classdiff_MethodRemoved())).run()
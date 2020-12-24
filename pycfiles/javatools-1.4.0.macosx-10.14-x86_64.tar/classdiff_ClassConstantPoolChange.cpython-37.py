# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/classdiff_ClassConstantPoolChange.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 9832 bytes
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
import javatools.cheetah.subreport as subreport
from javatools.classdiff import pretty_merge_constants
import javatools.cheetah as escape
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_ClassConstantPoolChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class classdiff_ClassConstantPoolChange(subreport):

    def __init__(self, *args, **KWs):
        (super(classdiff_ClassConstantPoolChange, self).__init__)(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v

            (self._initCheetahInstance)(**cheetahKWArgs)

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
        if VFN(VFFSL(SL, 'change', True), 'is_change', False)():
            _v = VFFSL(SL, 'render_dual_constant_pool', False)(VFN(VFFSL(SL, 'change', True), 'get_ldata', False)(), VFN(VFFSL(SL, 'change', True), 'get_rdata', False)())
            if _v is not None:
                write(_filter(_v, rawExpr='$render_dual_constant_pool($change.get_ldata(), $change.get_rdata())'))
            write('\n')
        else:
            _v = VFFSL(SL, 'render_constant_pool', False)(VFN(VFFSL(SL, 'change', True), 'pretty_ldata', False)())
            if _v is not None:
                write(_filter(_v, rawExpr='$render_constant_pool($change.pretty_ldata())'))
            write('\n')
        write('</div>\n</div>\n')
        write('\n<!-- END BLOCK: details -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def render_constant_pool(self, consts, **KWS):
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
        write('<table class="constant-pool">\n<thead>\n<tr>\n<th>Index</th>\n<th>Type</th>\n<th>Value</th>\n</tr>\n</thead>\n\n')
        for i, t, v in consts:
            write('<tr>\n<td class="const-index">')
            write(_filter(i))
            write('</td>\n<td class="const-type">')
            write(_filter(t))
            write('</td>\n<td class="const-value">')
            write(_filter(escape(str(v))))
            write('</td>\n</tr>\n')

        write('\n</table>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def render_dual_constant_pool(self, left, right, **KWS):
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
        write('<table class="dual-constant-pool">\n<thead>\n<tr>\n<th>Index</th>\n<th>Original Type</th>\n<th>Original Value</th>\n<th>Modified Type</th>\n<th>Modified Value</th>\n</tr>\n</thead>\n\n')
        for index, lt, lv, rt, rv in pretty_merge_constants(left, right):
            row_class = ' is_changed'[((lt, lv) == (rt, rv))]
            write('\n<tr>\n<td class="const-index">')
            write(_filter(index))
            write('</td>\n<td class="const-type">')
            write(_filter(lt or ''))
            write('</td>\n<td class="const-value">')
            write(_filter(escape(str(lv or ''))))
            write('</td>\n')
            if (lt, lv) == (rt, rv):
                write('<td class="const-type empty"></td>\n<td class="const-value empty"></td>\n')
            else:
                write('<td class="const-type is_changed">')
                write(_filter(rt or ''))
                write('</td>\n<td class="const-value is_changed">')
                write(_filter(escape(str(rv or ''))))
                write('</td>\n</tr>\n')

        write('\n</table>\n')
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
        self.details(trans=trans)
        write('\n\n\n\n\n\n\n\n\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_classdiff_ClassConstantPoolChange = 'writeBody'


if not hasattr(classdiff_ClassConstantPoolChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_ClassConstantPoolChange, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_ClassConstantPoolChange)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(classdiff_ClassConstantPoolChange())).run()
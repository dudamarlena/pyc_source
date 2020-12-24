# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/classdiff_AnnotationsChange.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 10805 bytes
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
import javatools.cheetah as escape
from six.moves import zip_longest
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_AnnotationsChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class classdiff_AnnotationsChange(subreport):

    def __init__(self, *args, **KWs):
        (super(classdiff_AnnotationsChange, self).__init__)(*args, **KWs)
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
            _v = VFFSL(SL, 'render_dual_annotations', False)(VFN(VFFSL(SL, 'change', True), 'get_ldata', False)(), VFN(VFFSL(SL, 'change', True), 'get_rdata', False)())
            if _v is not None:
                write(_filter(_v, rawExpr='$render_dual_annotations($change.get_ldata(), $change.get_rdata())'))
            write('\n')
        else:
            _v = VFFSL(SL, 'render_annotations', False)(VFN(VFFSL(SL, 'change', True), 'get_ldata', False)())
            if _v is not None:
                write(_filter(_v, rawExpr='$render_annotations($change.get_ldata())'))
            write('\n')
        write('</div>\n</div>\n')
        write('\n<!-- END BLOCK: details -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

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
        write('\n<!-- START BLOCK: description -->\n<div class="description">')
        _v = VFFSL(SL, 'change.label', True)
        if _v is not None:
            write(_filter(_v, rawExpr='$change.label'))
        write('</div>\n')
        write('\n<!-- END BLOCK: description -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def render_annotations(self, annos, **KWS):
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
        write('<table class="annotations">\n<thead>\n<tr>\n<th>Index</th>\n<th>Annotation</th>\n</tr>\n</thead>\n')
        for index in range(0, len(annos)):
            write('<tr>\n<td class="const-index">')
            write(_filter(index))
            write('</td>\n<td class="const-value">')
            write(_filter(annos[index].pretty_annotation()))
            write('</td>\n</tr>\n')

        write('</table>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def render_dual_annotations(self, left, right, **KWS):
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
        write('<table class="annotations">\n<thead>\n<tr>\n<th rowspan="2">Index</th>\n<th colspan="2">Annotation</th>\n</tr>\n<tr>\n<th>Original</th>\n<th>Changed</th>\n</tr>\n</thead>\n')
        index = 0
        write('\n')
        for la, ra in zip_longest(left, right):
            write('<tr>\n<td class="const-index">')
            write(_filter(index))
            write('</td>\n<td class="const-value">\n')
            write(_filter(la and la.pretty_annotation() or ''))
            write('</td>\n\n')
            if la == ra:
                write('<td class="const-value is_unchanged">\n')
                write(_filter(ra and ra.pretty_annotation() or ''))
                write('</td>\n')
            else:
                write('<td class="const-value is_changed">\n')
                write(_filter(ra and ra.pretty_annotation() or ''))
                write('</td>\n')
            write('</tr>\n')
            index += 1
            write('\n')

        write('</table>\n')
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
        write('\n\n')
        self.details(trans=trans)
        write('\n\n')
        self.description(trans=trans)
        write('\n\n\n\n\n\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_classdiff_AnnotationsChange = 'writeBody'


if not hasattr(classdiff_AnnotationsChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_AnnotationsChange, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_AnnotationsChange)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(classdiff_AnnotationsChange())).run()
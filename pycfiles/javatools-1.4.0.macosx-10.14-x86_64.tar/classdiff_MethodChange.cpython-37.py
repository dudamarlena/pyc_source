# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/classdiff_MethodChange.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 25427 bytes
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
from javatools.change import collect_by_typename
import javatools.cheetah as escape
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_MethodChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class classdiff_MethodChange(change_Change):

    def __init__(self, *args, **KWs):
        (super(classdiff_MethodChange, self).__init__)(*args, **KWs)
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
        ldata = change.get_ldata()
        a = ldata.get_name()
        b = ', '.join(ldata.pretty_arg_types())
        c = ldata.pretty_type()
        write('\n<h3>')
        write(_filter(escape('%s(%s):%s' % (a, b, c))))
        write('</h3>\n')
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
        change = getattr(self, 'change')
        data = collect_by_typename(change.collect())
        write('\n\n<div class="details">\n<div class="lrdata">\n\n<table class="left-headers">\n')
        _v = VFFSL(SL, 'sub_name', False)(data.pop('MethodNameChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_name(data.pop("MethodNameChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_type', False)(data.pop('MethodTypeChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_type(data.pop("MethodTypeChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_args', False)(data.pop('MethodParametersChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_args(data.pop("MethodParametersChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_flags', False)(data.pop('MethodAccessflagsChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_flags(data.pop("MethodAccessflagsChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_signature', False)(data.pop('MethodSignatureChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_signature(data.pop("MethodSignatureChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_throws', False)(data.pop('MethodExceptionsChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_throws(data.pop("MethodExceptionsChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_abstract', False)(data.pop('MethodAbstractChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_abstract(data.pop("MethodAbstractChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_deprecation', False)(data.pop('MethodDeprecationChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_deprecation(data.pop("MethodDeprecationChange")[0])'))
        write('\n</table>\n\n</div>\n</div>\n')
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
        change = getattr(self, 'change')
        data = collect_by_typename(change.collect())
        write('\n<div class="collect">\n')
        _v = VFFSL(SL, 'render_change', False)(data.pop('MethodAnnotationsChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$render_change(data.pop("MethodAnnotationsChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'render_change', False)(data.pop('MethodInvisibleAnnotationsChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$render_change(data.pop("MethodInvisibleAnnotationsChange")[0])'))
        write('\n')
        _v = VFFSL(SL, 'render_change', False)(data.pop('MethodCodeChange')[0])
        if _v is not None:
            write(_filter(_v, rawExpr='$render_change(data.pop("MethodCodeChange")[0])'))
        write('\n</div>\n')
        write('\n<!-- END BLOCK: collect -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_name(self, subch, **KWS):
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
        label = 'Method Name'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(escape(subch.pretty_ldata())))
            write('</td>\n</tr>\n<tr>\n<td>')
            write(_filter(escape(subch.pretty_rdata())))
            write('</td>\n</tr>\n')
        else:
            write('<tr>\n<th>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(escape(subch.pretty_ldata())))
            write('\n</tr>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_type(self, subch, **KWS):
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
        label = 'Return Type'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(subch.pretty_ldata()))
            write('</td>\n</tr>\n<tr>\n<td>')
            write(_filter(subch.pretty_rdata()))
            write('</td>\n</tr>\n')
        else:
            write('<tr>\n<th>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(subch.pretty_ldata()))
            write('\n</tr>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_args(self, subch, **KWS):
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
        label = 'Argument Types'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>(')
            write(_filter(', '.join(subch.pretty_ldata())))
            write(')</td>\n</tr>\n<tr>\n<td>(')
            write(_filter(', '.join(subch.pretty_rdata())))
            write(')</td>\n</tr>\n')
        else:
            write('<tr>\n<th>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>(')
            write(_filter(', '.join(subch.pretty_ldata())))
            write(')</td>\n</tr>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_flags(self, subch, **KWS):
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
        label = 'Method Flags'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter('0x%04x' % subch.get_ldata()))
            write(':\n    ')
            write(_filter(' '.join(subch.pretty_ldata())))
            write('</td>\n</tr>\n<tr>\n<td class="is_changed">\n')
            write(_filter('0x%04x' % subch.get_rdata()))
            write(':\n')
            write(_filter(' '.join(subch.pretty_rdata())))
            write('</td>\n</tr>\n')
        else:
            write('<tr>\n<th>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter('0x%04x' % subch.get_ldata()))
            write(':\n    ')
            write(_filter(' '.join(subch.pretty_ldata())))
            write('</td>\n</tr>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_signature(self, subch, **KWS):
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
        label = 'Generics Signature'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(escape(subch.pretty_ldata() or '(None)')))
            write('</td>\n</tr>\n<tr>\n<td class="is_changed">\n ')
            write(_filter(escape(subch.pretty_rdata() or '(None)')))
            write('</td>\n</tr>\n')
        else:
            if subch.get_ldata():
                write('<tr>\n<th>')
                _v = VFFSL(SL, 'label', True)
                if _v is not None:
                    write(_filter(_v, rawExpr='$label'))
                write('</th>\n<td>')
                write(_filter(escape(subch.pretty_ldata())))
                write('</td>\n</tr>\n')
            return _dummyTrans and trans.response().getvalue() or ''

    def sub_throws(self, subch, **KWS):
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
        label = 'Exceptions'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>(')
            write(_filter(', '.join(subch.pretty_ldata())))
            write(')</td>\n</tr>\n<tr>\n<td class="is_changed">(')
            write(_filter(', '.join(subch.pretty_rdata())))
            write(')</td>\n</tr>\n')
        else:
            if subch.get_ldata():
                write('<tr>\n<th>')
                _v = VFFSL(SL, 'label', True)
                if _v is not None:
                    write(_filter(_v, rawExpr='$label'))
                write('</th>\n<td>(')
                write(_filter(', '.join(subch.pretty_ldata())))
                write(')</td>\n</tr>\n')
            return _dummyTrans and trans.response().getvalue() or ''

    def sub_abstract(self, subch, **KWS):
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
        label = 'Abstract'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(subch.pretty_ldata()))
            write('</td>\n</tr>\n<tr>\n<td class="is_changed">')
            write(_filter(subch.pretty_rdata()))
            write('</td>\n</tr>\n')
        else:
            if subch.get_ldata():
                write('<tr>\n<th>')
                _v = VFFSL(SL, 'label', True)
                if _v is not None:
                    write(_filter(_v, rawExpr='$label'))
                write('</th>\n<td>')
                write(_filter(subch.pretty_ldata()))
                write('</td>\n</tr>\n')
            return _dummyTrans and trans.response().getvalue() or ''

    def sub_deprecation(self, subch, **KWS):
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
        label = 'Deprecated'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(subch.pretty_ldata()))
            write('</td>\n</tr>\n<tr>\n<td class="is_changed">')
            write(_filter(subch.pretty_rdata()))
            write('</td>\n</tr>\n')
        else:
            if subch.get_ldata():
                write('<tr>\n<th>')
                _v = VFFSL(SL, 'label', True)
                if _v is not None:
                    write(_filter(_v, rawExpr='$label'))
                write('</th>\n<td>')
                write(_filter(subch.pretty_ldata()))
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
        write('\n\n\n')
        self.collect(trans=trans)
        write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_classdiff_MethodChange = 'writeBody'


if not hasattr(classdiff_MethodChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_MethodChange, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_MethodChange)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(classdiff_MethodChange())).run()
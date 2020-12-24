# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/classdiff_ClassInfoChange.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 23029 bytes
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
from javatools.change import collect_by_typename
import javatools.cheetah as escape
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_ClassInfoChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class classdiff_ClassInfoChange(subreport):

    def __init__(self, *args, **KWs):
        (super(classdiff_ClassInfoChange, self).__init__)(*args, **KWs)
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
        write('\n<!-- START BLOCK: details -->\n')
        change = getattr(self, 'change')
        data = collect_by_typename(change.collect())
        write('\n<div class="details">\n<div class="lrdata">\n\n<table class="left-headers">\n')
        _v = VFFSL(SL, 'sub_classname', False)(data['ClassNameChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_classname(data["ClassNameChange"][0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_flags', False)(data['ClassAccessflagsChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_flags(data["ClassAccessflagsChange"][0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_super', False)(data['ClassSuperclassChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_super(data["ClassSuperclassChange"][0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_inter', False)(data['ClassInterfacesChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_inter(data["ClassInterfacesChange"][0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_version', False)(data['ClassVersionChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_version(data["ClassVersionChange"][0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_platform', False)(data['ClassPlatformChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_platform(data["ClassPlatformChange"][0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_signature', False)(data['ClassSignatureChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_signature(data["ClassSignatureChange"][0])'))
        write('\n')
        _v = VFFSL(SL, 'sub_deprecation', False)(data['ClassDeprecationChange'][0])
        if _v is not None:
            write(_filter(_v, rawExpr='$sub_deprecation(data["ClassDeprecationChange"][0])'))
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
        write('\n<!-- END BLOCK: collect -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_classname(self, subch, **KWS):
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
        label = 'Class Name'
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
            write('</td>\n</tr>\n')
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
        label = 'Class Flags'
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

    def sub_super(self, subch, **KWS):
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
        label = 'Extends'
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
            write('<tr>\n<th>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(subch.pretty_ldata()))
            write('</td>\n</tr>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_inter(self, subch, **KWS):
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
        label = 'Implements'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(', '.join(subch.pretty_ldata()) or '(None)'))
            write('</td>\n</tr>\n<tr>\n<td class="is_changed">\n')
            write(_filter(', '.join(subch.pretty_rdata()) or '(None)'))
            write('</td>\n</tr>\n')
        else:
            if subch.get_ldata():
                write('<tr>\n<th>')
                _v = VFFSL(SL, 'label', True)
                if _v is not None:
                    write(_filter(_v, rawExpr='$label'))
                write('</th>\n<td>')
                write(_filter(', '.join(subch.pretty_ldata())))
                write('</td>\n</tr>\n')
            return _dummyTrans and trans.response().getvalue() or ''

    def sub_version(self, subch, **KWS):
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
        label = 'Java Version'
        templ = 'Major: %i, Minor: %i'
        if subch.is_change():
            write('<tr>\n<th rowspan="2">')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(templ % subch.get_ldata()))
            write('</td>\n</tr>\n<tr>\n<td class="is_changed">')
            write(_filter(templ % subch.get_rdata()))
            write('</td>\n</tr>\n')
        else:
            write('<tr>\n<th>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(templ % subch.get_ldata()))
            write('</td>\n</tr>\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def sub_platform(self, subch, **KWS):
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
        label = 'Java Platform'
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
            write('<tr>\n<th>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</th>\n<td>')
            write(_filter(subch.pretty_ldata()))
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
    _mainCheetahMethod_for_classdiff_ClassInfoChange = 'writeBody'


if not hasattr(classdiff_ClassInfoChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_ClassInfoChange, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_ClassInfoChange)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(classdiff_ClassInfoChange())).run()
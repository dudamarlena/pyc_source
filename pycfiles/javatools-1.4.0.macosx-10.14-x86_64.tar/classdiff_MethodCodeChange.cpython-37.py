# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/classdiff_MethodCodeChange.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 15754 bytes
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
import javatools.cheetah.change_SuperChange as change_SuperChange
from javatools.classdiff import merge_code
from javatools.opcodes import has_const_arg, get_opname_by_code
import javatools.cheetah as escape
from six.moves import zip_longest
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_MethodCodeChange.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class classdiff_MethodCodeChange(change_SuperChange):

    def __init__(self, *args, **KWs):
        (super(classdiff_MethodCodeChange, self).__init__)(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v

            (self._initCheetahInstance)(**cheetahKWArgs)

    def details_changed(self, **KWS):
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
        write('\n<!-- START BLOCK: details_changed -->\n<table>\n<thead>\n<tr>\n<th>Relative</th>\n<th colspan="4">Original</th>\n<th colspan="4">Modified</th>\n</tr>\n<tr>\n<th>line</th>\n<th>line</th>\n<th>offset</th>\n<th>opcode</th>\n<th>args</th>\n<th>line</th>\n<th>offset</th>\n<th>opcode</th>\n<th>args</th>\n</tr>\n</thead>\n\n')
        change = getattr(self, 'change')
        ldata = change.get_ldata()
        rdata = change.get_rdata()
        merged = merge_code(ldata, rdata)
        write('\n')
        for rel_line, (left, right) in sorted(merged.items()):
            first = True
            last = False
            left_line = None
            left_dis = tuple()
            if left is not None:
                left_line, left_dis = left
            right_line = None
            right_dis = tuple()
            if right is not None:
                right_line, right_dis = right
            rowspan = max(len(left_dis), len(right_dis))
            lastrow = rowspan - min(len(left_dis), len(right_dis))
            write('\n')
            for l_instruction, r_instruction in zip_longest(left_dis, right_dis):
                write('<tr>\n\n')
                if first:
                    write('<td rowspan="')
                    write(_filter(rowspan))
                    write('">')
                    write(_filter(rel_line))
                    write('</td>\n')
                write('\n')
                if l_instruction is not None:
                    if first:
                        write('<td rowspan="')
                        write(_filter(rowspan))
                        write('">')
                        write(_filter(left[0]))
                        write('</td>\n')
                    l_offset, l_code, l_args = l_instruction
                    write('\n<td>')
                    write(_filter(l_offset))
                    write('</td>\n<td>')
                    write(_filter(get_opname_by_code(l_code)))
                    write('</td>\n<td>')
                    write(_filter(has_const_arg(l_code) and '#%s' % l_args[0] or ', '.join(map(str, l_args))))
                    write('</td>\n')
                else:
                    if not last:
                        if first:
                            write('<td colspan="4" rowspan="')
                            write(_filter(lastrow))
                            write('"></td>\n')
                        else:
                            write('<td colspan="3" rowspan="')
                            write(_filter(lastrow))
                            write('"></td>\n')
                        last = True
                        write('\n')
                    write('\n')
                if r_instruction is not None:
                    if first:
                        write('<td rowspan="')
                        write(_filter(rowspan))
                        write('">')
                        write(_filter(right[0]))
                        write('</td>\n')
                    r_offset, r_code, r_args = r_instruction
                    write('\n<td>')
                    write(_filter(r_offset))
                    write('</td>\n<td>')
                    write(_filter(get_opname_by_code(r_code)))
                    write('</td>\n<td>')
                    write(_filter(has_const_arg(r_code) and '#%s' % r_args[0] or ', '.join(map(str, r_args))))
                    write('</td>\n')
                else:
                    if not last:
                        if first:
                            write('<td colspan="4" rowspan="')
                            write(_filter(lastrow))
                            write('"></td>\n')
                        else:
                            write('<td colspan="3" rowspan="')
                            write(_filter(lastrow))
                            write('"></td>\n')
                        last = True
                        write('\n')
                    write('</tr>\n')
                    first = False
                    write('\n')

        write('</table>\n')
        write('\n<!-- END BLOCK: details_changed -->\n')
        return _dummyTrans and trans.response().getvalue() or ''

    def details_unchanged(self, **KWS):
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
        write('\n<!-- START BLOCK: details_unchanged -->\n')
        change = getattr(self, 'change')
        ldata = change.get_ldata()
        write('\n')
        if ldata is None:
            write('<!-- abstract -->\n')
        else:
            write('<table>\n<thead>\n<tr>\n<th>Relative</th>\n<th colspan="4">Method Code</th>\n</tr>\n<tr>\n<th>line</th>\n<th>line</th>\n<th>offset</th>\n<th>opcode</th>\n<th>args</th>\n</tr>\n</thead>\n')
            for abs_line, rel_line, dis in ldata.iter_code_by_lines():
                rowspan = len(dis)
                first = True
                write('\n')
                for offset, code, args in dis:
                    write('<tr>\n')
                    if first:
                        write('<td rowspan="')
                        write(_filter(rowspan))
                        write('">')
                        write(_filter(rel_line))
                        write('</td>\n<td rowspan="')
                        write(_filter(rowspan))
                        write('">')
                        write(_filter(abs_line))
                        write('</td>\n')
                    write('<td>')
                    write(_filter(offset))
                    write('</td>\n<td>')
                    write(_filter(get_opname_by_code(code)))
                    write('</td>\n<td>')
                    write(_filter(has_const_arg(code) and '#%s' % args[0] or ', '.join(map(str, args))))
                    write('</td>\n</tr>\n')
                    first = False
                    write('\n')

            write('</table>\n')
        write('\n<!-- END BLOCK: details_unchanged -->\n')
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
        change = getattr(self, 'change')
        lcode = change.ldata and change.ldata.code or tuple()
        rcode = change.rdata and change.rdata.code or tuple()
        write('\n')
        if change.is_change() or lcode != rcode:
            _v = VFFSL(SL, 'details_changed', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$details_changed'))
            write('\n')
        else:
            _v = VFFSL(SL, 'details_unchanged', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$details_unchanged'))
            write('\n')
        write('</div>\n</div>\n')
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
        self.details_changed(trans=trans)
        write('\n\n\n')
        self.details_unchanged(trans=trans)
        write('\n\n\n')
        self.details(trans=trans)
        write('\n\n\n')
        self.collect(trans=trans)
        write('\n\n\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_classdiff_MethodCodeChange = 'writeBody'


if not hasattr(classdiff_MethodCodeChange, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_MethodCodeChange, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_MethodCodeChange)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(classdiff_MethodCodeChange())).run()
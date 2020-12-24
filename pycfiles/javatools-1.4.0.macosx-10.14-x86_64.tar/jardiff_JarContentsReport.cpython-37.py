# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/cheetah/jardiff_JarContentsReport.py
# Compiled at: 2019-07-05 15:01:15
# Size of source mod 2**32: 9088 bytes
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
VFFSL = valueFromFrameOrSearchList
VFSL = valueFromSearchList
VFN = valueForName
currentTime = time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/jardiff_JarContentsReport.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'
if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError('This template was compiled with Cheetah version %s. Templates compiled before version %s must be recompiled.' % (
     __CHEETAH_version__, RequiredCheetahVersion))

class jardiff_JarContentsReport(Template):

    def __init__(self, *args, **KWs):
        (super(jardiff_JarContentsReport, self).__init__)(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k, v in KWs.items():
                if k in allowedKWs:
                    cheetahKWArgs[k] = v

            (self._initCheetahInstance)(**cheetahKWArgs)

    def render_by_class(self, changes, label, **KWS):
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
        if changes:
            write('\n<div class="change-category">\n<h2>')
            _v = VFFSL(SL, 'label', True)
            if _v is not None:
                write(_filter(_v, rawExpr='$label'))
            write('</h2>\n\n')
            chm = dict(((ch.entry, ch) for ch in changes))
            write('\n\n')
            for entry in sorted(chm.keys()):
                _v = VFFSL(SL, 'render_change', False)(chm[entry])
                if _v is not None:
                    write(_filter(_v, rawExpr='$render_change(chm[entry])'))
                write('\n')

            write('\n</div>\n')
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
        write('\n<!-- START BLOCK: details -->\n<!-- begin jardiff_JarContentsReport.details -->\n<div class="details">\n\n')
        import javatools.jardiff, javatools.change
        change = getattr(self, 'change')
        changemap = javatools.change.collect_by_type(change.collect())
        changeorder = (
         javatools.jardiff.JarManifestChange,
         javatools.jardiff.JarSignatureFileAdded,
         javatools.jardiff.JarSignatureFileRemoved,
         javatools.jardiff.JarSignatureFileChange,
         javatools.jardiff.JarSignatureBlockFileAdded,
         javatools.jardiff.JarSignatureBlockFileRemoved,
         javatools.jardiff.JarSignatureBlockFileChange,
         javatools.jardiff.JarContentAdded,
         javatools.jardiff.JarContentRemoved,
         javatools.jardiff.JarContentChange,
         javatools.jardiff.JarClassAdded,
         javatools.jardiff.JarClassRemoved,
         javatools.jardiff.JarClassChange)
        for sq in changemap.pop(javatools.change.SquashedChange, ()):
            oc = sq.origclass
            if oc is javatools.jardiff.JarClassReport:
                oc = javatools.jardiff.JarClassChange
            sqm = changemap.setdefault(oc, [])
            sqm.append(sq)

        write('\n\n')
        for ct in changeorder:
            _v = VFFSL(SL, 'render_by_class', False)(changemap.pop(ct, ()), ct.label)
            if _v is not None:
                write(_filter(_v, rawExpr='$render_by_class(changemap.pop(ct, ()), ct.label)'))
            write('\n')

        write('\n')
        for ct, changes in changemap.items():
            _v = VFFSL(SL, 'render_by_class', False)(changes, ct.label)
            if _v is not None:
                write(_filter(_v, rawExpr='$render_by_class(changes, ct.label)'))
            write('\n')

        write('\n</div>\n<!-- end jardiff_JarContentsReport.details -->\n')
        write('\n<!-- END BLOCK: details -->\n')
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
        self.details(trans=trans)
        write('\n\n')
        return _dummyTrans and trans.response().getvalue() or ''

    _CHEETAH__instanceInitialized = False
    _CHEETAH_version = __CHEETAH_version__
    _CHEETAH_versionTuple = __CHEETAH_versionTuple__
    _CHEETAH_src = __CHEETAH_src__
    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__
    _mainCheetahMethod_for_jardiff_JarContentsReport = 'respond'


if not hasattr(jardiff_JarContentsReport, '_initCheetahAttributes'):
    templateAPIClass = getattr(jardiff_JarContentsReport, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(jardiff_JarContentsReport)
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=(jardiff_JarContentsReport())).run()
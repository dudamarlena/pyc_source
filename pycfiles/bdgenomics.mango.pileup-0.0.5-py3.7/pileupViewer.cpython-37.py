# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/pileup/pileupViewer.py
# Compiled at: 2019-09-22 14:31:46
# Size of source mod 2**32: 1837 bytes
"""
============
PileupViewer
============
.. currentmodule:: bdgenomics.mango.pileup.pileupViewer
.. autosummary::
   :toctree: _generate/

   PileupViewer
"""
import ipywidgets as widgets
from traitlets import Unicode, Int, List
from .track import Track, track_list_serialization

@widgets.register('bdgenomics.mango.pileup.PileupViewer')
class PileupViewer(widgets.DOMWidget):
    __doc__ = ' Widget wrapper for pileup.js viewer in Jupyter notebooks.\n    '
    _view_name = Unicode('PileupViewerView').tag(sync=True)
    _model_name = Unicode('PileupViewerModel').tag(sync=True)
    _view_module = Unicode('pileup').tag(sync=True)
    _model_module = Unicode('pileup').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    locus = Unicode('chr1:1-50').tag(sync=True)
    reference = Unicode('hg19').tag(sync=True)
    tracks = (List(Track()).tag)(sync=True, **track_list_serialization)
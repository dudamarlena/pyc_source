# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/models/lines/calculated_line.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1660 bytes
import logging
from mvc.models.properties.tools import modify
logger = logging.getLogger(__name__)
from mvc.models.properties import ListProperty, SignalMixin
from pyxrd.data import settings
from pyxrd.generic.io import storables
from pyxrd.generic.models.base import DataModel
from .pyxrd_line import PyXRDLine

@storables.register()
class CalculatedLine(PyXRDLine):

    class Meta(PyXRDLine.Meta):
        store_id = 'CalculatedLine'
        inherit_format = 'display_calc_%s'

    specimen = property(DataModel.parent.fget, DataModel.parent.fset)
    phase_colors = ListProperty(default=[], test='Phase colors', mix_with=(
     SignalMixin,),
      signal_name='visuals_changed')
    color = modify((PyXRDLine.color), default=(settings.CALCULATED_COLOR),
      inherit_from='parent.parent.display_calc_color')
    lw = modify((PyXRDLine.lw), default=(settings.CALCULATED_LINEWIDTH),
      inherit_from='parent.parent.display_calc_lw')
    ls = modify((PyXRDLine.ls), default=(settings.CALCULATED_LINESTYLE),
      inherit_from='parent.parent.display_calc_ls')
    marker = modify((PyXRDLine.marker), default=(settings.CALCULATED_MARKER),
      inherit_from='parent.parent.display_calc_marker')
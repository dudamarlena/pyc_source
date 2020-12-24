# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/extra_guiqwt/styles.py
# Compiled at: 2019-08-19 15:09:29
"""Extension of :mod:`guiqwt.styles`"""
__docformat__ = 'restructuredtext'
from guidata.dataset.datatypes import DataSet
from guidata.dataset.dataitems import StringItem, IntItem, ChoiceItem, BoolItem

class TaurusCurveParam(DataSet):
    xModel = StringItem('Model for X', default='')
    yModel = StringItem('Model for Y', default='')

    def update_param(self, curve):
        self.xModel.update_param(curve.taurusparam.xModel)
        self.yModel.update_param(curve.taurusparam.yModel)

    def update_curve(self, curve):
        curve.setModels(self.xModel or None, self.yModel)
        return


class TaurusTrendParam(DataSet):
    model = StringItem('Model', default='')
    maxBufferSize = IntItem('Buffer Size', default=16384)
    useArchiving = BoolItem('Use Archiving', default=False)
    stackMode = ChoiceItem('Stack Mode', [
     ('datetime', 'Absolute Time'),
     ('timedelta', 'Relative Time'),
     ('event', 'Event')], default='datetime')

    def update_param(self, curve):
        self.model.update_param(curve.taurusparam.model)
        self.maxBufferSize.update_param(curve.taurusparam.maxBufferSize)
        self.stackMode.update_param(curve.taurusparam.stackMode)

    def update_curve(self, curve):
        curve.setModel(self.model)
        curve.setBufferSize(self.maxBufferSize)
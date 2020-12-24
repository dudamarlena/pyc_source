# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/chart/simple_plot.py
# Compiled at: 2013-04-11 17:47:52
from camelot.admin.object_admin import ObjectAdmin
from camelot.view.controls import delegates
from camelot.container.chartcontainer import PlotContainer

class Wave(object):

    def __init__(self):
        self.amplitude = 1
        self.phase = 0

    @property
    def chart(self):
        import math
        x_data = [ x / 100.0 for x in range(1, 700, 1) ]
        y_data = [ self.amplitude * math.sin(x - self.phase) for x in x_data ]
        return PlotContainer(x_data, y_data)

    class Admin(ObjectAdmin):
        form_display = [
         'amplitude', 'phase', 'chart']
        field_attributes = dict(amplitude=dict(delegate=delegates.FloatDelegate, editable=True), phase=dict(delegate=delegates.FloatDelegate, editable=True), chart=dict(delegate=delegates.ChartDelegate))
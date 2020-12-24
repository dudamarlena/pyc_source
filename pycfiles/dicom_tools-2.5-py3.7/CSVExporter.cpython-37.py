# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/exporters/CSVExporter.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2798 bytes
from ..Qt import QtGui, QtCore
from .Exporter import Exporter
from ..parametertree import Parameter
from .. import PlotItem
__all__ = ['CSVExporter']

class CSVExporter(Exporter):
    Name = 'CSV from plot data'
    windows = []

    def __init__(self, item):
        Exporter.__init__(self, item)
        self.params = Parameter(name='params', type='group', children=[
         {'name':'separator', 
          'type':'list',  'value':'comma',  'values':['comma', 'tab']},
         {'name':'precision', 
          'type':'int',  'value':10,  'limits':[0, None]},
         {'name':'columnMode', 
          'type':'list',  'values':['(x,y) per plot', '(x,y,y,y) for all plots']}])

    def parameters(self):
        return self.params

    def export(self, fileName=None):
        if not isinstance(self.item, PlotItem):
            raise Exception('Must have a PlotItem selected for CSV export.')
        elif fileName is None:
            self.fileSaveDialog(filter=['*.csv', '*.tsv'])
            return
            fd = open(fileName, 'w')
            data = []
            header = []
            appendAllX = self.params['columnMode'] == '(x,y) per plot'
            for i, c in enumerate(self.item.curves):
                cd = c.getData()
                if cd[0] is None:
                    continue
                data.append(cd)
                if hasattr(c, 'implements'):
                    if c.implements('plotData') and c.name() is not None:
                        name = c.name().replace('"', '""') + '_'
                        xName, yName = '"' + name + 'x"', '"' + name + 'y"'
                    else:
                        xName = 'x%04d' % i
                        yName = 'y%04d' % i
                    if appendAllX or i == 0:
                        header.extend([xName, yName])
                else:
                    header.extend([yName])

            if self.params['separator'] == 'comma':
                sep = ','
        else:
            sep = '\t'
        fd.write(sep.join(header) + '\n')
        i = 0
        numFormat = '%%0.%dg' % self.params['precision']
        numRows = max([len(d[0]) for d in data])
        for i in range(numRows):
            for j, d in enumerate(data):
                if not appendAllX:
                    if j == 0:
                        if d is not None and i < len(d[0]):
                            fd.write(numFormat % d[0][i] + sep)
                        else:
                            fd.write(' %s' % sep)
                    if d is not None:
                        if i < len(d[1]):
                            fd.write(numFormat % d[1][i] + sep)
                    fd.write(' %s' % sep)

            fd.write('\n')

        fd.close()


CSVExporter.register()
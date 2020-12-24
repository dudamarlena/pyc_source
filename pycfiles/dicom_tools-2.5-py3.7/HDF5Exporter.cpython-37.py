# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/exporters/HDF5Exporter.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1813 bytes
from ..Qt import QtGui, QtCore
from .Exporter import Exporter
from ..parametertree import Parameter
from .. import PlotItem
import numpy
try:
    import h5py
    HAVE_HDF5 = True
except ImportError:
    HAVE_HDF5 = False

__all__ = ['HDF5Exporter']

class HDF5Exporter(Exporter):
    Name = 'HDF5 Export: plot (x,y)'
    windows = []
    allowCopy = False

    def __init__(self, item):
        Exporter.__init__(self, item)
        self.params = Parameter(name='params', type='group', children=[
         {'name':'Name', 
          'type':'str',  'value':'Export'},
         {'name':'columnMode', 
          'type':'list',  'values':['(x,y) per plot', '(x,y,y,y) for all plots']}])

    def parameters(self):
        return self.params

    def export(self, fileName=None):
        if not HAVE_HDF5:
            raise RuntimeError('This exporter requires the h5py package, but it was not importable.')
        if not isinstance(self.item, PlotItem):
            raise Exception('Must have a PlotItem selected for HDF5 export.')
        if fileName is None:
            self.fileSaveDialog(filter=['*.h5', '*.hdf', '*.hd5'])
            return
        dsname = self.params['Name']
        fd = h5py.File(fileName, 'a')
        data = []
        appendAllX = self.params['columnMode'] == '(x,y) per plot'
        for i, c in enumerate(self.item.curves):
            d = c.getData()
            if not appendAllX:
                if i == 0:
                    data.append(d[0])
                data.append(d[1])

        fdata = numpy.array(data).astype('double')
        dset = fd.create_dataset(dsname, data=fdata)
        fd.close()


if HAVE_HDF5:
    HDF5Exporter.register()
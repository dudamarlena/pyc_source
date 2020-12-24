# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alex/dev/dummydata/dummydata/model2.py
# Compiled at: 2017-03-16 09:39:03
# Size of source mod 2**32: 1448 bytes
from .dummydata import DummyData

class Model2(DummyData):
    __doc__ = '\n    Dummydata that mimic Model data with two spatial dimensions\n    '

    def __init__(self, var='ta', oname='DummyM2.nc', **kwargs):
        """
        create an empty 3D file

        Parameters
        ----------
        month : int
            number of months
        var : str
            variable name to specify
        """
        (super(Model2, self).__init__)(oname, **kwargs)
        self.var = var
        self.createM2Dimension()
        self.createM2Variable()
        self.addM2Data()
        self.add_ancillary_data()
        self.close()

    def createM2Dimension(self):
        self._create_time_dimension()
        self._create_coordinate_dimensions()
        self._create_bnds_dimensions()

    def createM2Variable(self):
        self._create_time_variable()
        self._create_coordinates()
        self.createVariable((self.var),
          'f4',
          ('time', 'lat', 'lon'),
          fill_value=1e+20)
        self._set_variable_metadata()
        self._set_metadata()

    def addM2Data(self):
        self.variables[self.var][0:self.month, :, :] = self._get_variable_data()
        self._set_coordinate_data()
        self._set_time_data()
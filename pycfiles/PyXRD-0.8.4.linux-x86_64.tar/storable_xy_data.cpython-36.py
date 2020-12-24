# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/models/lines/storable_xy_data.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 4186 bytes
import logging
logger = logging.getLogger(__name__)
import numpy as np
from mvc.models.xydata import XYData
from pyxrd.generic.io import storables, Storable
from pyxrd.generic.models.base import DataModel
from pyxrd.generic.utils import not_none

@storables.register()
class StorableXYData(DataModel, XYData, Storable):
    __doc__ = '\n        A storable XYData model with additional I/O and CRUD abilities.\n    '

    class Meta(XYData.Meta):
        store_id = 'StorableXYData'

    def __init__(self, *args, **kwargs):
        if 'xy_store' in kwargs:
            kwargs['data'] = kwargs.pop('xy_store')
        (super(StorableXYData, self).__init__)(*args, **kwargs)

    def json_properties(self):
        props = super(XYData, self).json_properties()
        props['data'] = self._serialize_data()
        return props

    def apply_correction(self, correction):
        self.data_y = self.data_y * correction[:, np.newaxis]

    def save_data(self, parser, filename, **kwargs):
        if self.data_y.shape[1] > 1:
            kwargs['header'] = [
             '2θ'] + not_none(self.y_names, [])
        (parser.write)(filename, (self.data_x), (self._data_y.transpose()), **kwargs)

    def load_data(self, parser, filename, clear=True):
        """
            Loads data using passed filename and parser, which are passed on to
            the load_data_from_generator method.
            If clear=True the x-y data is cleared first.
        """
        xrdfiles = parser.parse(filename)
        if xrdfiles:
            self.load_data_from_generator((xrdfiles[0].data), clear=clear)

    def load_data_from_generator(self, generator, clear=True):
        with self.data_changed.hold_and_emit():
            with self.visuals_changed.hold_and_emit():
                super(StorableXYData, self).load_data_from_generator(generator, clear=clear)

    def set_data(self, x, y):
        with self.data_changed.hold_and_emit():
            with self.visuals_changed.hold_and_emit():
                super(StorableXYData, self).set_data(x, y)

    def set_value(self, i, j, value):
        with self.data_changed.hold_and_emit():
            with self.visuals_changed.hold_and_emit():
                super(StorableXYData, self).set_value(i, j, value)

    def append(self, x, y):
        with self.data_changed.hold_and_emit():
            with self.visuals_changed.hold_and_emit():
                super(StorableXYData, self).append(x, y)

    def insert(self, pos, x, y):
        with self.data_changed.hold_and_emit():
            with self.visuals_changed.hold_and_emit():
                super(StorableXYData, self).insert(pos, x, y)

    def remove_from_indeces(self, *indeces):
        with self.data_changed.hold_and_emit():
            with self.visuals_changed.hold_and_emit():
                (super(StorableXYData, self).remove_from_indeces)(*indeces)
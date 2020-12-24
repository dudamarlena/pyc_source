# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/container.py
# Compiled at: 2019-12-09 07:12:30
# Size of source mod 2**32: 2440 bytes
import json
import getml.communication as comm

class Container(object):
    __doc__ = '\n    Base object not meant to be called directly\n    '

    def __init__(self):
        self.colnames = None
        self.units = None
        self.thisptr = dict()

    def send(self, numpy_array, s):
        """
        Sends the object to the engine, data taken from a numpy array.

        Args:
            numpy_array (:class:`numpy.ndarray`): Number of columns should match the number of columns of the object itself.
            s: Socket
        """
        comm.send_string(s, json.dumps(self.thisptr))
        if self.thisptr['type_'] == 'CategoricalColumn':
            comm.send_categorical_matrix(s, numpy_array)
        else:
            if self.thisptr['type_'] == 'Column':
                comm.send_matrix(s, numpy_array)
        msg = comm.recv_string(s)
        if msg != 'Success!':
            raise Exception(msg)
        if len(numpy_array.shape) > 1:
            self.colnames = self.colnames or ['column_' + str(i + 1) for i in range(numpy_array.shape[1])]

    def set_unit(self, unit):
        """
        Sets the unit of the column.

        Args:
            unit: The new unit.
        """
        cmd = dict()
        cmd.update(self.thisptr)
        cmd['unit_'] = unit
        cmd['type_'] += '.set_unit'
        comm.send(cmd)
        self.thisptr['unit_'] = unit
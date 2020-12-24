# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/trane/ops/transformation_ops.py
# Compiled at: 2018-04-05 20:01:41
# Size of source mod 2**32: 2781 bytes
from ..utils.table_meta import TableMeta as TM
from .op_base import OpBase
import numpy, logging
TRANSFORMATION_OPS = [
 'IdentityTransformationOp',
 'DiffTransformationOp', 'ObjectFrequencyTransformationOp']
__all__ = ['TransformationOpBase', 'TRANSFORMATION_OPS'] + TRANSFORMATION_OPS

class TransformationOpBase(OpBase):
    __doc__ = 'super class for all Transformation Operations. (deprecated)'


class IdentityTransformationOp(TransformationOpBase):
    REQUIRED_PARAMETERS = []
    IOTYPES = [
     (
      TM.TYPE_CATEGORY, TM.TYPE_CATEGORY), (TM.TYPE_BOOL, TM.TYPE_BOOL),
     (
      TM.TYPE_ORDERED, TM.TYPE_ORDERED), (TM.TYPE_TEXT, TM.TYPE_TEXT),
     (
      TM.TYPE_INTEGER, TM.TYPE_INTEGER), (TM.TYPE_FLOAT, TM.TYPE_FLOAT),
     (
      TM.TYPE_TIME, TM.TYPE_TIME), (TM.TYPE_IDENTIFIER, TM.TYPE_IDENTIFIER)]

    def execute(self, dataframe):
        return dataframe


class DiffTransformationOp(TransformationOpBase):
    REQUIRED_PARAMETERS = []
    IOTYPES = [
     (
      TM.TYPE_FLOAT, TM.TYPE_FLOAT),
     (
      TM.TYPE_INTEGER, TM.TYPE_INTEGER)]

    def execute(self, dataframe):
        dataframe = dataframe.copy()
        index = dataframe.index
        for i in range(len(index) - 1, 0, -1):
            dataframe.at[(index[i], self.column_name)] -= float(dataframe.at[(
             index[(i - 1)], self.column_name)].astype(numpy.float32))

        dataframe.at[(index[0], self.column_name)] = 0
        return dataframe


class ObjectFrequencyTransformationOp(TransformationOpBase):
    REQUIRED_PARAMETERS = []
    IOTYPES = [
     (
      TM.TYPE_CATEGORY, TM.TYPE_INTEGER), (TM.TYPE_BOOL, TM.TYPE_INTEGER),
     (
      TM.TYPE_ORDERED, TM.TYPE_INTEGER), (TM.TYPE_TEXT, TM.TYPE_INTEGER),
     (
      TM.TYPE_INTEGER, TM.TYPE_INTEGER), (TM.TYPE_FLOAT, TM.TYPE_INTEGER),
     (
      TM.TYPE_TIME, TM.TYPE_INTEGER), (TM.TYPE_IDENTIFIER, TM.TYPE_INTEGER)]

    def execute(self, dataframe):
        dataframe = dataframe.copy()
        objects = dataframe.copy()[self.column_name].unique()
        objects_to_frequency = {}
        for obj in objects:
            objects_to_frequency[obj] = 0

        for val in dataframe[self.column_name]:
            objects_to_frequency[val] = objects_to_frequency[val] + 1

        for idx, obj in enumerate(objects):
            dataframe.at[(idx, self.column_name)] = objects_to_frequency[obj]

        dataframe[self.column_name] = dataframe[self.column_name].astype(int)
        num_rows_to_drop = len(dataframe) - len(objects_to_frequency)
        assert num_rows_to_drop >= 0
        if num_rows_to_drop == 0:
            return dataframe
        return dataframe[:-num_rows_to_drop]
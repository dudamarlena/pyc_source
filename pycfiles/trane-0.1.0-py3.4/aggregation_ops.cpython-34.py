# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/trane/ops/aggregation_ops.py
# Compiled at: 2018-04-05 20:01:41
# Size of source mod 2**32: 3016 bytes
from ..utils.table_meta import TableMeta as TM
from .op_base import OpBase
import sys, numpy
AGGREGATION_OPS = [
 'FirstAggregationOp', 'CountAggregationOp', 'SumAggregationOp',
 'LastAggregationOp', 'LMFAggregationOp']
__all__ = ['AggregationOpBase', 'AGGREGATION_OPS'] + AGGREGATION_OPS
import logging

class AggregationOpBase(OpBase):
    __doc__ = 'super class for all Aggregation Operations. (deprecated)'


class FirstAggregationOp(AggregationOpBase):
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
        dataframe = dataframe.copy()
        return dataframe.head(1)


class LastAggregationOp(AggregationOpBase):
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
        dataframe = dataframe.copy()
        return dataframe.tail(1)


class LMFAggregationOp(AggregationOpBase):
    REQUIRED_PARAMETERS = []
    IOTYPES = [
     (
      TM.TYPE_FLOAT, TM.TYPE_FLOAT),
     (
      TM.TYPE_INTEGER, TM.TYPE_FLOAT)]

    def execute(self, dataframe):
        dataframe = dataframe.copy()
        dataframe[self.column_name] = dataframe[self.column_name].astype(numpy.float32)
        last = dataframe.tail(1)
        first = dataframe.head(1)
        last.at[(last.index[0],
         self.column_name)] -= first.at[(first.index[0], self.column_name)]
        return last


class CountAggregationOp(AggregationOpBase):
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
        head = dataframe.head(1)
        head[self.column_name] = int(dataframe.shape[0])
        return head


class SumAggregationOp(AggregationOpBase):
    REQUIRED_PARAMETERS = []
    IOTYPES = [
     (
      TM.TYPE_FLOAT, TM.TYPE_FLOAT), (TM.TYPE_BOOL, TM.TYPE_FLOAT),
     (
      TM.TYPE_INTEGER, TM.TYPE_FLOAT)]

    def execute(self, dataframe):
        dataframe = dataframe.copy()
        head = dataframe.head(1)
        head[self.column_name] = float(dataframe[self.column_name].sum())
        return head
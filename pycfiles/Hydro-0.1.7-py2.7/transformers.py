# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/transformers.py
# Compiled at: 2016-03-22 10:29:20
__author__ = 'moshebasanchig'
from base_classes import Base
import pandas as pd

class Transformers(Base):

    def __init__(self):
        self._execution_plan = None
        return

    def combine(self, stream1, stream2, left_on=None, right_on=None, how='inner', suffixes=('_x', '_y')):
        """
        takes two input streams (pandas data frames) and joins them based on the keys dictionary
        """
        if self._execution_plan:
            self._execution_plan.append('combine', 'transform')
        if left_on and right_on:
            return pd.merge(stream1, stream2, left_on=left_on, right_on=right_on, how=how, suffixes=suffixes)
        else:
            return
            return

    def aggregate(self, stream, group_by=None, operators=None):
        """
        takes an input stream (pandas data frame) and perform a group-by + aggregation.
        for instance: aggregate(data, group_by=['col1'], operators={'col2': 'sum'})
        """
        if self._execution_plan:
            self._execution_plan.append('aggregate', 'transform')
        if group_by and operators:
            return stream.groupby(group_by).agg(operators)
        else:
            return
            return

    def concat(self, streams):
        """
        takes two input streams (pandas data frames) and concats them, assuming they have the same structure
        :param streams: iterable of streams to concat
        :return: a single stream
        """
        if self._execution_plan:
            self._execution_plan.append('concat', 'transform')
        return pd.concat(streams)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/data_sink.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 1876 bytes
from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection
from awsglue.utils import makeOptions, callsite

class DataSink(object):

    def __init__(self, j_sink, sql_ctx):
        self._jsink = j_sink
        self._sql_ctx = sql_ctx

    def setFormat(self, format, **options):
        self._jsink.setFormat(format, makeOptions(self._sql_ctx._sc, options))

    def setAccumulableSize(self, size):
        self._jsink.setAccumulableSize(size)

    def writeFrame(self, dynamic_frame, info=''):
        return DynamicFrame(self._jsink.pyWriteDynamicFrame(dynamic_frame._jdf, callsite(), info), dynamic_frame.glue_ctx, dynamic_frame.name + '_errors')

    def write(self, dynamic_frame_or_dfc, info=''):
        if isinstance(dynamic_frame_or_dfc, DynamicFrame):
            return self.writeFrame(dynamic_frame_or_dfc, info)
        if isinstance(dynamic_frame_or_dfc, DynamicFrameCollection):
            res_frames = [self.writeFrame(frame) for frame in dynamic_frame_or_dfc.values()]
            return DynamicFrameCollection(res_frames, self._sql_ctx)
        raise TypeError('dynamic_frame_or_dfc must be an instance ofDynamicFrame or DynamicFrameCollection. Got ' + str(type(dynamic_frame_or_dfc)))
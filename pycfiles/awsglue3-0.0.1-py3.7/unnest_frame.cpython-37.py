# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/transforms/unnest_frame.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 3248 bytes
from awsglue.transforms import GlueTransform

class UnnestFrame(GlueTransform):
    __doc__ = '\n    unnest a dynamic frame. i.e. flattens nested objects to top level elements.\n    It also generates joinkeys for array objects\n    '

    def __call__(self, frame, transformation_ctx='', info='', stageThreshold=0, totalThreshold=0):
        """
        unnest a dynamic frame. i.e. flattens nested objects to top level elements.
        It also generates joinkeys for array objects
        :param frame: DynamicFrame, the dynamicframe to unnest
        :param info: String, any string to be associated with errors in this transformation.
        :param stageThreshold: Long, number of errors in the given transformation for which the processing needs to error out.
        :param totalThreshold: Long, total number of errors upto and including in this transformation
          for which the processing needs to error out.
        :return: a new unnested dynamic frame
        """
        return frame.unnest(transformation_ctx, info, stageThreshold, totalThreshold)

    @classmethod
    def describeArgs(cls):
        arg1 = {'name':'frame',  'type':'DynamicFrame', 
         'description':'The DynamicFrame to unnest', 
         'optional':False, 
         'defaultValue':None}
        arg2 = {'name':'transformation_ctx',  'type':'String', 
         'description':'A unique string that is used to identify stats / state information', 
         'optional':True, 
         'defaultValue':''}
        arg3 = {'name':'info',  'type':'String', 
         'description':'Any string to be associated with errors in the transformation', 
         'optional':True, 
         'defaultValue':'""'}
        arg4 = {'name':'stageThreshold',  'type':'Integer', 
         'description':'Max number of errors in the transformation until processing will error out', 
         'optional':True, 
         'defaultValue':'0'}
        arg5 = {'name':'totalThreshold',  'type':'Integer', 
         'description':'Max number of errors total until processing will error out.', 
         'optional':True, 
         'defaultValue':'0'}
        return [
         arg1, arg2, arg3, arg4, arg5]

    @classmethod
    def describeTransform(cls):
        return 'unnest a dynamic frame. i.e. flatten nested objects to top level elements.'

    @classmethod
    def describeErrors(cls):
        return []

    @classmethod
    def describeReturn(cls):
        return {'type':'DynamicFrame',  'description':'new unnested DynamicFrame'}
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/transforms/dynamicframe_filter.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 2831 bytes
from transform import GlueTransform

class Filter(GlueTransform):

    def __call__(self, frame, f, transformation_ctx='', info='', stageThreshold=0, totalThreshold=0):
        return frame.filter(f, transformation_ctx, info, stageThreshold, totalThreshold)

    @classmethod
    def describeArgs(cls):
        arg1 = {'name':'frame',  'type':'DynamicFrame', 
         'description':'The DynamicFrame to apply the Filter function', 
         'optional':False, 
         'defaultValue':None}
        arg2 = {'name':'f',  'type':'Function', 
         'description':'Predicate function to call on the DynamicFrame. The function takes DynamicRecord as the argument and returns True/False', 
         'optional':False, 
         'defaultValue':None}
        arg3 = {'name':'transformation_ctx',  'type':'String', 
         'description':'A unique string that is used to identify stats / state information', 
         'optional':True, 
         'defaultValue':''}
        arg4 = {'name':'info',  'type':'String', 
         'description':'Any string to be associated with errors in the transformation', 
         'optional':True, 
         'defaultValue':'""'}
        arg5 = {'name':'stageThreshold',  'type':'Integer', 
         'description':'Max number of errors in the transformation until processing will error out', 
         'optional':True, 
         'defaultValue':'0'}
        arg6 = {'name':'totalThreshold',  'type':'Integer', 
         'description':'Max number of errors total until processing will error out.', 
         'optional':True, 
         'defaultValue':'0'}
        return [
         arg1, arg2, arg3, arg4, arg5, arg6]

    @classmethod
    def describeTransform(cls):
        return 'Builds a new DynamicFrame by selecting records from the input frame that satisfy the predicate function'

    @classmethod
    def describeErrors(cls):
        return []

    @classmethod
    def describeReturn(cls):
        return {'type':'DynamicFrame',  'description':'new DynamicFrame with DynamicRecords that matched the predicate'}
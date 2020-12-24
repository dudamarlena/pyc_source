# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/transforms/apply_mapping.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 2950 bytes
from awsglue.transforms import DropFields, GlueTransform

class ApplyMapping(GlueTransform):

    def __call__(self, frame, mappings, case_sensitive=False, transformation_ctx='', info='', stageThreshold=0, totalThreshold=0):
        return frame.apply_mapping(mappings, case_sensitive)

    @classmethod
    def describeArgs(cls):
        arg1 = {'name':'frame',  'type':'DynamicFrame', 
         'description':'DynamicFrame to transform', 
         'optional':False, 
         'defaultValue':None}
        arg2 = {'name':'mappings',  'type':'DynamicFrame', 
         'description':'List of mapping tuples (source col, source type, target col, target type)', 
         'optional':False, 
         'defaultValue':None}
        arg3 = {'name':'case_sensitive',  'type':'Boolean', 
         'description':'Whether ', 
         'optional':True, 
         'defaultValue':'False'}
        arg4 = {'name':'transformation_ctx',  'type':'String', 
         'description':'A unique string that is used to identify stats / state information', 
         'optional':True, 
         'defaultValue':''}
        arg5 = {'name':'info',  'type':'String', 
         'description':'Any string to be associated with errors in the transformation', 
         'optional':True, 
         'defaultValue':'""'}
        arg6 = {'name':'stageThreshold',  'type':'Integer', 
         'description':'Max number of errors in the transformation until processing will error out', 
         'optional':True, 
         'defaultValue':'0'}
        arg7 = {'name':'totalThreshold',  'type':'Integer', 
         'description':'Max number of errors total until processing will error out.', 
         'optional':True, 
         'defaultValue':'0'}
        return [
         arg1, arg2, arg3, arg4, arg5, arg6, arg7]

    @classmethod
    def describeTransform(cls):
        return 'Apply a declarative mapping to this DynamicFrame.'

    @classmethod
    def describeErrors(cls):
        return []

    @classmethod
    def describeReturn(cls):
        return {'type':'DynamicFrame',  'description':'DynamicFrame after applying mappings.'}
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/transforms/resolve_choice.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 3367 bytes
from awsglue.transforms import GlueTransform

class ResolveChoice(GlueTransform):

    def __call__(self, frame, specs=None, choice='', database=None, table_name=None, transformation_ctx='', info='', stageThreshold=0, totalThreshold=0):
        return frame.resolveChoice(specs, choice, database, table_name)

    @classmethod
    def describeArgs(cls):
        arg1 = {'name':'frame',  'type':'DynamicFrame', 
         'description':'DynamicFrame to transform', 
         'optional':False, 
         'defaultValue':None}
        arg2 = {'name':'specs',  'type':'List', 
         'description':'List of specs (path, action)', 
         'optional':True, 
         'defaultValue':None}
        arg3 = {'name':'choice',  'type':'String', 
         'description':'resolve choice option', 
         'optional':True, 
         'defaultValue':''}
        arg4 = {'name':'database',  'type':'String', 
         'description':'Glue catalog database name, required for MATCH_CATALOG choice', 
         'optional':True, 
         'defaultValue':''}
        arg5 = {'name':'table_name',  'type':'String', 
         'description':'Glue catalog table name, required for MATCH_CATALOG choice', 
         'optional':True, 
         'defaultValue':''}
        arg6 = {'name':'transformation_ctx',  'type':'String', 
         'description':'A unique string that is used to identify stats / state information', 
         'optional':True, 
         'defaultValue':''}
        arg7 = {'name':'info',  'type':'String', 
         'description':'Any string to be associated with errors in the transformation', 
         'optional':True, 
         'defaultValue':'""'}
        arg8 = {'name':'stageThreshold',  'type':'Integer', 
         'description':'Max number of errors in the transformation until processing will error out', 
         'optional':True, 
         'defaultValue':'0'}
        arg9 = {'name':'totalThreshold',  'type':'Integer', 
         'description':'Max number of errors total until processing will error out.', 
         'optional':True, 
         'defaultValue':'0'}
        return [
         arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9]

    @classmethod
    def describeTransform(cls):
        return 'Resolve choice type in this DynamicFrame.'

    @classmethod
    def describeErrors(cls):
        return []

    @classmethod
    def describeReturn(cls):
        return {'type':'DynamicFrame',  'description':'DynamicFrame after resolving choice type.'}
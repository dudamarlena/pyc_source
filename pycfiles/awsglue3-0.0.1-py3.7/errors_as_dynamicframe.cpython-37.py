# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/transforms/errors_as_dynamicframe.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 1557 bytes
from transform import GlueTransform

class ErrorsAsDynamicFrame(GlueTransform):

    def __call__(self, frame):
        """
        Returns a DynamicFrame which has error records leading up to the source DynmaicFrame, nested in the returned DynamicFrame.

        :param frame: Source dynamicFrame
        """
        return frame.errorsAsDynamicFrame()

    @classmethod
    def describeArgs(cls):
        arg1 = {'name':'frame',  'type':'DynamicFrame', 
         'description':'The DynamicFrame on which to call errorsAsDynamicFrame', 
         'optional':False, 
         'defaultValue':None}
        return [arg1]

    @classmethod
    def describeTransform(cls):
        return 'Get error records leading up to the source DynmaicFrame'

    @classmethod
    def describeErrors(cls):
        return []

    @classmethod
    def describeReturn(cls):
        return {'type':'DynamicFrame',  'description':'new DynamicFrame with error DynamicRecords'}
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/associate/lbd_func_event_map.py
# Compiled at: 2020-02-12 21:45:54
# Size of source mod 2**32: 2415 bytes
from troposphere_mate import Ref, GetAtt
from troposphere_mate import awslambda, sqs, kinesis, dynamodb
from ..core.associate_linker import Linker, x_depends_on_y, LinkerApi as LinkerApi_

class LinkerApi(LinkerApi_):

    class LbdEventMapWithLbdFuncAndSQS(Linker):
        __doc__ = '\n        Ref: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html\n        '
        rtype1 = awslambda.EventSourceMapping
        rtype2 = awslambda.Function
        rtype3 = sqs.Queue

        def associate(self, lbd_event_map, lbd_func, sqs_queue, *args, **kwargs):
            """
            Use SQS Queue to trigger Lambda Function
            """
            lbd_event_map.FunctionName = Ref(lbd_func)
            lbd_event_map.EventSourceArn = GetAtt(sqs_queue, 'Arn')
            x_depends_on_y(lbd_event_map, lbd_func)
            x_depends_on_y(lbd_event_map, sqs_queue)

    class LbdEventMapWithLbdFuncAndKinesisStream(Linker):
        __doc__ = '\n        Ref: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html\n        '
        rtype1 = awslambda.EventSourceMapping
        rtype2 = awslambda.Function
        rtype3 = kinesis.Stream

        def associate(self, lbd_event_map, lbd_func, kinesis_stream, *args, **kwargs):
            """
            Use Kinesis Stream to trigger Lambda Function
            """
            lbd_event_map.FunctionName = Ref(lbd_func)
            lbd_event_map.EventSourceArn = GetAtt(kinesis_stream, 'Arn')
            x_depends_on_y(lbd_event_map, lbd_func)
            x_depends_on_y(lbd_event_map, kinesis_stream)

    class LbdEventMapWithLbdFuncAndDynamoDB(Linker):
        __doc__ = '\n        Ref: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html\n        '
        rtype1 = awslambda.EventSourceMapping
        rtype2 = awslambda.Function
        rtype3 = dynamodb.Table

        def associate(self, lbd_event_map, lbd_func, dynamodb_table, *args, **kwargs):
            """
            Use DynamoDB Table Stream to trigger Lambda Function
            """
            lbd_event_map.FunctionName = Ref(lbd_func)
            lbd_event_map.EventSourceArn = GetAtt(dynamodb_table, 'StreamArn')
            x_depends_on_y(lbd_event_map, lbd_func)
            x_depends_on_y(lbd_event_map, dynamodb_table)
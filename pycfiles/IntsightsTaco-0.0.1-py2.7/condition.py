# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/aws_wrappers/dynamodb_wrapper/condition.py
# Compiled at: 2019-09-05 09:49:59
import boto3.dynamodb.conditions as boto_conditions

class Condition(object):

    @staticmethod
    def is_equal(attribute_name, tester_data):
        return boto_conditions.Attr(attribute_name).eq(tester_data)

    @staticmethod
    def not_exists(attribute_name):
        return boto_conditions.Attr(attribute_name).not_exists()

    @staticmethod
    def number_lower_than(attribute_name, tester_data):
        return boto_conditions.Attr(attribute_name).lt(tester_data)
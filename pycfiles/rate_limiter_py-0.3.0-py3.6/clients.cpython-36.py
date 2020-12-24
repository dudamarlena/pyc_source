# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limiter/clients.py
# Compiled at: 2019-04-12 11:17:57
# Size of source mod 2**32: 140 bytes
import boto3

def dynamodb():
    """ Create a DynamoDB resource instance. """
    return boto3.resource('dynamodb')
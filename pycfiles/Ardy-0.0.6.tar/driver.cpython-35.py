# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prometeo/projects/ardy/ardy/core/triggers/driver.py
# Compiled at: 2018-04-15 10:04:49
# Size of source mod 2**32: 2339 bytes
from __future__ import unicode_literals, print_function
import json
from abc import ABCMeta, abstractmethod
from botocore.exceptions import ClientError
from ardy.core.triggers.exceptions import ArdyNoTriggerConfError
from ardy.utils.aws import AWSCli

class Trigger(object):
    __metaclass__ = ABCMeta
    _DEPLOY_KEYS_WHITELIST = []
    _LAMBDA_ARN_KEY = None
    trigget_type = None
    get_awsservice_method = None
    awsservice_put_method = None

    def __init__(self, *args, **kwargs):
        self.lambda_function_arn = kwargs['lambda_function_arn']
        self.lambda_conf = kwargs['lambda_conf']
        self.client = self.set_client()
        self.awslambda = AWSCli(config=self.lambda_conf).get_lambda_client()

    def get_triggers(self):
        trigger_conf = self.lambda_conf.get('triggers', {}).get(self.trigget_type)
        if not len(trigger_conf):
            raise ArdyNoTriggerConfError('Not exists conf for lambda {} and trigger {}'.format(self.lambda_function_arn, self.trigget_type))
        return trigger_conf

    def get_trigger_conf(self, index):
        trigger_conf = self.get_triggers()[index]
        return trigger_conf

    def get_deploy_conf(self, trigger_conf):
        conf = {k:v for k, v in trigger_conf.items() if k in self._DEPLOY_KEYS_WHITELIST}
        return conf

    def set_client(self):
        return self.set_aws_class()

    def set_aws_class(self, *args, **kwargs):
        return getattr(AWSCli(config=self.lambda_conf), self.get_awsservice_method)()

    @abstractmethod
    def put(self, *args, **kwargs):
        return getattr(self.client, self.awsservice_put_method)(*args, **kwargs)

    def lambda_exist_policy(self, function_name, StatementId):
        try:
            response = self.awslambda.get_policy(FunctionName=function_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return False
            else:
                return False

        policies = json.loads(response['Policy'])
        for policy in policies['Statement']:
            if policy['Sid'] == StatementId:
                return True

        return False
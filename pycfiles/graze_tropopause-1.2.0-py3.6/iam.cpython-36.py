# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tropopause/iam.py
# Compiled at: 2018-11-06 11:27:11
# Size of source mod 2**32: 951 bytes
from troposphere.iam import PolicyType, Role, Policy
import yaml

class RoleFromYaml(Role):

    def __init__(self, title, template, *args, **kwargs):
        with open(kwargs['AssumeRolePolicyDocument'], 'r') as (stream):
            document = yaml.load(stream)
        kwargs['AssumeRolePolicyDocument'] = document
        (super().__init__)(title, template, *args, **kwargs)


class PolicyFromYaml(Policy):

    def __init__(self, title, *args, **kwargs):
        with open(kwargs['PolicyDocument'], 'r') as (stream):
            document = yaml.load(stream)
        kwargs['PolicyDocument'] = document
        (super().__init__)(title, *args, **kwargs)


class PolicyTypeFromYaml(PolicyType):

    def __init__(self, title, template, *args, **kwargs):
        with open(kwargs['PolicyDocument'], 'r') as (stream):
            document = yaml.load(stream)
        kwargs['PolicyDocument'] = document
        (super().__init__)(title, template, *args, **kwargs)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/examples/nested_stack/deploy.py
# Compiled at: 2020-02-13 14:22:25
# Size of source mod 2**32: 657 bytes
import boto3
from troposphere_mate import StackManager
from troposphere_mate.examples.nested_stack import tier_master_iam_inst_profile
aws_profile = 'eq_sanhe'
aws_region = 'us-east-1'
cft_bucket = 'eq-sanhe-for-everything'
env_name = 'tropo-mate-examples-nested-stack-dev'
boto_ses = boto3.session.Session(profile_name=aws_profile, region_name=aws_region)
sm = StackManager(boto_ses=boto_ses, cft_bucket=cft_bucket)
sm.deploy(template=(tier_master_iam_inst_profile.template),
  stack_name=env_name,
  stack_parameters={tier_master_iam_inst_profile.param_env_name.title: env_name},
  include_iam=True)
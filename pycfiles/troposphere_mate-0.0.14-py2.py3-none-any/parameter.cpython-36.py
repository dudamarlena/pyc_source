# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/canned/parameter.py
# Compiled at: 2019-11-19 14:04:47
# Size of source mod 2**32: 999 bytes
from troposphere_mate import Parameter
param_project_name = Parameter('ProjectName',
  Type='String',
  Description='the sluggified project name, please make it as short as possible',
  MaxLength=32,
  Default='my-project')
param_stage = Parameter('Stage',
  Type='String',
  Description='an stage name indicate the which environment of this project the application running on.',
  AllowedValues=[
 'dev', 'test', 'stage', 'qa', 'prod', 'temp'],
  MaxLength=32,
  Default='dev')
param_env_name = Parameter('EnvironmentName',
  Type='String',
  Description='an environment name includes the slugified project name and stage name, represent the environment tag, and it will be a global resource name prefix for all AWS Resource. For example: my-project-dev-iam-role, my-project-dev-s3-bucket',
  MaxLength=32,
  Default='my-project-dev')
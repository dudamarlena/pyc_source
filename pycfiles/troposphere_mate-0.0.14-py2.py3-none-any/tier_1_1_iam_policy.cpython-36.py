# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/examples/nested_stack/tier_1_1_iam_policy.py
# Compiled at: 2020-02-13 14:13:44
# Size of source mod 2**32: 1094 bytes
from troposphere_mate import Template, Parameter, Output, Export, iam, helper_fn_sub
template = Template()
param_env_name = Parameter('EnvironmentName',
  Type='String')
template.add_parameter(param_env_name)
iam_ec2_instance_policy = iam.ManagedPolicy('IamPolicy',
  template=template,
  ManagedPolicyName=(helper_fn_sub('{}-web-server', param_env_name)),
  PolicyDocument={'Version':'2012-10-17', 
 'Statement':[
  {'Sid':'VisualEditor0', 
   'Effect':'Allow', 
   'Action':[
    's3:Get*',
    's3:List*',
    's3:Describe*'], 
   'Resource':'*'}]})
output_iam_ec2_instance_policy_name = Output('IamInstancePolicyArn',
  Value=(iam_ec2_instance_policy.iam_managed_policy_arn),
  Export=(Export(helper_fn_sub('{}-iam-ec2-instance-policy-arn', param_env_name))),
  DependsOn=iam_ec2_instance_policy)
template.add_output(output_iam_ec2_instance_policy_name)
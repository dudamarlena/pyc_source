# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/examples/nested_stack/tier_master_iam_inst_profile.py
# Compiled at: 2020-02-13 14:29:08
# Size of source mod 2**32: 1503 bytes
from troposphere_mate import Template, Parameter, Output, GetAtt, helper_fn_sub, Ref, Export, iam, cloudformation, link_stack_template
from . import tier_1_iam_role
template = Template()
param_env_name = Parameter('EnvironmentName',
  Type='String')
template.add_parameter(param_env_name)
iam_role_stack = cloudformation.Stack('IamRoleStack',
  template=template,
  TemplateURL='',
  Parameters={tier_1_iam_role.param_env_name.title: Ref(param_env_name)})
link_stack_template(stack=iam_role_stack, template=(tier_1_iam_role.template))
iam_instance_profile = iam.InstanceProfile('IamInstanceProfileWebServer',
  template=template,
  InstanceProfileName=(helper_fn_sub('{}-web-server', param_env_name)),
  Roles=[
 GetAtt(iam_role_stack, f"Outputs.{tier_1_iam_role.output_iam_ec2_instance_role_name.title}")],
  DependsOn=iam_role_stack)
output_iam_ec2_instance_profile_name = Output('IamInstanceProfileName',
  Value=(iam_instance_profile.iam_instance_profile_name),
  Export=(Export(helper_fn_sub('{}-iam-ec2-instance-profile-name', param_env_name))))
template.add_output(output_iam_ec2_instance_profile_name)
output_iam_ec2_instance_profile_arn = Output('IamInstanceProfileArn',
  Value=(iam_instance_profile.iam_instance_profile_arn),
  Export=(Export(helper_fn_sub('{}-iam-ec2-instance-profile-arn', param_env_name))))
template.add_output(output_iam_ec2_instance_profile_arn)
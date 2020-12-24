# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/canned/dev/get_all_aws_managed_policy_arn.py
# Compiled at: 2019-08-08 16:17:46
# Size of source mod 2**32: 596 bytes
import boto3
aws_profile = 'sanhe'
ses = boto3.session.Session(profile_name=aws_profile)
iam = ses.client('iam')
res = iam.list_policies(Scope='AWS',
  MaxItems=1000)
lines = list()
lines.append('class AWSManagedPolicyArn:')
for policy_data in res['Policies']:
    name = policy_data['PolicyName']
    if name.startswith('AWS'):
        name = name.replace('AWS', 'aws', 1)
    name = name.replace('-', '')
    new_name = name[0].lower() + name[1:]
    arn = policy_data['Arn']
    lines.append('    {} = "{}"'.format(new_name, arn))

print('\n'.join(lines))
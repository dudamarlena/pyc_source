# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/common_iam_policies.py
# Compiled at: 2016-11-22 15:21:45
ec2_read_only_policy = dict(Version='2012-10-17', Statement=[
 dict(Effect='Allow', Resource='*', Action='ec2:Describe*'),
 dict(Effect='Allow', Resource='*', Action='autoscaling:Describe*'),
 dict(Effect='Allow', Resource='*', Action='elasticloadbalancing:Describe*'),
 dict(Effect='Allow', Resource='*', Action=[
  'cloudwatch:ListMetrics',
  'cloudwatch:GetMetricStatistics',
  'cloudwatch:Describe*'])])
s3_read_only_policy = dict(Version='2012-10-17', Statement=[
 dict(Effect='Allow', Resource='*', Action=['s3:Get*', 's3:List*'])])
iam_read_only_policy = dict(Version='2012-10-17', Statement=[
 dict(Effect='Allow', Resource='*', Action=['iam:List*', 'iam:Get*'])])
ec2_full_policy = dict(Version='2012-10-17', Statement=[
 dict(Effect='Allow', Resource='*', Action='ec2:*')])
s3_full_policy = dict(Version='2012-10-17', Statement=[
 dict(Effect='Allow', Resource='*', Action='s3:*')])
sdb_full_policy = dict(Version='2012-10-17', Statement=[
 dict(Effect='Allow', Resource='*', Action='sdb:*')])
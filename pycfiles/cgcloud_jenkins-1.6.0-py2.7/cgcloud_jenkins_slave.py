# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/jenkins/cgcloud_jenkins_slave.py
# Compiled at: 2016-11-22 15:21:45
from cgcloud.core.common_iam_policies import ec2_full_policy
from cgcloud.core.ubuntu_box import Python27UpdateUbuntuBox
from cgcloud.lib import test_namespace_suffix_length
from cgcloud.lib.util import abreviated_snake_case_class_name
from cgcloud.jenkins.generic_jenkins_slaves import UbuntuTrustyGenericJenkinsSlave

class CgcloudJenkinsSlave(UbuntuTrustyGenericJenkinsSlave, Python27UpdateUbuntuBox):
    """
    Jenkins slave for runing CGCloud's unit tests
    """

    @classmethod
    def recommended_instance_type(cls):
        return 'm3.xlarge'

    def _list_packages_to_install(self):
        return super(CgcloudJenkinsSlave, self)._list_packages_to_install() + [
         'python-dev',
         'autoconf',
         'automake',
         'binutils',
         'gcc',
         'make',
         'libyaml-dev']

    def _get_iam_ec2_role(self):
        iam_role_name, policies = super(CgcloudJenkinsSlave, self)._get_iam_ec2_role()
        iam_role_name += '--' + abreviated_snake_case_class_name(CgcloudJenkinsSlave)
        cgcloud_bucket_arn = 'arn:aws:s3:::%s' % self.ctx.s3_bucket_name
        policies.update(dict(ec2_full=ec2_full_policy, iam_cgcloud_jenkins_slave_pass_role=dict(Version='2012-10-17', Statement=[
         dict(Effect='Allow', Resource=self._pass_role_arn(), Action='iam:PassRole')]), register_keypair=dict(Version='2012-10-17', Statement=[
         dict(Effect='Allow', Resource='arn:aws:s3:::*', Action='s3:ListAllMyBuckets'),
         dict(Effect='Allow', Action='s3:*', Resource=[
          cgcloud_bucket_arn, cgcloud_bucket_arn + '/*']),
         dict(Effect='Allow', Action=[
          'sns:Publish', 'sns:CreateTopic'], Resource='arn:aws:sns:*:%s:cgcloud-agent-notifications' % self.ctx.account)]), iam_cgcloud_jenkins_slave=dict(Version='2012-10-17', Statement=[
         dict(Effect='Allow', Resource='*', Action=[
          'iam:ListRoles',
          'iam:CreateRole',
          'iam:DeleteRole',
          'iam:ListRolePolicies',
          'iam:DeleteRolePolicy',
          'iam:GetRolePolicy',
          'iam:PutRolePolicy',
          'iam:ListInstanceProfiles',
          'iam:GetInstanceProfile',
          'iam:CreateInstanceProfile',
          'iam:DeleteInstanceProfile',
          'iam:RemoveRoleFromInstanceProfile',
          'iam:AddRoleToInstanceProfile',
          'iam:DeleteInstanceProfile'])])))
        return (iam_role_name, policies)

    def _pass_role_arn(self):
        """
        Return a pattern that a role name must match if it is to be passed to an instance created
        by code running on this Jenkins slave.
        """
        pass_role_arn = self._role_arn(iam_role_name_prefix='test/testnamespacesuffixpattern/')
        pass_role_arn = pass_role_arn.replace('testnamespacesuffixpattern', '?' * test_namespace_suffix_length)
        return pass_role_arn
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/iam.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 10118 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.iam
from troposphere.iam import LoginProfile as _LoginProfile, Policy as _Policy, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AccessKey(troposphere.iam.AccessKey, Mixin):

    def __init__(self, title, template=None, validation=True, UserName=REQUIRED, Serial=NOTHING, Status=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         UserName=UserName, 
         Serial=Serial, 
         Status=Status, **kwargs)
        (super(AccessKey, self).__init__)(**processed_kwargs)


class PolicyType(troposphere.iam.PolicyType, Mixin):

    def __init__(self, title, template=None, validation=True, PolicyDocument=REQUIRED, PolicyName=REQUIRED, Groups=NOTHING, Roles=NOTHING, Users=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PolicyDocument=PolicyDocument, 
         PolicyName=PolicyName, 
         Groups=Groups, 
         Roles=Roles, 
         Users=Users, **kwargs)
        (super(PolicyType, self).__init__)(**processed_kwargs)


class Policy(troposphere.iam.Policy, Mixin):

    def __init__(self, title=None, PolicyDocument=REQUIRED, PolicyName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PolicyDocument=PolicyDocument, 
         PolicyName=PolicyName, **kwargs)
        (super(Policy, self).__init__)(**processed_kwargs)


class Group(troposphere.iam.Group, Mixin):

    def __init__(self, title, template=None, validation=True, GroupName=NOTHING, ManagedPolicyArns=NOTHING, Path=NOTHING, Policies=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GroupName=GroupName, 
         ManagedPolicyArns=ManagedPolicyArns, 
         Path=Path, 
         Policies=Policies, **kwargs)
        (super(Group, self).__init__)(**processed_kwargs)


class InstanceProfile(troposphere.iam.InstanceProfile, Mixin):

    def __init__(self, title, template=None, validation=True, Roles=REQUIRED, Path=NOTHING, InstanceProfileName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Roles=Roles, 
         Path=Path, 
         InstanceProfileName=InstanceProfileName, **kwargs)
        (super(InstanceProfile, self).__init__)(**processed_kwargs)


class Role(troposphere.iam.Role, Mixin):

    def __init__(self, title, template=None, validation=True, AssumeRolePolicyDocument=REQUIRED, Description=NOTHING, ManagedPolicyArns=NOTHING, MaxSessionDuration=NOTHING, Path=NOTHING, PermissionsBoundary=NOTHING, Policies=NOTHING, RoleName=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AssumeRolePolicyDocument=AssumeRolePolicyDocument, 
         Description=Description, 
         ManagedPolicyArns=ManagedPolicyArns, 
         MaxSessionDuration=MaxSessionDuration, 
         Path=Path, 
         PermissionsBoundary=PermissionsBoundary, 
         Policies=Policies, 
         RoleName=RoleName, 
         Tags=Tags, **kwargs)
        (super(Role, self).__init__)(**processed_kwargs)


class ServiceLinkedRole(troposphere.iam.ServiceLinkedRole, Mixin):

    def __init__(self, title, template=None, validation=True, AWSServiceName=REQUIRED, CustomSuffix=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AWSServiceName=AWSServiceName, 
         CustomSuffix=CustomSuffix, 
         Description=Description, **kwargs)
        (super(ServiceLinkedRole, self).__init__)(**processed_kwargs)


class LoginProfile(troposphere.iam.LoginProfile, Mixin):

    def __init__(self, title=None, Password=REQUIRED, PasswordResetRequired=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Password=Password, 
         PasswordResetRequired=PasswordResetRequired, **kwargs)
        (super(LoginProfile, self).__init__)(**processed_kwargs)


class User(troposphere.iam.User, Mixin):

    def __init__(self, title, template=None, validation=True, Groups=NOTHING, LoginProfile=NOTHING, ManagedPolicyArns=NOTHING, Path=NOTHING, PermissionsBoundary=NOTHING, Policies=NOTHING, Tags=NOTHING, UserName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Groups=Groups, 
         LoginProfile=LoginProfile, 
         ManagedPolicyArns=ManagedPolicyArns, 
         Path=Path, 
         PermissionsBoundary=PermissionsBoundary, 
         Policies=Policies, 
         Tags=Tags, 
         UserName=UserName, **kwargs)
        (super(User, self).__init__)(**processed_kwargs)


class UserToGroupAddition(troposphere.iam.UserToGroupAddition, Mixin):

    def __init__(self, title, template=None, validation=True, GroupName=REQUIRED, Users=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GroupName=GroupName, 
         Users=Users, **kwargs)
        (super(UserToGroupAddition, self).__init__)(**processed_kwargs)


class ManagedPolicy(troposphere.iam.ManagedPolicy, Mixin):

    def __init__(self, title, template=None, validation=True, PolicyDocument=REQUIRED, Description=NOTHING, Groups=NOTHING, ManagedPolicyName=NOTHING, Path=NOTHING, Roles=NOTHING, Users=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PolicyDocument=PolicyDocument, 
         Description=Description, 
         Groups=Groups, 
         ManagedPolicyName=ManagedPolicyName, 
         Path=Path, 
         Roles=Roles, 
         Users=Users, **kwargs)
        (super(ManagedPolicy, self).__init__)(**processed_kwargs)
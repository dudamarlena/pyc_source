# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/codedeploy.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 16406 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.codedeploy
from troposphere.codedeploy import Alarm as _Alarm, AlarmConfiguration as _AlarmConfiguration, AutoRollbackConfiguration as _AutoRollbackConfiguration, Deployment as _Deployment, DeploymentStyle as _DeploymentStyle, Ec2TagFilters as _Ec2TagFilters, Ec2TagSet as _Ec2TagSet, Ec2TagSetListObject as _Ec2TagSetListObject, ElbInfoList as _ElbInfoList, GitHubLocation as _GitHubLocation, LoadBalancerInfo as _LoadBalancerInfo, MinimumHealthyHosts as _MinimumHealthyHosts, OnPremisesInstanceTagFilters as _OnPremisesInstanceTagFilters, OnPremisesTagSet as _OnPremisesTagSet, OnPremisesTagSetList as _OnPremisesTagSetList, OnPremisesTagSetObject as _OnPremisesTagSetObject, Revision as _Revision, S3Location as _S3Location, TagFilters as _TagFilters, TargetGroupInfoList as _TargetGroupInfoList, TriggerConfig as _TriggerConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class GitHubLocation(troposphere.codedeploy.GitHubLocation, Mixin):

    def __init__(self, title=None, CommitId=REQUIRED, Repository=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CommitId=CommitId, 
         Repository=Repository, **kwargs)
        (super(GitHubLocation, self).__init__)(**processed_kwargs)


class S3Location(troposphere.codedeploy.S3Location, Mixin):

    def __init__(self, title=None, Bucket=REQUIRED, BundleType=REQUIRED, Key=REQUIRED, ETag=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         BundleType=BundleType, 
         Key=Key, 
         ETag=ETag, 
         Version=Version, **kwargs)
        (super(S3Location, self).__init__)(**processed_kwargs)


class Revision(troposphere.codedeploy.Revision, Mixin):

    def __init__(self, title=None, GitHubLocation=NOTHING, RevisionType=NOTHING, S3Location=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         GitHubLocation=GitHubLocation, 
         RevisionType=RevisionType, 
         S3Location=S3Location, **kwargs)
        (super(Revision, self).__init__)(**processed_kwargs)


class AutoRollbackConfiguration(troposphere.codedeploy.AutoRollbackConfiguration, Mixin):

    def __init__(self, title=None, Enabled=NOTHING, Events=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         Events=Events, **kwargs)
        (super(AutoRollbackConfiguration, self).__init__)(**processed_kwargs)


class Deployment(troposphere.codedeploy.Deployment, Mixin):

    def __init__(self, title=None, Revision=REQUIRED, Description=NOTHING, IgnoreApplicationStopFailures=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Revision=Revision, 
         Description=Description, 
         IgnoreApplicationStopFailures=IgnoreApplicationStopFailures, **kwargs)
        (super(Deployment, self).__init__)(**processed_kwargs)


class DeploymentStyle(troposphere.codedeploy.DeploymentStyle, Mixin):

    def __init__(self, title=None, DeploymentOption=NOTHING, DeploymentType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeploymentOption=DeploymentOption, 
         DeploymentType=DeploymentType, **kwargs)
        (super(DeploymentStyle, self).__init__)(**processed_kwargs)


class Ec2TagFilters(troposphere.codedeploy.Ec2TagFilters, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Key=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(Ec2TagFilters, self).__init__)(**processed_kwargs)


class TagFilters(troposphere.codedeploy.TagFilters, Mixin):

    def __init__(self, title=None, Key=NOTHING, Type=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Type=Type, 
         Value=Value, **kwargs)
        (super(TagFilters, self).__init__)(**processed_kwargs)


class ElbInfoList(troposphere.codedeploy.ElbInfoList, Mixin):

    def __init__(self, title=None, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, **kwargs)
        (super(ElbInfoList, self).__init__)(**processed_kwargs)


class TargetGroupInfoList(troposphere.codedeploy.TargetGroupInfoList, Mixin):

    def __init__(self, title=None, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, **kwargs)
        (super(TargetGroupInfoList, self).__init__)(**processed_kwargs)


class LoadBalancerInfo(troposphere.codedeploy.LoadBalancerInfo, Mixin):

    def __init__(self, title=None, ElbInfoList=NOTHING, TargetGroupInfoList=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ElbInfoList=ElbInfoList, 
         TargetGroupInfoList=TargetGroupInfoList, **kwargs)
        (super(LoadBalancerInfo, self).__init__)(**processed_kwargs)


class OnPremisesInstanceTagFilters(troposphere.codedeploy.OnPremisesInstanceTagFilters, Mixin):

    def __init__(self, title=None, Key=NOTHING, Type=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Type=Type, 
         Value=Value, **kwargs)
        (super(OnPremisesInstanceTagFilters, self).__init__)(**processed_kwargs)


class MinimumHealthyHosts(troposphere.codedeploy.MinimumHealthyHosts, Mixin):

    def __init__(self, title=None, Type=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Value=Value, **kwargs)
        (super(MinimumHealthyHosts, self).__init__)(**processed_kwargs)


class Application(troposphere.codedeploy.Application, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=NOTHING, ComputePlatform=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         ComputePlatform=ComputePlatform, **kwargs)
        (super(Application, self).__init__)(**processed_kwargs)


class DeploymentConfig(troposphere.codedeploy.DeploymentConfig, Mixin):

    def __init__(self, title, template=None, validation=True, DeploymentConfigName=NOTHING, MinimumHealthyHosts=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DeploymentConfigName=DeploymentConfigName, 
         MinimumHealthyHosts=MinimumHealthyHosts, **kwargs)
        (super(DeploymentConfig, self).__init__)(**processed_kwargs)


class Alarm(troposphere.codedeploy.Alarm, Mixin):

    def __init__(self, title=None, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, **kwargs)
        (super(Alarm, self).__init__)(**processed_kwargs)


class AlarmConfiguration(troposphere.codedeploy.AlarmConfiguration, Mixin):

    def __init__(self, title=None, Alarms=NOTHING, Enabled=NOTHING, IgnorePollAlarmFailure=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Alarms=Alarms, 
         Enabled=Enabled, 
         IgnorePollAlarmFailure=IgnorePollAlarmFailure, **kwargs)
        (super(AlarmConfiguration, self).__init__)(**processed_kwargs)


class TriggerConfig(troposphere.codedeploy.TriggerConfig, Mixin):

    def __init__(self, title=None, TriggerEvents=NOTHING, TriggerName=NOTHING, TriggerTargetArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TriggerEvents=TriggerEvents, 
         TriggerName=TriggerName, 
         TriggerTargetArn=TriggerTargetArn, **kwargs)
        (super(TriggerConfig, self).__init__)(**processed_kwargs)


class Ec2TagSetListObject(troposphere.codedeploy.Ec2TagSetListObject, Mixin):

    def __init__(self, title=None, Ec2TagGroup=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Ec2TagGroup=Ec2TagGroup, **kwargs)
        (super(Ec2TagSetListObject, self).__init__)(**processed_kwargs)


class Ec2TagSet(troposphere.codedeploy.Ec2TagSet, Mixin):

    def __init__(self, title=None, Ec2TagSetList=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Ec2TagSetList=Ec2TagSetList, **kwargs)
        (super(Ec2TagSet, self).__init__)(**processed_kwargs)


class OnPremisesTagSetObject(troposphere.codedeploy.OnPremisesTagSetObject, Mixin):

    def __init__(self, title=None, OnPremisesTagGroup=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OnPremisesTagGroup=OnPremisesTagGroup, **kwargs)
        (super(OnPremisesTagSetObject, self).__init__)(**processed_kwargs)


class OnPremisesTagSetList(troposphere.codedeploy.OnPremisesTagSetList, Mixin):

    def __init__(self, title=None, OnPremisesTagSetList=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OnPremisesTagSetList=OnPremisesTagSetList, **kwargs)
        (super(OnPremisesTagSetList, self).__init__)(**processed_kwargs)


class OnPremisesTagSet(troposphere.codedeploy.OnPremisesTagSet, Mixin):

    def __init__(self, title=None, OnPremisesTagSetList=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OnPremisesTagSetList=OnPremisesTagSetList, **kwargs)
        (super(OnPremisesTagSet, self).__init__)(**processed_kwargs)


class DeploymentGroup(troposphere.codedeploy.DeploymentGroup, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationName=REQUIRED, ServiceRoleArn=REQUIRED, AlarmConfiguration=NOTHING, AutoRollbackConfiguration=NOTHING, AutoScalingGroups=NOTHING, Deployment=NOTHING, DeploymentConfigName=NOTHING, DeploymentGroupName=NOTHING, DeploymentStyle=NOTHING, Ec2TagFilters=NOTHING, Ec2TagSet=NOTHING, LoadBalancerInfo=NOTHING, OnPremisesInstanceTagFilters=NOTHING, OnPremisesInstanceTagSet=NOTHING, TriggerConfigurations=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationName=ApplicationName, 
         ServiceRoleArn=ServiceRoleArn, 
         AlarmConfiguration=AlarmConfiguration, 
         AutoRollbackConfiguration=AutoRollbackConfiguration, 
         AutoScalingGroups=AutoScalingGroups, 
         Deployment=Deployment, 
         DeploymentConfigName=DeploymentConfigName, 
         DeploymentGroupName=DeploymentGroupName, 
         DeploymentStyle=DeploymentStyle, 
         Ec2TagFilters=Ec2TagFilters, 
         Ec2TagSet=Ec2TagSet, 
         LoadBalancerInfo=LoadBalancerInfo, 
         OnPremisesInstanceTagFilters=OnPremisesInstanceTagFilters, 
         OnPremisesInstanceTagSet=OnPremisesInstanceTagSet, 
         TriggerConfigurations=TriggerConfigurations, **kwargs)
        (super(DeploymentGroup, self).__init__)(**processed_kwargs)
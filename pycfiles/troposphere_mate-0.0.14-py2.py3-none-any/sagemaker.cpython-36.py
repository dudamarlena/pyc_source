# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/sagemaker.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 13380 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.sagemaker
from troposphere.sagemaker import CognitoMemberDefinition as _CognitoMemberDefinition, ContainerDefinition as _ContainerDefinition, GitConfig as _GitConfig, MemberDefinition as _MemberDefinition, NotebookInstanceLifecycleHook as _NotebookInstanceLifecycleHook, NotificationConfiguration as _NotificationConfiguration, ProductionVariant as _ProductionVariant, Tags as _Tags, VpcConfig as _VpcConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class GitConfig(troposphere.sagemaker.GitConfig, Mixin):

    def __init__(self, title=None, RepositoryUrl=REQUIRED, Branch=NOTHING, SecretArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RepositoryUrl=RepositoryUrl, 
         Branch=Branch, 
         SecretArn=SecretArn, **kwargs)
        (super(GitConfig, self).__init__)(**processed_kwargs)


class CodeRepository(troposphere.sagemaker.CodeRepository, Mixin):

    def __init__(self, title, template=None, validation=True, GitConfig=REQUIRED, CodeRepositoryName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GitConfig=GitConfig, 
         CodeRepositoryName=CodeRepositoryName, **kwargs)
        (super(CodeRepository, self).__init__)(**processed_kwargs)


class Endpoint(troposphere.sagemaker.Endpoint, Mixin):

    def __init__(self, title, template=None, validation=True, EndpointConfigName=REQUIRED, Tags=REQUIRED, EndpointName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         EndpointConfigName=EndpointConfigName, 
         Tags=Tags, 
         EndpointName=EndpointName, **kwargs)
        (super(Endpoint, self).__init__)(**processed_kwargs)


class ProductionVariant(troposphere.sagemaker.ProductionVariant, Mixin):

    def __init__(self, title=None, ModelName=REQUIRED, VariantName=REQUIRED, InitialInstanceCount=REQUIRED, InstanceType=REQUIRED, InitialVariantWeight=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ModelName=ModelName, 
         VariantName=VariantName, 
         InitialInstanceCount=InitialInstanceCount, 
         InstanceType=InstanceType, 
         InitialVariantWeight=InitialVariantWeight, **kwargs)
        (super(ProductionVariant, self).__init__)(**processed_kwargs)


class EndpointConfig(troposphere.sagemaker.EndpointConfig, Mixin):

    def __init__(self, title, template=None, validation=True, ProductionVariants=REQUIRED, Tags=REQUIRED, EndpointConfigName=NOTHING, KmsKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ProductionVariants=ProductionVariants, 
         Tags=Tags, 
         EndpointConfigName=EndpointConfigName, 
         KmsKeyId=KmsKeyId, **kwargs)
        (super(EndpointConfig, self).__init__)(**processed_kwargs)


class ContainerDefinition(troposphere.sagemaker.ContainerDefinition, Mixin):

    def __init__(self, title=None, Image=REQUIRED, ContainerHostname=NOTHING, Environment=NOTHING, ModelDataUrl=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Image=Image, 
         ContainerHostname=ContainerHostname, 
         Environment=Environment, 
         ModelDataUrl=ModelDataUrl, **kwargs)
        (super(ContainerDefinition, self).__init__)(**processed_kwargs)


class VpcConfig(troposphere.sagemaker.VpcConfig, Mixin):

    def __init__(self, title=None, Subnets=REQUIRED, SecurityGroupIds=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Subnets=Subnets, 
         SecurityGroupIds=SecurityGroupIds, **kwargs)
        (super(VpcConfig, self).__init__)(**processed_kwargs)


class Model(troposphere.sagemaker.Model, Mixin):

    def __init__(self, title, template=None, validation=True, ExecutionRoleArn=REQUIRED, PrimaryContainer=REQUIRED, Containers=NOTHING, ModelName=NOTHING, VpcConfig=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ExecutionRoleArn=ExecutionRoleArn, 
         PrimaryContainer=PrimaryContainer, 
         Containers=Containers, 
         ModelName=ModelName, 
         VpcConfig=VpcConfig, 
         Tags=Tags, **kwargs)
        (super(Model, self).__init__)(**processed_kwargs)


class NotebookInstanceLifecycleHook(troposphere.sagemaker.NotebookInstanceLifecycleHook, Mixin):

    def __init__(self, title=None, Content=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Content=Content, **kwargs)
        (super(NotebookInstanceLifecycleHook, self).__init__)(**processed_kwargs)


class NotebookInstanceLifecycleConfig(troposphere.sagemaker.NotebookInstanceLifecycleConfig, Mixin):

    def __init__(self, title, template=None, validation=True, NotebookInstanceLifecycleConfigName=NOTHING, OnCreate=NOTHING, OnStart=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         NotebookInstanceLifecycleConfigName=NotebookInstanceLifecycleConfigName, 
         OnCreate=OnCreate, 
         OnStart=OnStart, **kwargs)
        (super(NotebookInstanceLifecycleConfig, self).__init__)(**processed_kwargs)


class NotebookInstance(troposphere.sagemaker.NotebookInstance, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceType=REQUIRED, RoleArn=REQUIRED, AcceleratorTypes=NOTHING, AdditionalCodeRepositories=NOTHING, DefaultCodeRepository=NOTHING, DirectInternetAccess=NOTHING, KmsKeyId=NOTHING, LifecycleConfigName=NOTHING, NotebookInstanceName=NOTHING, RootAccess=NOTHING, SecurityGroupIds=NOTHING, SubnetId=NOTHING, Tags=NOTHING, VolumeSizeInGB=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceType=InstanceType, 
         RoleArn=RoleArn, 
         AcceleratorTypes=AcceleratorTypes, 
         AdditionalCodeRepositories=AdditionalCodeRepositories, 
         DefaultCodeRepository=DefaultCodeRepository, 
         DirectInternetAccess=DirectInternetAccess, 
         KmsKeyId=KmsKeyId, 
         LifecycleConfigName=LifecycleConfigName, 
         NotebookInstanceName=NotebookInstanceName, 
         RootAccess=RootAccess, 
         SecurityGroupIds=SecurityGroupIds, 
         SubnetId=SubnetId, 
         Tags=Tags, 
         VolumeSizeInGB=VolumeSizeInGB, **kwargs)
        (super(NotebookInstance, self).__init__)(**processed_kwargs)


class CognitoMemberDefinition(troposphere.sagemaker.CognitoMemberDefinition, Mixin):

    def __init__(self, title=None, CognitoClientId=REQUIRED, CognitoUserGroup=REQUIRED, CognitoUserPool=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CognitoClientId=CognitoClientId, 
         CognitoUserGroup=CognitoUserGroup, 
         CognitoUserPool=CognitoUserPool, **kwargs)
        (super(CognitoMemberDefinition, self).__init__)(**processed_kwargs)


class MemberDefinition(troposphere.sagemaker.MemberDefinition, Mixin):

    def __init__(self, title=None, CognitoMemberDefinition=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CognitoMemberDefinition=CognitoMemberDefinition, **kwargs)
        (super(MemberDefinition, self).__init__)(**processed_kwargs)


class NotificationConfiguration(troposphere.sagemaker.NotificationConfiguration, Mixin):

    def __init__(self, title=None, NotificationTopicArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NotificationTopicArn=NotificationTopicArn, **kwargs)
        (super(NotificationConfiguration, self).__init__)(**processed_kwargs)


class Workteam(troposphere.sagemaker.Workteam, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, MemberDefinitions=NOTHING, NotificationConfiguration=NOTHING, Tags=NOTHING, WorkteamName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         MemberDefinitions=MemberDefinitions, 
         NotificationConfiguration=NotificationConfiguration, 
         Tags=Tags, 
         WorkteamName=WorkteamName, **kwargs)
        (super(Workteam, self).__init__)(**processed_kwargs)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/appstream.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 14651 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.appstream
from troposphere.appstream import AccessEndpoint as _AccessEndpoint, ApplicationSettings as _ApplicationSettings, ComputeCapacity as _ComputeCapacity, DomainJoinInfo as _DomainJoinInfo, ServiceAccountCredentials as _ServiceAccountCredentials, StorageConnector as _StorageConnector, Tags as _Tags, UserSetting as _UserSetting, VpcConfig as _VpcConfig
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ServiceAccountCredentials(troposphere.appstream.ServiceAccountCredentials, Mixin):

    def __init__(self, title=None, AccountName=REQUIRED, AccountPassword=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AccountName=AccountName, 
         AccountPassword=AccountPassword, **kwargs)
        (super(ServiceAccountCredentials, self).__init__)(**processed_kwargs)


class DirectoryConfig(troposphere.appstream.DirectoryConfig, Mixin):

    def __init__(self, title, template=None, validation=True, DirectoryName=REQUIRED, OrganizationalUnitDistinguishedNames=REQUIRED, ServiceAccountCredentials=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DirectoryName=DirectoryName, 
         OrganizationalUnitDistinguishedNames=OrganizationalUnitDistinguishedNames, 
         ServiceAccountCredentials=ServiceAccountCredentials, **kwargs)
        (super(DirectoryConfig, self).__init__)(**processed_kwargs)


class ComputeCapacity(troposphere.appstream.ComputeCapacity, Mixin):

    def __init__(self, title=None, DesiredInstances=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DesiredInstances=DesiredInstances, **kwargs)
        (super(ComputeCapacity, self).__init__)(**processed_kwargs)


class DomainJoinInfo(troposphere.appstream.DomainJoinInfo, Mixin):

    def __init__(self, title=None, DirectoryName=NOTHING, OrganizationalUnitDistinguishedName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DirectoryName=DirectoryName, 
         OrganizationalUnitDistinguishedName=OrganizationalUnitDistinguishedName, **kwargs)
        (super(DomainJoinInfo, self).__init__)(**processed_kwargs)


class VpcConfig(troposphere.appstream.VpcConfig, Mixin):

    def __init__(self, title=None, SecurityGroupIds=NOTHING, SubnetIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SecurityGroupIds=SecurityGroupIds, 
         SubnetIds=SubnetIds, **kwargs)
        (super(VpcConfig, self).__init__)(**processed_kwargs)


class Fleet(troposphere.appstream.Fleet, Mixin):

    def __init__(self, title, template=None, validation=True, ComputeCapacity=REQUIRED, InstanceType=REQUIRED, Description=NOTHING, DisconnectTimeoutInSeconds=NOTHING, DisplayName=NOTHING, DomainJoinInfo=NOTHING, EnableDefaultInternetAccess=NOTHING, FleetType=NOTHING, IdleDisconnectTimeoutInSeconds=NOTHING, ImageArn=NOTHING, ImageName=NOTHING, MaxUserDurationInSeconds=NOTHING, Name=NOTHING, Tags=NOTHING, VpcConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ComputeCapacity=ComputeCapacity, 
         InstanceType=InstanceType, 
         Description=Description, 
         DisconnectTimeoutInSeconds=DisconnectTimeoutInSeconds, 
         DisplayName=DisplayName, 
         DomainJoinInfo=DomainJoinInfo, 
         EnableDefaultInternetAccess=EnableDefaultInternetAccess, 
         FleetType=FleetType, 
         IdleDisconnectTimeoutInSeconds=IdleDisconnectTimeoutInSeconds, 
         ImageArn=ImageArn, 
         ImageName=ImageName, 
         MaxUserDurationInSeconds=MaxUserDurationInSeconds, 
         Name=Name, 
         Tags=Tags, 
         VpcConfig=VpcConfig, **kwargs)
        (super(Fleet, self).__init__)(**processed_kwargs)


class AccessEndpoint(troposphere.appstream.AccessEndpoint, Mixin):

    def __init__(self, title=None, EndpointType=REQUIRED, VpceId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EndpointType=EndpointType, 
         VpceId=VpceId, **kwargs)
        (super(AccessEndpoint, self).__init__)(**processed_kwargs)


class ImageBuilder(troposphere.appstream.ImageBuilder, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceType=REQUIRED, AccessEndpoints=NOTHING, AppstreamAgentVersion=NOTHING, Description=NOTHING, DisplayName=NOTHING, DomainJoinInfo=NOTHING, EnableDefaultInternetAccess=NOTHING, ImageArn=NOTHING, ImageName=NOTHING, Name=NOTHING, Tags=NOTHING, VpcConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceType=InstanceType, 
         AccessEndpoints=AccessEndpoints, 
         AppstreamAgentVersion=AppstreamAgentVersion, 
         Description=Description, 
         DisplayName=DisplayName, 
         DomainJoinInfo=DomainJoinInfo, 
         EnableDefaultInternetAccess=EnableDefaultInternetAccess, 
         ImageArn=ImageArn, 
         ImageName=ImageName, 
         Name=Name, 
         Tags=Tags, 
         VpcConfig=VpcConfig, **kwargs)
        (super(ImageBuilder, self).__init__)(**processed_kwargs)


class ApplicationSettings(troposphere.appstream.ApplicationSettings, Mixin):

    def __init__(self, title=None, Enabled=REQUIRED, SettingsGroup=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         SettingsGroup=SettingsGroup, **kwargs)
        (super(ApplicationSettings, self).__init__)(**processed_kwargs)


class StorageConnector(troposphere.appstream.StorageConnector, Mixin):

    def __init__(self, title=None, ConnectorType=REQUIRED, Domains=NOTHING, ResourceIdentifier=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ConnectorType=ConnectorType, 
         Domains=Domains, 
         ResourceIdentifier=ResourceIdentifier, **kwargs)
        (super(StorageConnector, self).__init__)(**processed_kwargs)


class UserSetting(troposphere.appstream.UserSetting, Mixin):

    def __init__(self, title=None, Action=REQUIRED, Permission=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Permission=Permission, **kwargs)
        (super(UserSetting, self).__init__)(**processed_kwargs)


class Stack(troposphere.appstream.Stack, Mixin):

    def __init__(self, title, template=None, validation=True, AccessEndpoints=NOTHING, ApplicationSettings=NOTHING, AttributesToDelete=NOTHING, DeleteStorageConnectors=NOTHING, Description=NOTHING, DisplayName=NOTHING, EmbedHostDomains=NOTHING, FeedbackURL=NOTHING, Name=NOTHING, RedirectURL=NOTHING, StorageConnectors=NOTHING, Tags=NOTHING, UserSettings=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AccessEndpoints=AccessEndpoints, 
         ApplicationSettings=ApplicationSettings, 
         AttributesToDelete=AttributesToDelete, 
         DeleteStorageConnectors=DeleteStorageConnectors, 
         Description=Description, 
         DisplayName=DisplayName, 
         EmbedHostDomains=EmbedHostDomains, 
         FeedbackURL=FeedbackURL, 
         Name=Name, 
         RedirectURL=RedirectURL, 
         StorageConnectors=StorageConnectors, 
         Tags=Tags, 
         UserSettings=UserSettings, **kwargs)
        (super(Stack, self).__init__)(**processed_kwargs)


class StackFleetAssociation(troposphere.appstream.StackFleetAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, FleetName=REQUIRED, StackName=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         FleetName=FleetName, 
         StackName=StackName, **kwargs)
        (super(StackFleetAssociation, self).__init__)(**processed_kwargs)


class StackUserAssociation(troposphere.appstream.StackUserAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, AuthenticationType=REQUIRED, StackName=REQUIRED, UserName=REQUIRED, SendEmailNotification=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthenticationType=AuthenticationType, 
         StackName=StackName, 
         UserName=UserName, 
         SendEmailNotification=SendEmailNotification, **kwargs)
        (super(StackUserAssociation, self).__init__)(**processed_kwargs)


class User(troposphere.appstream.User, Mixin):

    def __init__(self, title, template=None, validation=True, AuthenticationType=REQUIRED, UserName=REQUIRED, FirstName=NOTHING, LastName=NOTHING, MessageAction=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthenticationType=AuthenticationType, 
         UserName=UserName, 
         FirstName=FirstName, 
         LastName=LastName, 
         MessageAction=MessageAction, **kwargs)
        (super(User, self).__init__)(**processed_kwargs)
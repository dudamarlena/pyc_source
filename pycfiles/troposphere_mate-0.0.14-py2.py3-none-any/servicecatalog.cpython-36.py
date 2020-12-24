# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/servicecatalog.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 18596 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.servicecatalog
from troposphere.servicecatalog import ProvisioningArtifactProperties as _ProvisioningArtifactProperties, ProvisioningParameter as _ProvisioningParameter, ProvisioningPreferences as _ProvisioningPreferences, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AcceptedPortfolioShare(troposphere.servicecatalog.AcceptedPortfolioShare, Mixin):

    def __init__(self, title, template=None, validation=True, PortfolioId=REQUIRED, AcceptLanguage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PortfolioId=PortfolioId, 
         AcceptLanguage=AcceptLanguage, **kwargs)
        (super(AcceptedPortfolioShare, self).__init__)(**processed_kwargs)


class ProvisioningArtifactProperties(troposphere.servicecatalog.ProvisioningArtifactProperties, Mixin):

    def __init__(self, title=None, Info=REQUIRED, Description=NOTHING, DisableTemplateValidation=NOTHING, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Info=Info, 
         Description=Description, 
         DisableTemplateValidation=DisableTemplateValidation, 
         Name=Name, **kwargs)
        (super(ProvisioningArtifactProperties, self).__init__)(**processed_kwargs)


class CloudFormationProduct(troposphere.servicecatalog.CloudFormationProduct, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, Owner=REQUIRED, ProvisioningArtifactParameters=REQUIRED, AcceptLanguage=NOTHING, Description=NOTHING, Distributor=NOTHING, SupportDescription=NOTHING, SupportEmail=NOTHING, SupportUrl=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         Owner=Owner, 
         ProvisioningArtifactParameters=ProvisioningArtifactParameters, 
         AcceptLanguage=AcceptLanguage, 
         Description=Description, 
         Distributor=Distributor, 
         SupportDescription=SupportDescription, 
         SupportEmail=SupportEmail, 
         SupportUrl=SupportUrl, 
         Tags=Tags, **kwargs)
        (super(CloudFormationProduct, self).__init__)(**processed_kwargs)


class ProvisioningParameter(troposphere.servicecatalog.ProvisioningParameter, Mixin):

    def __init__(self, title=None, Key=NOTHING, Value=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(ProvisioningParameter, self).__init__)(**processed_kwargs)


class ProvisioningPreferences(troposphere.servicecatalog.ProvisioningPreferences, Mixin):

    def __init__(self, title=None, StackSetAccounts=NOTHING, StackSetFailureToleranceCount=NOTHING, StackSetFailureTolerancePercentage=NOTHING, StackSetMaxConcurrencyCount=NOTHING, StackSetMaxConcurrencyPercentage=NOTHING, StackSetOperationType=NOTHING, StackSetRegions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         StackSetAccounts=StackSetAccounts, 
         StackSetFailureToleranceCount=StackSetFailureToleranceCount, 
         StackSetFailureTolerancePercentage=StackSetFailureTolerancePercentage, 
         StackSetMaxConcurrencyCount=StackSetMaxConcurrencyCount, 
         StackSetMaxConcurrencyPercentage=StackSetMaxConcurrencyPercentage, 
         StackSetOperationType=StackSetOperationType, 
         StackSetRegions=StackSetRegions, **kwargs)
        (super(ProvisioningPreferences, self).__init__)(**processed_kwargs)


class CloudFormationProvisionedProduct(troposphere.servicecatalog.CloudFormationProvisionedProduct, Mixin):

    def __init__(self, title, template=None, validation=True, AcceptLanguage=NOTHING, NotificationArns=NOTHING, PathId=NOTHING, ProductId=NOTHING, ProductName=NOTHING, ProvisionedProductName=NOTHING, ProvisioningArtifactId=NOTHING, ProvisioningArtifactName=NOTHING, ProvisioningParameters=NOTHING, ProvisioningPreferences=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AcceptLanguage=AcceptLanguage, 
         NotificationArns=NotificationArns, 
         PathId=PathId, 
         ProductId=ProductId, 
         ProductName=ProductName, 
         ProvisionedProductName=ProvisionedProductName, 
         ProvisioningArtifactId=ProvisioningArtifactId, 
         ProvisioningArtifactName=ProvisioningArtifactName, 
         ProvisioningParameters=ProvisioningParameters, 
         ProvisioningPreferences=ProvisioningPreferences, 
         Tags=Tags, **kwargs)
        (super(CloudFormationProvisionedProduct, self).__init__)(**processed_kwargs)


class LaunchNotificationConstraint(troposphere.servicecatalog.LaunchNotificationConstraint, Mixin):

    def __init__(self, title, template=None, validation=True, NotificationArns=REQUIRED, PortfolioId=REQUIRED, ProductId=REQUIRED, AcceptLanguage=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         NotificationArns=NotificationArns, 
         PortfolioId=PortfolioId, 
         ProductId=ProductId, 
         AcceptLanguage=AcceptLanguage, 
         Description=Description, **kwargs)
        (super(LaunchNotificationConstraint, self).__init__)(**processed_kwargs)


class LaunchRoleConstraint(troposphere.servicecatalog.LaunchRoleConstraint, Mixin):

    def __init__(self, title, template=None, validation=True, PortfolioId=REQUIRED, ProductId=REQUIRED, RoleArn=REQUIRED, AcceptLanguage=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PortfolioId=PortfolioId, 
         ProductId=ProductId, 
         RoleArn=RoleArn, 
         AcceptLanguage=AcceptLanguage, 
         Description=Description, **kwargs)
        (super(LaunchRoleConstraint, self).__init__)(**processed_kwargs)


class LaunchTemplateConstraint(troposphere.servicecatalog.LaunchTemplateConstraint, Mixin):

    def __init__(self, title, template=None, validation=True, PortfolioId=REQUIRED, ProductId=REQUIRED, Rules=REQUIRED, AcceptLanguage=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PortfolioId=PortfolioId, 
         ProductId=ProductId, 
         Rules=Rules, 
         AcceptLanguage=AcceptLanguage, 
         Description=Description, **kwargs)
        (super(LaunchTemplateConstraint, self).__init__)(**processed_kwargs)


class Portfolio(troposphere.servicecatalog.Portfolio, Mixin):

    def __init__(self, title, template=None, validation=True, DisplayName=REQUIRED, ProviderName=REQUIRED, AcceptLanguage=NOTHING, Description=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DisplayName=DisplayName, 
         ProviderName=ProviderName, 
         AcceptLanguage=AcceptLanguage, 
         Description=Description, 
         Tags=Tags, **kwargs)
        (super(Portfolio, self).__init__)(**processed_kwargs)


class PortfolioPrincipalAssociation(troposphere.servicecatalog.PortfolioPrincipalAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, PortfolioId=REQUIRED, PrincipalARN=REQUIRED, PrincipalType=REQUIRED, AcceptLanguage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PortfolioId=PortfolioId, 
         PrincipalARN=PrincipalARN, 
         PrincipalType=PrincipalType, 
         AcceptLanguage=AcceptLanguage, **kwargs)
        (super(PortfolioPrincipalAssociation, self).__init__)(**processed_kwargs)


class PortfolioProductAssociation(troposphere.servicecatalog.PortfolioProductAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, PortfolioId=REQUIRED, ProductId=REQUIRED, AcceptLanguage=NOTHING, SourcePortfolioId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PortfolioId=PortfolioId, 
         ProductId=ProductId, 
         AcceptLanguage=AcceptLanguage, 
         SourcePortfolioId=SourcePortfolioId, **kwargs)
        (super(PortfolioProductAssociation, self).__init__)(**processed_kwargs)


class PortfolioShare(troposphere.servicecatalog.PortfolioShare, Mixin):

    def __init__(self, title, template=None, validation=True, AccountId=REQUIRED, PortfolioId=REQUIRED, AcceptLanguage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AccountId=AccountId, 
         PortfolioId=PortfolioId, 
         AcceptLanguage=AcceptLanguage, **kwargs)
        (super(PortfolioShare, self).__init__)(**processed_kwargs)


class ResourceUpdateConstraint(troposphere.servicecatalog.ResourceUpdateConstraint, Mixin):

    def __init__(self, title, template=None, validation=True, PortfolioId=REQUIRED, ProductId=REQUIRED, TagUpdateOnProvisionedProduct=REQUIRED, AcceptLanguage=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PortfolioId=PortfolioId, 
         ProductId=ProductId, 
         TagUpdateOnProvisionedProduct=TagUpdateOnProvisionedProduct, 
         AcceptLanguage=AcceptLanguage, 
         Description=Description, **kwargs)
        (super(ResourceUpdateConstraint, self).__init__)(**processed_kwargs)


class StackSetConstraint(troposphere.servicecatalog.StackSetConstraint, Mixin):

    def __init__(self, title, template=None, validation=True, AccountList=REQUIRED, AdminRole=REQUIRED, Description=REQUIRED, ExecutionRole=REQUIRED, PortfolioId=REQUIRED, ProductId=REQUIRED, RegionList=REQUIRED, StackInstanceControl=REQUIRED, AcceptLanguage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AccountList=AccountList, 
         AdminRole=AdminRole, 
         Description=Description, 
         ExecutionRole=ExecutionRole, 
         PortfolioId=PortfolioId, 
         ProductId=ProductId, 
         RegionList=RegionList, 
         StackInstanceControl=StackInstanceControl, 
         AcceptLanguage=AcceptLanguage, **kwargs)
        (super(StackSetConstraint, self).__init__)(**processed_kwargs)


class TagOption(troposphere.servicecatalog.TagOption, Mixin):

    def __init__(self, title, template=None, validation=True, Key=REQUIRED, Value=REQUIRED, Active=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Key=Key, 
         Value=Value, 
         Active=Active, **kwargs)
        (super(TagOption, self).__init__)(**processed_kwargs)


class TagOptionAssociation(troposphere.servicecatalog.TagOptionAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, ResourceId=REQUIRED, TagOptionId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ResourceId=ResourceId, 
         TagOptionId=TagOptionId, **kwargs)
        (super(TagOptionAssociation, self).__init__)(**processed_kwargs)
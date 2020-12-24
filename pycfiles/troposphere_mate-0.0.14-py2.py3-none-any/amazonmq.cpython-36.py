# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/amazonmq.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 7320 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.amazonmq
from troposphere.amazonmq import ConfigurationId as _ConfigurationId, EncryptionOptions as _EncryptionOptions, LogsConfiguration as _LogsConfiguration, MaintenanceWindow as _MaintenanceWindow, Tags as _Tags, User as _User
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ConfigurationId(troposphere.amazonmq.ConfigurationId, Mixin):

    def __init__(self, title=None, Id=REQUIRED, Revision=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         Revision=Revision, **kwargs)
        (super(ConfigurationId, self).__init__)(**processed_kwargs)


class EncryptionOptions(troposphere.amazonmq.EncryptionOptions, Mixin):

    def __init__(self, title=None, UseAwsOwnedKey=REQUIRED, KmsKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         UseAwsOwnedKey=UseAwsOwnedKey, 
         KmsKeyId=KmsKeyId, **kwargs)
        (super(EncryptionOptions, self).__init__)(**processed_kwargs)


class MaintenanceWindow(troposphere.amazonmq.MaintenanceWindow, Mixin):

    def __init__(self, title=None, DayOfWeek=REQUIRED, TimeOfDay=REQUIRED, TimeZone=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DayOfWeek=DayOfWeek, 
         TimeOfDay=TimeOfDay, 
         TimeZone=TimeZone, **kwargs)
        (super(MaintenanceWindow, self).__init__)(**processed_kwargs)


class User(troposphere.amazonmq.User, Mixin):

    def __init__(self, title=None, Password=REQUIRED, Username=REQUIRED, ConsoleAccess=NOTHING, Groups=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Password=Password, 
         Username=Username, 
         ConsoleAccess=ConsoleAccess, 
         Groups=Groups, **kwargs)
        (super(User, self).__init__)(**processed_kwargs)


class LogsConfiguration(troposphere.amazonmq.LogsConfiguration, Mixin):

    def __init__(self, title=None, Audit=NOTHING, General=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Audit=Audit, 
         General=General, **kwargs)
        (super(LogsConfiguration, self).__init__)(**processed_kwargs)


class Broker(troposphere.amazonmq.Broker, Mixin):

    def __init__(self, title, template=None, validation=True, AutoMinorVersionUpgrade=REQUIRED, BrokerName=REQUIRED, Users=REQUIRED, DeploymentMode=REQUIRED, EngineType=REQUIRED, EngineVersion=REQUIRED, HostInstanceType=REQUIRED, PubliclyAccessible=REQUIRED, Configuration=NOTHING, EncryptionOptions=NOTHING, Logs=NOTHING, MaintenanceWindowStartTime=NOTHING, SecurityGroups=NOTHING, SubnetIds=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AutoMinorVersionUpgrade=AutoMinorVersionUpgrade, 
         BrokerName=BrokerName, 
         Users=Users, 
         DeploymentMode=DeploymentMode, 
         EngineType=EngineType, 
         EngineVersion=EngineVersion, 
         HostInstanceType=HostInstanceType, 
         PubliclyAccessible=PubliclyAccessible, 
         Configuration=Configuration, 
         EncryptionOptions=EncryptionOptions, 
         Logs=Logs, 
         MaintenanceWindowStartTime=MaintenanceWindowStartTime, 
         SecurityGroups=SecurityGroups, 
         SubnetIds=SubnetIds, 
         Tags=Tags, **kwargs)
        (super(Broker, self).__init__)(**processed_kwargs)


class Configuration(troposphere.amazonmq.Configuration, Mixin):

    def __init__(self, title, template=None, validation=True, Data=REQUIRED, EngineType=REQUIRED, EngineVersion=REQUIRED, Name=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Data=Data, 
         EngineType=EngineType, 
         EngineVersion=EngineVersion, 
         Name=Name, 
         Description=Description, **kwargs)
        (super(Configuration, self).__init__)(**processed_kwargs)


class ConfigurationAssociation(troposphere.amazonmq.ConfigurationAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, Broker=REQUIRED, Configuration=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Broker=Broker, 
         Configuration=Configuration, **kwargs)
        (super(ConfigurationAssociation, self).__init__)(**processed_kwargs)
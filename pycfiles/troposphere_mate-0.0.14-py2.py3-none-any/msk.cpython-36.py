# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/msk.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 6917 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.msk
from troposphere.msk import BrokerNodeGroupInfo as _BrokerNodeGroupInfo, ClientAuthentication as _ClientAuthentication, ConfigurationInfo as _ConfigurationInfo, EBSStorageInfo as _EBSStorageInfo, EncryptionAtRest as _EncryptionAtRest, EncryptionInTransit as _EncryptionInTransit, EncryptionInfo as _EncryptionInfo, StorageInfo as _StorageInfo, Tls as _Tls
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class EBSStorageInfo(troposphere.msk.EBSStorageInfo, Mixin):

    def __init__(self, title=None, VolumeSize=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VolumeSize=VolumeSize, **kwargs)
        (super(EBSStorageInfo, self).__init__)(**processed_kwargs)


class StorageInfo(troposphere.msk.StorageInfo, Mixin):

    def __init__(self, title=None, EBSStorageInfo=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EBSStorageInfo=EBSStorageInfo, **kwargs)
        (super(StorageInfo, self).__init__)(**processed_kwargs)


class BrokerNodeGroupInfo(troposphere.msk.BrokerNodeGroupInfo, Mixin):

    def __init__(self, title=None, ClientSubnets=REQUIRED, InstanceType=REQUIRED, BrokerAZDistribution=NOTHING, SecurityGroups=NOTHING, StorageInfo=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClientSubnets=ClientSubnets, 
         InstanceType=InstanceType, 
         BrokerAZDistribution=BrokerAZDistribution, 
         SecurityGroups=SecurityGroups, 
         StorageInfo=StorageInfo, **kwargs)
        (super(BrokerNodeGroupInfo, self).__init__)(**processed_kwargs)


class Tls(troposphere.msk.Tls, Mixin):

    def __init__(self, title=None, CertificateAuthorityArnList=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CertificateAuthorityArnList=CertificateAuthorityArnList, **kwargs)
        (super(Tls, self).__init__)(**processed_kwargs)


class ClientAuthentication(troposphere.msk.ClientAuthentication, Mixin):

    def __init__(self, title=None, Tls=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Tls=Tls, **kwargs)
        (super(ClientAuthentication, self).__init__)(**processed_kwargs)


class ConfigurationInfo(troposphere.msk.ConfigurationInfo, Mixin):

    def __init__(self, title=None, Arn=REQUIRED, Revision=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Arn=Arn, 
         Revision=Revision, **kwargs)
        (super(ConfigurationInfo, self).__init__)(**processed_kwargs)


class EncryptionAtRest(troposphere.msk.EncryptionAtRest, Mixin):

    def __init__(self, title=None, DataVolumeKMSKeyId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DataVolumeKMSKeyId=DataVolumeKMSKeyId, **kwargs)
        (super(EncryptionAtRest, self).__init__)(**processed_kwargs)


class EncryptionInTransit(troposphere.msk.EncryptionInTransit, Mixin):

    def __init__(self, title=None, ClientBroker=NOTHING, InCluster=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClientBroker=ClientBroker, 
         InCluster=InCluster, **kwargs)
        (super(EncryptionInTransit, self).__init__)(**processed_kwargs)


class EncryptionInfo(troposphere.msk.EncryptionInfo, Mixin):

    def __init__(self, title=None, EncryptionAtRest=NOTHING, EncryptionInTransit=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EncryptionAtRest=EncryptionAtRest, 
         EncryptionInTransit=EncryptionInTransit, **kwargs)
        (super(EncryptionInfo, self).__init__)(**processed_kwargs)


class Cluster(troposphere.msk.Cluster, Mixin):

    def __init__(self, title, template=None, validation=True, BrokerNodeGroupInfo=REQUIRED, ClusterName=REQUIRED, KafkaVersion=REQUIRED, NumberOfBrokerNodes=REQUIRED, ClientAuthentication=NOTHING, ConfigurationInfo=NOTHING, EncryptionInfo=NOTHING, EnhancedMonitoring=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BrokerNodeGroupInfo=BrokerNodeGroupInfo, 
         ClusterName=ClusterName, 
         KafkaVersion=KafkaVersion, 
         NumberOfBrokerNodes=NumberOfBrokerNodes, 
         ClientAuthentication=ClientAuthentication, 
         ConfigurationInfo=ConfigurationInfo, 
         EncryptionInfo=EncryptionInfo, 
         EnhancedMonitoring=EnhancedMonitoring, 
         Tags=Tags, **kwargs)
        (super(Cluster, self).__init__)(**processed_kwargs)
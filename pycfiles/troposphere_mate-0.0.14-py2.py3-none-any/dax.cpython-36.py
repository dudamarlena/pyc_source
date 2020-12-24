# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/dax.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 4555 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.dax
from troposphere.dax import SSESpecification as _SSESpecification
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class SSESpecification(troposphere.dax.SSESpecification, Mixin):

    def __init__(self, title=None, SSEEnabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         SSEEnabled=SSEEnabled, **kwargs)
        (super(SSESpecification, self).__init__)(**processed_kwargs)


class Cluster(troposphere.dax.Cluster, Mixin):

    def __init__(self, title, template=None, validation=True, IAMRoleARN=REQUIRED, NodeType=REQUIRED, ReplicationFactor=REQUIRED, SubnetGroupName=REQUIRED, AvailabilityZones=NOTHING, ClusterName=NOTHING, Description=NOTHING, NotificationTopicARN=NOTHING, ParameterGroupName=NOTHING, PreferredMaintenanceWindow=NOTHING, SSESpecification=NOTHING, SecurityGroupIds=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         IAMRoleARN=IAMRoleARN, 
         NodeType=NodeType, 
         ReplicationFactor=ReplicationFactor, 
         SubnetGroupName=SubnetGroupName, 
         AvailabilityZones=AvailabilityZones, 
         ClusterName=ClusterName, 
         Description=Description, 
         NotificationTopicARN=NotificationTopicARN, 
         ParameterGroupName=ParameterGroupName, 
         PreferredMaintenanceWindow=PreferredMaintenanceWindow, 
         SSESpecification=SSESpecification, 
         SecurityGroupIds=SecurityGroupIds, 
         Tags=Tags, **kwargs)
        (super(Cluster, self).__init__)(**processed_kwargs)


class ParameterGroup(troposphere.dax.ParameterGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, ParameterGroupName=NOTHING, ParameterNameValues=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         ParameterGroupName=ParameterGroupName, 
         ParameterNameValues=ParameterNameValues, **kwargs)
        (super(ParameterGroup, self).__init__)(**processed_kwargs)


class SubnetGroup(troposphere.dax.SubnetGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, SubnetGroupName=NOTHING, SubnetIds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         SubnetGroupName=SubnetGroupName, 
         SubnetIds=SubnetIds, **kwargs)
        (super(SubnetGroup, self).__init__)(**processed_kwargs)
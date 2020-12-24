# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/managedblockchain.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 8352 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.managedblockchain
from troposphere.managedblockchain import ApprovalThresholdPolicy as _ApprovalThresholdPolicy, MemberConfiguration as _MemberConfiguration, MemberFabricConfiguration as _MemberFabricConfiguration, MemberFrameworkConfiguration as _MemberFrameworkConfiguration, NetworkConfiguration as _NetworkConfiguration, NetworkFabricConfiguration as _NetworkFabricConfiguration, NetworkFrameworkConfiguration as _NetworkFrameworkConfiguration, NodeConfiguration as _NodeConfiguration, VotingPolicy as _VotingPolicy
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class MemberFabricConfiguration(troposphere.managedblockchain.MemberFabricConfiguration, Mixin):

    def __init__(self, title=None, AdminPassword=REQUIRED, AdminUsername=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AdminPassword=AdminPassword, 
         AdminUsername=AdminUsername, **kwargs)
        (super(MemberFabricConfiguration, self).__init__)(**processed_kwargs)


class MemberFrameworkConfiguration(troposphere.managedblockchain.MemberFrameworkConfiguration, Mixin):

    def __init__(self, title=None, MemberFabricConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MemberFabricConfiguration=MemberFabricConfiguration, **kwargs)
        (super(MemberFrameworkConfiguration, self).__init__)(**processed_kwargs)


class MemberConfiguration(troposphere.managedblockchain.MemberConfiguration, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Description=NOTHING, MemberFrameworkConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Description=Description, 
         MemberFrameworkConfiguration=MemberFrameworkConfiguration, **kwargs)
        (super(MemberConfiguration, self).__init__)(**processed_kwargs)


class NetworkFabricConfiguration(troposphere.managedblockchain.NetworkFabricConfiguration, Mixin):

    def __init__(self, title=None, Edition=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Edition=Edition, **kwargs)
        (super(NetworkFabricConfiguration, self).__init__)(**processed_kwargs)


class NetworkFrameworkConfiguration(troposphere.managedblockchain.NetworkFrameworkConfiguration, Mixin):

    def __init__(self, title=None, NetworkFabricConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         NetworkFabricConfiguration=NetworkFabricConfiguration, **kwargs)
        (super(NetworkFrameworkConfiguration, self).__init__)(**processed_kwargs)


class ApprovalThresholdPolicy(troposphere.managedblockchain.ApprovalThresholdPolicy, Mixin):

    def __init__(self, title=None, ProposalDurationInHours=NOTHING, ThresholdComparator=NOTHING, ThresholdPercentage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ProposalDurationInHours=ProposalDurationInHours, 
         ThresholdComparator=ThresholdComparator, 
         ThresholdPercentage=ThresholdPercentage, **kwargs)
        (super(ApprovalThresholdPolicy, self).__init__)(**processed_kwargs)


class VotingPolicy(troposphere.managedblockchain.VotingPolicy, Mixin):

    def __init__(self, title=None, ApprovalThresholdPolicy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ApprovalThresholdPolicy=ApprovalThresholdPolicy, **kwargs)
        (super(VotingPolicy, self).__init__)(**processed_kwargs)


class NetworkConfiguration(troposphere.managedblockchain.NetworkConfiguration, Mixin):

    def __init__(self, title=None, Framework=REQUIRED, FrameworkVersion=REQUIRED, Name=REQUIRED, VotingPolicy=REQUIRED, Description=NOTHING, NetworkFrameworkConfiguration=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Framework=Framework, 
         FrameworkVersion=FrameworkVersion, 
         Name=Name, 
         VotingPolicy=VotingPolicy, 
         Description=Description, 
         NetworkFrameworkConfiguration=NetworkFrameworkConfiguration, **kwargs)
        (super(NetworkConfiguration, self).__init__)(**processed_kwargs)


class Member(troposphere.managedblockchain.Member, Mixin):

    def __init__(self, title, template=None, validation=True, MemberConfiguration=REQUIRED, InvitationId=NOTHING, NetworkConfiguration=NOTHING, NetworkId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MemberConfiguration=MemberConfiguration, 
         InvitationId=InvitationId, 
         NetworkConfiguration=NetworkConfiguration, 
         NetworkId=NetworkId, **kwargs)
        (super(Member, self).__init__)(**processed_kwargs)


class NodeConfiguration(troposphere.managedblockchain.NodeConfiguration, Mixin):

    def __init__(self, title=None, AvailabilityZone=REQUIRED, InstanceType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AvailabilityZone=AvailabilityZone, 
         InstanceType=InstanceType, **kwargs)
        (super(NodeConfiguration, self).__init__)(**processed_kwargs)


class Node(troposphere.managedblockchain.Node, Mixin):

    def __init__(self, title, template=None, validation=True, MemberId=REQUIRED, NetworkId=REQUIRED, NodeConfiguration=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MemberId=MemberId, 
         NetworkId=NetworkId, 
         NodeConfiguration=NodeConfiguration, **kwargs)
        (super(Node, self).__init__)(**processed_kwargs)
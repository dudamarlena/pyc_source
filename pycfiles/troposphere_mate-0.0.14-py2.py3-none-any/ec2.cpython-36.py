# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/ec2.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 101757 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.ec2
from troposphere.ec2 import AssociationParameters as _AssociationParameters, BlockDeviceMapping as _BlockDeviceMapping, CertificateAuthenticationRequest as _CertificateAuthenticationRequest, ClassicLoadBalancer as _ClassicLoadBalancer, ClassicLoadBalancersConfig as _ClassicLoadBalancersConfig, ClientAuthenticationRequest as _ClientAuthenticationRequest, ConnectionLogOptions as _ConnectionLogOptions, CpuOptions as _CpuOptions, CreditSpecification as _CreditSpecification, DirectoryServiceAuthenticationRequest as _DirectoryServiceAuthenticationRequest, EBSBlockDevice as _EBSBlockDevice, ElasticGpuSpecification as _ElasticGpuSpecification, ElasticInferenceAccelerator as _ElasticInferenceAccelerator, FleetLaunchTemplateConfigRequest as _FleetLaunchTemplateConfigRequest, FleetLaunchTemplateOverridesRequest as _FleetLaunchTemplateOverridesRequest, FleetLaunchTemplateSpecificationRequest as _FleetLaunchTemplateSpecificationRequest, ICMP as _ICMP, IamInstanceProfile as _IamInstanceProfile, InstanceMarketOptions as _InstanceMarketOptions, Ipv6Addresses as _Ipv6Addresses, LaunchSpecifications as _LaunchSpecifications, LaunchTemplateConfigs as _LaunchTemplateConfigs, LaunchTemplateCreditSpecification as _LaunchTemplateCreditSpecification, LaunchTemplateData as _LaunchTemplateData, LaunchTemplateOverrides as _LaunchTemplateOverrides, LaunchTemplateSpecification as _LaunchTemplateSpecification, LicenseSpecification as _LicenseSpecification, LoadBalancersConfig as _LoadBalancersConfig, Monitoring as _Monitoring, NetworkInterfaceProperty as _NetworkInterfaceProperty, NetworkInterfaces as _NetworkInterfaces, OnDemandOptionsRequest as _OnDemandOptionsRequest, Placement as _Placement, PortRange as _PortRange, PrivateIpAddressSpecification as _PrivateIpAddressSpecification, SecurityGroups as _SecurityGroups, SpotFleetRequestConfigData as _SpotFleetRequestConfigData, SpotFleetTagSpecification as _SpotFleetTagSpecification, SpotOptions as _SpotOptions, SpotOptionsRequest as _SpotOptionsRequest, SsmAssociations as _SsmAssociations, TagSpecifications as _TagSpecifications, Tags as _Tags, TargetCapacitySpecificationRequest as _TargetCapacitySpecificationRequest, TargetGroup as _TargetGroup, TargetGroupConfig as _TargetGroupConfig, TrafficMirrorPortRange as _TrafficMirrorPortRange, VpnTunnelOptionsSpecification as _VpnTunnelOptionsSpecification
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Tag(troposphere.ec2.Tag, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(Tag, self).__init__)(**processed_kwargs)


class CustomerGateway(troposphere.ec2.CustomerGateway, Mixin):

    def __init__(self, title, template=None, validation=True, BgpAsn=REQUIRED, IpAddress=REQUIRED, Type=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         BgpAsn=BgpAsn, 
         IpAddress=IpAddress, 
         Type=Type, 
         Tags=Tags, **kwargs)
        (super(CustomerGateway, self).__init__)(**processed_kwargs)


class DHCPOptions(troposphere.ec2.DHCPOptions, Mixin):

    def __init__(self, title, template=None, validation=True, DomainName=NOTHING, DomainNameServers=NOTHING, NetbiosNameServers=NOTHING, NetbiosNodeType=NOTHING, NtpServers=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DomainName=DomainName, 
         DomainNameServers=DomainNameServers, 
         NetbiosNameServers=NetbiosNameServers, 
         NetbiosNodeType=NetbiosNodeType, 
         NtpServers=NtpServers, 
         Tags=Tags, **kwargs)
        (super(DHCPOptions, self).__init__)(**processed_kwargs)


class EgressOnlyInternetGateway(troposphere.ec2.EgressOnlyInternetGateway, Mixin):

    def __init__(self, title, template=None, validation=True, VpcId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         VpcId=VpcId, **kwargs)
        (super(EgressOnlyInternetGateway, self).__init__)(**processed_kwargs)


class EIP(troposphere.ec2.EIP, Mixin):

    def __init__(self, title, template=None, validation=True, InstanceId=NOTHING, Domain=NOTHING, PublicIpv4Pool=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InstanceId=InstanceId, 
         Domain=Domain, 
         PublicIpv4Pool=PublicIpv4Pool, 
         Tags=Tags, **kwargs)
        (super(EIP, self).__init__)(**processed_kwargs)


class EIPAssociation(troposphere.ec2.EIPAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, AllocationId=NOTHING, EIP=NOTHING, InstanceId=NOTHING, NetworkInterfaceId=NOTHING, PrivateIpAddress=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AllocationId=AllocationId, 
         EIP=EIP, 
         InstanceId=InstanceId, 
         NetworkInterfaceId=NetworkInterfaceId, 
         PrivateIpAddress=PrivateIpAddress, **kwargs)
        (super(EIPAssociation, self).__init__)(**processed_kwargs)


class FlowLog(troposphere.ec2.FlowLog, Mixin):

    def __init__(self, title, template=None, validation=True, ResourceId=REQUIRED, ResourceType=REQUIRED, TrafficType=REQUIRED, DeliverLogsPermissionArn=NOTHING, LogDestination=NOTHING, LogDestinationType=NOTHING, LogGroupName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ResourceId=ResourceId, 
         ResourceType=ResourceType, 
         TrafficType=TrafficType, 
         DeliverLogsPermissionArn=DeliverLogsPermissionArn, 
         LogDestination=LogDestination, 
         LogDestinationType=LogDestinationType, 
         LogGroupName=LogGroupName, **kwargs)
        (super(FlowLog, self).__init__)(**processed_kwargs)


class NatGateway(troposphere.ec2.NatGateway, Mixin):

    def __init__(self, title, template=None, validation=True, AllocationId=REQUIRED, SubnetId=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AllocationId=AllocationId, 
         SubnetId=SubnetId, 
         Tags=Tags, **kwargs)
        (super(NatGateway, self).__init__)(**processed_kwargs)


class EBSBlockDevice(troposphere.ec2.EBSBlockDevice, Mixin):

    def __init__(self, title=None, DeleteOnTermination=NOTHING, Encrypted=NOTHING, KmsKeyId=NOTHING, Iops=NOTHING, SnapshotId=NOTHING, VolumeSize=NOTHING, VolumeType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeleteOnTermination=DeleteOnTermination, 
         Encrypted=Encrypted, 
         KmsKeyId=KmsKeyId, 
         Iops=Iops, 
         SnapshotId=SnapshotId, 
         VolumeSize=VolumeSize, 
         VolumeType=VolumeType, **kwargs)
        (super(EBSBlockDevice, self).__init__)(**processed_kwargs)


class BlockDeviceMapping(troposphere.ec2.BlockDeviceMapping, Mixin):

    def __init__(self, title=None, DeviceName=REQUIRED, Ebs=NOTHING, NoDevice=NOTHING, VirtualName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeviceName=DeviceName, 
         Ebs=Ebs, 
         NoDevice=NoDevice, 
         VirtualName=VirtualName, **kwargs)
        (super(BlockDeviceMapping, self).__init__)(**processed_kwargs)


class MountPoint(troposphere.ec2.MountPoint, Mixin):

    def __init__(self, title=None, Device=REQUIRED, VolumeId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Device=Device, 
         VolumeId=VolumeId, **kwargs)
        (super(MountPoint, self).__init__)(**processed_kwargs)


class Placement(troposphere.ec2.Placement, Mixin):

    def __init__(self, title=None, Affinity=NOTHING, AvailabilityZone=NOTHING, GroupName=NOTHING, HostId=NOTHING, Tenancy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Affinity=Affinity, 
         AvailabilityZone=AvailabilityZone, 
         GroupName=GroupName, 
         HostId=HostId, 
         Tenancy=Tenancy, **kwargs)
        (super(Placement, self).__init__)(**processed_kwargs)


class CpuOptions(troposphere.ec2.CpuOptions, Mixin):

    def __init__(self, title=None, CoreCount=NOTHING, ThreadsPerCore=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CoreCount=CoreCount, 
         ThreadsPerCore=ThreadsPerCore, **kwargs)
        (super(CpuOptions, self).__init__)(**processed_kwargs)


class CreditSpecification(troposphere.ec2.CreditSpecification, Mixin):

    def __init__(self, title=None, CPUCredits=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CPUCredits=CPUCredits, **kwargs)
        (super(CreditSpecification, self).__init__)(**processed_kwargs)


class ElasticGpuSpecification(troposphere.ec2.ElasticGpuSpecification, Mixin):

    def __init__(self, title=None, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, **kwargs)
        (super(ElasticGpuSpecification, self).__init__)(**processed_kwargs)


class LaunchTemplateSpecification(troposphere.ec2.LaunchTemplateSpecification, Mixin):

    def __init__(self, title=None, Version=REQUIRED, LaunchTemplateId=NOTHING, LaunchTemplateName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Version=Version, 
         LaunchTemplateId=LaunchTemplateId, 
         LaunchTemplateName=LaunchTemplateName, **kwargs)
        (super(LaunchTemplateSpecification, self).__init__)(**processed_kwargs)


class PrivateIpAddressSpecification(troposphere.ec2.PrivateIpAddressSpecification, Mixin):

    def __init__(self, title=None, Primary=REQUIRED, PrivateIpAddress=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Primary=Primary, 
         PrivateIpAddress=PrivateIpAddress, **kwargs)
        (super(PrivateIpAddressSpecification, self).__init__)(**processed_kwargs)


class NetworkInterfaceProperty(troposphere.ec2.NetworkInterfaceProperty, Mixin):

    def __init__(self, title=None, DeviceIndex=REQUIRED, AssociatePublicIpAddress=NOTHING, DeleteOnTermination=NOTHING, Description=NOTHING, GroupSet=NOTHING, NetworkInterfaceId=NOTHING, Ipv6AddressCount=NOTHING, Ipv6Addresses=NOTHING, PrivateIpAddress=NOTHING, PrivateIpAddresses=NOTHING, SecondaryPrivateIpAddressCount=NOTHING, SubnetId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeviceIndex=DeviceIndex, 
         AssociatePublicIpAddress=AssociatePublicIpAddress, 
         DeleteOnTermination=DeleteOnTermination, 
         Description=Description, 
         GroupSet=GroupSet, 
         NetworkInterfaceId=NetworkInterfaceId, 
         Ipv6AddressCount=Ipv6AddressCount, 
         Ipv6Addresses=Ipv6Addresses, 
         PrivateIpAddress=PrivateIpAddress, 
         PrivateIpAddresses=PrivateIpAddresses, 
         SecondaryPrivateIpAddressCount=SecondaryPrivateIpAddressCount, 
         SubnetId=SubnetId, **kwargs)
        (super(NetworkInterfaceProperty, self).__init__)(**processed_kwargs)


class AssociationParameters(troposphere.ec2.AssociationParameters, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(AssociationParameters, self).__init__)(**processed_kwargs)


class SsmAssociations(troposphere.ec2.SsmAssociations, Mixin):

    def __init__(self, title=None, DocumentName=REQUIRED, AssociationParameters=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DocumentName=DocumentName, 
         AssociationParameters=AssociationParameters, **kwargs)
        (super(SsmAssociations, self).__init__)(**processed_kwargs)


class Host(troposphere.ec2.Host, Mixin):

    def __init__(self, title, template=None, validation=True, AvailabilityZone=REQUIRED, InstanceType=REQUIRED, AutoPlacement=NOTHING, HostRecovery=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AvailabilityZone=AvailabilityZone, 
         InstanceType=InstanceType, 
         AutoPlacement=AutoPlacement, 
         HostRecovery=HostRecovery, **kwargs)
        (super(Host, self).__init__)(**processed_kwargs)


class ElasticInferenceAccelerator(troposphere.ec2.ElasticInferenceAccelerator, Mixin):

    def __init__(self, title=None, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, **kwargs)
        (super(ElasticInferenceAccelerator, self).__init__)(**processed_kwargs)


class LicenseSpecification(troposphere.ec2.LicenseSpecification, Mixin):

    def __init__(self, title=None, LicenseConfigurationArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LicenseConfigurationArn=LicenseConfigurationArn, **kwargs)
        (super(LicenseSpecification, self).__init__)(**processed_kwargs)


class Instance(troposphere.ec2.Instance, Mixin):

    def __init__(self, title, template, validation, Affinity, AvailabilityZone, BlockDeviceMappings, CpuOptions, CreditSpecification, DisableApiTermination, EbsOptimized, ElasticGpuSpecifications, ElasticInferenceAccelerators, HostId, IamInstanceProfile, ImageId, InstanceInitiatedShutdownBehavior, InstanceType, Ipv6AddressCount, Ipv6Addresses, KernelId, KeyName, LaunchTemplate, LicenseSpecifications, Monitoring, NetworkInterfaces, PlacementGroupName, PrivateIpAddress, RamdiskId, SecurityGroupIds, SecurityGroups, SsmAssociations, SourceDestCheck, SubnetId=NoneTrueNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHINGNOTHING, Tags=NOTHING, Tenancy=NOTHING, UserData=NOTHING, Volumes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Affinity=Affinity, 
         AvailabilityZone=AvailabilityZone, 
         BlockDeviceMappings=BlockDeviceMappings, 
         CpuOptions=CpuOptions, 
         CreditSpecification=CreditSpecification, 
         DisableApiTermination=DisableApiTermination, 
         EbsOptimized=EbsOptimized, 
         ElasticGpuSpecifications=ElasticGpuSpecifications, 
         ElasticInferenceAccelerators=ElasticInferenceAccelerators, 
         HostId=HostId, 
         IamInstanceProfile=IamInstanceProfile, 
         ImageId=ImageId, 
         InstanceInitiatedShutdownBehavior=InstanceInitiatedShutdownBehavior, 
         InstanceType=InstanceType, 
         Ipv6AddressCount=Ipv6AddressCount, 
         Ipv6Addresses=Ipv6Addresses, 
         KernelId=KernelId, 
         KeyName=KeyName, 
         LaunchTemplate=LaunchTemplate, 
         LicenseSpecifications=LicenseSpecifications, 
         Monitoring=Monitoring, 
         NetworkInterfaces=NetworkInterfaces, 
         PlacementGroupName=PlacementGroupName, 
         PrivateIpAddress=PrivateIpAddress, 
         RamdiskId=RamdiskId, 
         SecurityGroupIds=SecurityGroupIds, 
         SecurityGroups=SecurityGroups, 
         SsmAssociations=SsmAssociations, 
         SourceDestCheck=SourceDestCheck, 
         SubnetId=SubnetId, 
         Tags=Tags, 
         Tenancy=Tenancy, 
         UserData=UserData, 
         Volumes=Volumes, **kwargs)
        (super(Instance, self).__init__)(**processed_kwargs)


class InternetGateway(troposphere.ec2.InternetGateway, Mixin):

    def __init__(self, title, template=None, validation=True, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Tags=Tags, **kwargs)
        (super(InternetGateway, self).__init__)(**processed_kwargs)


class NetworkAcl(troposphere.ec2.NetworkAcl, Mixin):

    def __init__(self, title, template=None, validation=True, VpcId=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         VpcId=VpcId, 
         Tags=Tags, **kwargs)
        (super(NetworkAcl, self).__init__)(**processed_kwargs)


class ICMP(troposphere.ec2.ICMP, Mixin):

    def __init__(self, title=None, Code=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Code=Code, 
         Type=Type, **kwargs)
        (super(ICMP, self).__init__)(**processed_kwargs)


class PortRange(troposphere.ec2.PortRange, Mixin):

    def __init__(self, title=None, From=NOTHING, To=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         From=From, 
         To=To, **kwargs)
        (super(PortRange, self).__init__)(**processed_kwargs)


class NetworkAclEntry(troposphere.ec2.NetworkAclEntry, Mixin):

    def __init__(self, title, template=None, validation=True, NetworkAclId=REQUIRED, Protocol=REQUIRED, RuleAction=REQUIRED, RuleNumber=REQUIRED, CidrBlock=NOTHING, Egress=NOTHING, Icmp=NOTHING, Ipv6CidrBlock=NOTHING, PortRange=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         NetworkAclId=NetworkAclId, 
         Protocol=Protocol, 
         RuleAction=RuleAction, 
         RuleNumber=RuleNumber, 
         CidrBlock=CidrBlock, 
         Egress=Egress, 
         Icmp=Icmp, 
         Ipv6CidrBlock=Ipv6CidrBlock, 
         PortRange=PortRange, **kwargs)
        (super(NetworkAclEntry, self).__init__)(**processed_kwargs)


class NetworkInterface(troposphere.ec2.NetworkInterface, Mixin):

    def __init__(self, title, template=None, validation=True, SubnetId=REQUIRED, Description=NOTHING, GroupSet=NOTHING, Ipv6AddressCount=NOTHING, Ipv6Addresses=NOTHING, PrivateIpAddress=NOTHING, PrivateIpAddresses=NOTHING, SecondaryPrivateIpAddressCount=NOTHING, SourceDestCheck=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SubnetId=SubnetId, 
         Description=Description, 
         GroupSet=GroupSet, 
         Ipv6AddressCount=Ipv6AddressCount, 
         Ipv6Addresses=Ipv6Addresses, 
         PrivateIpAddress=PrivateIpAddress, 
         PrivateIpAddresses=PrivateIpAddresses, 
         SecondaryPrivateIpAddressCount=SecondaryPrivateIpAddressCount, 
         SourceDestCheck=SourceDestCheck, 
         Tags=Tags, **kwargs)
        (super(NetworkInterface, self).__init__)(**processed_kwargs)


class NetworkInterfaceAttachment(troposphere.ec2.NetworkInterfaceAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, DeviceIndex=REQUIRED, InstanceId=REQUIRED, NetworkInterfaceId=REQUIRED, DeleteOnTermination=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DeviceIndex=DeviceIndex, 
         InstanceId=InstanceId, 
         NetworkInterfaceId=NetworkInterfaceId, 
         DeleteOnTermination=DeleteOnTermination, **kwargs)
        (super(NetworkInterfaceAttachment, self).__init__)(**processed_kwargs)


class NetworkInterfacePermission(troposphere.ec2.NetworkInterfacePermission, Mixin):

    def __init__(self, title, template=None, validation=True, AwsAccountId=REQUIRED, NetworkInterfaceId=REQUIRED, Permission=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AwsAccountId=AwsAccountId, 
         NetworkInterfaceId=NetworkInterfaceId, 
         Permission=Permission, **kwargs)
        (super(NetworkInterfacePermission, self).__init__)(**processed_kwargs)


class Route(troposphere.ec2.Route, Mixin):

    def __init__(self, title, template=None, validation=True, RouteTableId=REQUIRED, DestinationCidrBlock=NOTHING, DestinationIpv6CidrBlock=NOTHING, EgressOnlyInternetGatewayId=NOTHING, GatewayId=NOTHING, InstanceId=NOTHING, NatGatewayId=NOTHING, NetworkInterfaceId=NOTHING, TransitGatewayId=NOTHING, VpcPeeringConnectionId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RouteTableId=RouteTableId, 
         DestinationCidrBlock=DestinationCidrBlock, 
         DestinationIpv6CidrBlock=DestinationIpv6CidrBlock, 
         EgressOnlyInternetGatewayId=EgressOnlyInternetGatewayId, 
         GatewayId=GatewayId, 
         InstanceId=InstanceId, 
         NatGatewayId=NatGatewayId, 
         NetworkInterfaceId=NetworkInterfaceId, 
         TransitGatewayId=TransitGatewayId, 
         VpcPeeringConnectionId=VpcPeeringConnectionId, **kwargs)
        (super(Route, self).__init__)(**processed_kwargs)


class RouteTable(troposphere.ec2.RouteTable, Mixin):

    def __init__(self, title, template=None, validation=True, VpcId=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         VpcId=VpcId, 
         Tags=Tags, **kwargs)
        (super(RouteTable, self).__init__)(**processed_kwargs)


class SecurityGroupEgress(troposphere.ec2.SecurityGroupEgress, Mixin):

    def __init__(self, title, template=None, validation=True, GroupId=REQUIRED, IpProtocol=REQUIRED, CidrIp=NOTHING, CidrIpv6=NOTHING, Description=NOTHING, DestinationPrefixListId=NOTHING, DestinationSecurityGroupId=NOTHING, FromPort=NOTHING, ToPort=NOTHING, SourceSecurityGroupId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GroupId=GroupId, 
         IpProtocol=IpProtocol, 
         CidrIp=CidrIp, 
         CidrIpv6=CidrIpv6, 
         Description=Description, 
         DestinationPrefixListId=DestinationPrefixListId, 
         DestinationSecurityGroupId=DestinationSecurityGroupId, 
         FromPort=FromPort, 
         ToPort=ToPort, 
         SourceSecurityGroupId=SourceSecurityGroupId, **kwargs)
        (super(SecurityGroupEgress, self).__init__)(**processed_kwargs)


class SecurityGroupIngress(troposphere.ec2.SecurityGroupIngress, Mixin):

    def __init__(self, title, template=None, validation=True, IpProtocol=REQUIRED, CidrIp=NOTHING, CidrIpv6=NOTHING, Description=NOTHING, FromPort=NOTHING, GroupName=NOTHING, GroupId=NOTHING, SourceSecurityGroupName=NOTHING, SourceSecurityGroupId=NOTHING, SourceSecurityGroupOwnerId=NOTHING, ToPort=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         IpProtocol=IpProtocol, 
         CidrIp=CidrIp, 
         CidrIpv6=CidrIpv6, 
         Description=Description, 
         FromPort=FromPort, 
         GroupName=GroupName, 
         GroupId=GroupId, 
         SourceSecurityGroupName=SourceSecurityGroupName, 
         SourceSecurityGroupId=SourceSecurityGroupId, 
         SourceSecurityGroupOwnerId=SourceSecurityGroupOwnerId, 
         ToPort=ToPort, **kwargs)
        (super(SecurityGroupIngress, self).__init__)(**processed_kwargs)


class SecurityGroupRule(troposphere.ec2.SecurityGroupRule, Mixin):

    def __init__(self, title=None, IpProtocol=REQUIRED, CidrIp=NOTHING, CidrIpv6=NOTHING, Description=NOTHING, DestinationPrefixListId=NOTHING, DestinationSecurityGroupId=NOTHING, FromPort=NOTHING, SourceSecurityGroupId=NOTHING, SourceSecurityGroupName=NOTHING, SourceSecurityGroupOwnerId=NOTHING, ToPort=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IpProtocol=IpProtocol, 
         CidrIp=CidrIp, 
         CidrIpv6=CidrIpv6, 
         Description=Description, 
         DestinationPrefixListId=DestinationPrefixListId, 
         DestinationSecurityGroupId=DestinationSecurityGroupId, 
         FromPort=FromPort, 
         SourceSecurityGroupId=SourceSecurityGroupId, 
         SourceSecurityGroupName=SourceSecurityGroupName, 
         SourceSecurityGroupOwnerId=SourceSecurityGroupOwnerId, 
         ToPort=ToPort, **kwargs)
        (super(SecurityGroupRule, self).__init__)(**processed_kwargs)


class SecurityGroup(troposphere.ec2.SecurityGroup, Mixin):

    def __init__(self, title, template=None, validation=True, GroupDescription=REQUIRED, GroupName=NOTHING, SecurityGroupEgress=NOTHING, SecurityGroupIngress=NOTHING, VpcId=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         GroupDescription=GroupDescription, 
         GroupName=GroupName, 
         SecurityGroupEgress=SecurityGroupEgress, 
         SecurityGroupIngress=SecurityGroupIngress, 
         VpcId=VpcId, 
         Tags=Tags, **kwargs)
        (super(SecurityGroup, self).__init__)(**processed_kwargs)


class Subnet(troposphere.ec2.Subnet, Mixin):

    def __init__(self, title, template=None, validation=True, CidrBlock=REQUIRED, VpcId=REQUIRED, AssignIpv6AddressOnCreation=NOTHING, AvailabilityZone=NOTHING, Ipv6CidrBlock=NOTHING, MapPublicIpOnLaunch=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CidrBlock=CidrBlock, 
         VpcId=VpcId, 
         AssignIpv6AddressOnCreation=AssignIpv6AddressOnCreation, 
         AvailabilityZone=AvailabilityZone, 
         Ipv6CidrBlock=Ipv6CidrBlock, 
         MapPublicIpOnLaunch=MapPublicIpOnLaunch, 
         Tags=Tags, **kwargs)
        (super(Subnet, self).__init__)(**processed_kwargs)


class SubnetNetworkAclAssociation(troposphere.ec2.SubnetNetworkAclAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, SubnetId=REQUIRED, NetworkAclId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SubnetId=SubnetId, 
         NetworkAclId=NetworkAclId, **kwargs)
        (super(SubnetNetworkAclAssociation, self).__init__)(**processed_kwargs)


class SubnetRouteTableAssociation(troposphere.ec2.SubnetRouteTableAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, RouteTableId=REQUIRED, SubnetId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RouteTableId=RouteTableId, 
         SubnetId=SubnetId, **kwargs)
        (super(SubnetRouteTableAssociation, self).__init__)(**processed_kwargs)


class Volume(troposphere.ec2.Volume, Mixin):

    def __init__(self, title, template=None, validation=True, AvailabilityZone=REQUIRED, AutoEnableIO=NOTHING, Encrypted=NOTHING, Iops=NOTHING, KmsKeyId=NOTHING, Size=NOTHING, SnapshotId=NOTHING, Tags=NOTHING, VolumeType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AvailabilityZone=AvailabilityZone, 
         AutoEnableIO=AutoEnableIO, 
         Encrypted=Encrypted, 
         Iops=Iops, 
         KmsKeyId=KmsKeyId, 
         Size=Size, 
         SnapshotId=SnapshotId, 
         Tags=Tags, 
         VolumeType=VolumeType, **kwargs)
        (super(Volume, self).__init__)(**processed_kwargs)


class VolumeAttachment(troposphere.ec2.VolumeAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, Device=REQUIRED, InstanceId=REQUIRED, VolumeId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Device=Device, 
         InstanceId=InstanceId, 
         VolumeId=VolumeId, **kwargs)
        (super(VolumeAttachment, self).__init__)(**processed_kwargs)


class VPC(troposphere.ec2.VPC, Mixin):

    def __init__(self, title, template=None, validation=True, CidrBlock=REQUIRED, EnableDnsSupport=NOTHING, EnableDnsHostnames=NOTHING, InstanceTenancy=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CidrBlock=CidrBlock, 
         EnableDnsSupport=EnableDnsSupport, 
         EnableDnsHostnames=EnableDnsHostnames, 
         InstanceTenancy=InstanceTenancy, 
         Tags=Tags, **kwargs)
        (super(VPC, self).__init__)(**processed_kwargs)


class VPCDHCPOptionsAssociation(troposphere.ec2.VPCDHCPOptionsAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, DhcpOptionsId=REQUIRED, VpcId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DhcpOptionsId=DhcpOptionsId, 
         VpcId=VpcId, **kwargs)
        (super(VPCDHCPOptionsAssociation, self).__init__)(**processed_kwargs)


class VPCEndpoint(troposphere.ec2.VPCEndpoint, Mixin):

    def __init__(self, title, template=None, validation=True, ServiceName=REQUIRED, VpcId=REQUIRED, PolicyDocument=NOTHING, PrivateDnsEnabled=NOTHING, RouteTableIds=NOTHING, SecurityGroupIds=NOTHING, SubnetIds=NOTHING, VpcEndpointType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ServiceName=ServiceName, 
         VpcId=VpcId, 
         PolicyDocument=PolicyDocument, 
         PrivateDnsEnabled=PrivateDnsEnabled, 
         RouteTableIds=RouteTableIds, 
         SecurityGroupIds=SecurityGroupIds, 
         SubnetIds=SubnetIds, 
         VpcEndpointType=VpcEndpointType, **kwargs)
        (super(VPCEndpoint, self).__init__)(**processed_kwargs)


class VPCEndpointConnectionNotification(troposphere.ec2.VPCEndpointConnectionNotification, Mixin):

    def __init__(self, title, template=None, validation=True, ConnectionEvents=REQUIRED, ConnectionNotificationArn=REQUIRED, ServiceId=NOTHING, VPCEndpointId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ConnectionEvents=ConnectionEvents, 
         ConnectionNotificationArn=ConnectionNotificationArn, 
         ServiceId=ServiceId, 
         VPCEndpointId=VPCEndpointId, **kwargs)
        (super(VPCEndpointConnectionNotification, self).__init__)(**processed_kwargs)


class VPCEndpointService(troposphere.ec2.VPCEndpointService, Mixin):

    def __init__(self, title, template=None, validation=True, NetworkLoadBalancerArns=REQUIRED, AcceptanceRequired=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         NetworkLoadBalancerArns=NetworkLoadBalancerArns, 
         AcceptanceRequired=AcceptanceRequired, **kwargs)
        (super(VPCEndpointService, self).__init__)(**processed_kwargs)


class VPCEndpointServicePermissions(troposphere.ec2.VPCEndpointServicePermissions, Mixin):

    def __init__(self, title, template=None, validation=True, ServiceId=REQUIRED, AllowedPrincipals=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ServiceId=ServiceId, 
         AllowedPrincipals=AllowedPrincipals, **kwargs)
        (super(VPCEndpointServicePermissions, self).__init__)(**processed_kwargs)


class VPCGatewayAttachment(troposphere.ec2.VPCGatewayAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, VpcId=REQUIRED, InternetGatewayId=NOTHING, VpnGatewayId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         VpcId=VpcId, 
         InternetGatewayId=InternetGatewayId, 
         VpnGatewayId=VpnGatewayId, **kwargs)
        (super(VPCGatewayAttachment, self).__init__)(**processed_kwargs)


class VpnTunnelOptionsSpecification(troposphere.ec2.VpnTunnelOptionsSpecification, Mixin):

    def __init__(self, title=None, PreSharedKey=NOTHING, TunnelInsideCidr=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         PreSharedKey=PreSharedKey, 
         TunnelInsideCidr=TunnelInsideCidr, **kwargs)
        (super(VpnTunnelOptionsSpecification, self).__init__)(**processed_kwargs)


class VPNConnection(troposphere.ec2.VPNConnection, Mixin):

    def __init__(self, title, template=None, validation=True, CustomerGatewayId=REQUIRED, Type=REQUIRED, StaticRoutesOnly=NOTHING, Tags=NOTHING, TransitGatewayId=NOTHING, VpnGatewayId=NOTHING, VpnTunnelOptionsSpecifications=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CustomerGatewayId=CustomerGatewayId, 
         Type=Type, 
         StaticRoutesOnly=StaticRoutesOnly, 
         Tags=Tags, 
         TransitGatewayId=TransitGatewayId, 
         VpnGatewayId=VpnGatewayId, 
         VpnTunnelOptionsSpecifications=VpnTunnelOptionsSpecifications, **kwargs)
        (super(VPNConnection, self).__init__)(**processed_kwargs)


class VPNConnectionRoute(troposphere.ec2.VPNConnectionRoute, Mixin):

    def __init__(self, title, template=None, validation=True, DestinationCidrBlock=REQUIRED, VpnConnectionId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DestinationCidrBlock=DestinationCidrBlock, 
         VpnConnectionId=VpnConnectionId, **kwargs)
        (super(VPNConnectionRoute, self).__init__)(**processed_kwargs)


class VPNGateway(troposphere.ec2.VPNGateway, Mixin):

    def __init__(self, title, template=None, validation=True, Type=REQUIRED, AmazonSideAsn=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Type=Type, 
         AmazonSideAsn=AmazonSideAsn, 
         Tags=Tags, **kwargs)
        (super(VPNGateway, self).__init__)(**processed_kwargs)


class VPNGatewayRoutePropagation(troposphere.ec2.VPNGatewayRoutePropagation, Mixin):

    def __init__(self, title, template=None, validation=True, RouteTableIds=REQUIRED, VpnGatewayId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RouteTableIds=RouteTableIds, 
         VpnGatewayId=VpnGatewayId, **kwargs)
        (super(VPNGatewayRoutePropagation, self).__init__)(**processed_kwargs)


class VPCPeeringConnection(troposphere.ec2.VPCPeeringConnection, Mixin):

    def __init__(self, title, template=None, validation=True, PeerVpcId=REQUIRED, VpcId=REQUIRED, Tags=NOTHING, PeerRegion=NOTHING, PeerOwnerId=NOTHING, PeerRoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PeerVpcId=PeerVpcId, 
         VpcId=VpcId, 
         Tags=Tags, 
         PeerRegion=PeerRegion, 
         PeerOwnerId=PeerOwnerId, 
         PeerRoleArn=PeerRoleArn, **kwargs)
        (super(VPCPeeringConnection, self).__init__)(**processed_kwargs)


class Monitoring(troposphere.ec2.Monitoring, Mixin):

    def __init__(self, title=None, Enabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, **kwargs)
        (super(Monitoring, self).__init__)(**processed_kwargs)


class NetworkInterfaces(troposphere.ec2.NetworkInterfaces, Mixin):

    def __init__(self, title=None, DeviceIndex=REQUIRED, AssociatePublicIpAddress=NOTHING, DeleteOnTermination=NOTHING, Description=NOTHING, Groups=NOTHING, InterfaceType=NOTHING, Ipv6AddressCount=NOTHING, Ipv6Addresses=NOTHING, NetworkInterfaceId=NOTHING, PrivateIpAddresses=NOTHING, SecondaryPrivateIpAddressCount=NOTHING, SubnetId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeviceIndex=DeviceIndex, 
         AssociatePublicIpAddress=AssociatePublicIpAddress, 
         DeleteOnTermination=DeleteOnTermination, 
         Description=Description, 
         Groups=Groups, 
         InterfaceType=InterfaceType, 
         Ipv6AddressCount=Ipv6AddressCount, 
         Ipv6Addresses=Ipv6Addresses, 
         NetworkInterfaceId=NetworkInterfaceId, 
         PrivateIpAddresses=PrivateIpAddresses, 
         SecondaryPrivateIpAddressCount=SecondaryPrivateIpAddressCount, 
         SubnetId=SubnetId, **kwargs)
        (super(NetworkInterfaces, self).__init__)(**processed_kwargs)


class SecurityGroups(troposphere.ec2.SecurityGroups, Mixin):

    def __init__(self, title=None, GroupId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         GroupId=GroupId, **kwargs)
        (super(SecurityGroups, self).__init__)(**processed_kwargs)


class IamInstanceProfile(troposphere.ec2.IamInstanceProfile, Mixin):

    def __init__(self, title=None, Arn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Arn=Arn, **kwargs)
        (super(IamInstanceProfile, self).__init__)(**processed_kwargs)


class SpotFleetTagSpecification(troposphere.ec2.SpotFleetTagSpecification, Mixin):

    def __init__(self, title=None, ResourceType=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceType=ResourceType, 
         Tags=Tags, **kwargs)
        (super(SpotFleetTagSpecification, self).__init__)(**processed_kwargs)


class LaunchSpecifications(troposphere.ec2.LaunchSpecifications, Mixin):

    def __init__(self, title=None, ImageId=REQUIRED, InstanceType=REQUIRED, BlockDeviceMappings=NOTHING, EbsOptimized=NOTHING, IamInstanceProfile=NOTHING, KernelId=NOTHING, KeyName=NOTHING, Monitoring=NOTHING, NetworkInterfaces=NOTHING, Placement=NOTHING, RamdiskId=NOTHING, SecurityGroups=NOTHING, SpotPrice=NOTHING, SubnetId=NOTHING, TagSpecifications=NOTHING, UserData=NOTHING, WeightedCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ImageId=ImageId, 
         InstanceType=InstanceType, 
         BlockDeviceMappings=BlockDeviceMappings, 
         EbsOptimized=EbsOptimized, 
         IamInstanceProfile=IamInstanceProfile, 
         KernelId=KernelId, 
         KeyName=KeyName, 
         Monitoring=Monitoring, 
         NetworkInterfaces=NetworkInterfaces, 
         Placement=Placement, 
         RamdiskId=RamdiskId, 
         SecurityGroups=SecurityGroups, 
         SpotPrice=SpotPrice, 
         SubnetId=SubnetId, 
         TagSpecifications=TagSpecifications, 
         UserData=UserData, 
         WeightedCapacity=WeightedCapacity, **kwargs)
        (super(LaunchSpecifications, self).__init__)(**processed_kwargs)


class LaunchTemplateOverrides(troposphere.ec2.LaunchTemplateOverrides, Mixin):

    def __init__(self, title=None, AvailabilityZone=NOTHING, InstanceType=NOTHING, SpotPrice=NOTHING, SubnetId=NOTHING, WeightedCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AvailabilityZone=AvailabilityZone, 
         InstanceType=InstanceType, 
         SpotPrice=SpotPrice, 
         SubnetId=SubnetId, 
         WeightedCapacity=WeightedCapacity, **kwargs)
        (super(LaunchTemplateOverrides, self).__init__)(**processed_kwargs)


class LaunchTemplateConfigs(troposphere.ec2.LaunchTemplateConfigs, Mixin):

    def __init__(self, title=None, LaunchTemplateSpecification=REQUIRED, Overrides=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LaunchTemplateSpecification=LaunchTemplateSpecification, 
         Overrides=Overrides, **kwargs)
        (super(LaunchTemplateConfigs, self).__init__)(**processed_kwargs)


class ClassicLoadBalancer(troposphere.ec2.ClassicLoadBalancer, Mixin):

    def __init__(self, title=None, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, **kwargs)
        (super(ClassicLoadBalancer, self).__init__)(**processed_kwargs)


class ClassicLoadBalancersConfig(troposphere.ec2.ClassicLoadBalancersConfig, Mixin):

    def __init__(self, title=None, ClassicLoadBalancers=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClassicLoadBalancers=ClassicLoadBalancers, **kwargs)
        (super(ClassicLoadBalancersConfig, self).__init__)(**processed_kwargs)


class TargetGroup(troposphere.ec2.TargetGroup, Mixin):

    def __init__(self, title=None, Arn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Arn=Arn, **kwargs)
        (super(TargetGroup, self).__init__)(**processed_kwargs)


class TargetGroupConfig(troposphere.ec2.TargetGroupConfig, Mixin):

    def __init__(self, title=None, TargetGroups=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TargetGroups=TargetGroups, **kwargs)
        (super(TargetGroupConfig, self).__init__)(**processed_kwargs)


class LoadBalancersConfig(troposphere.ec2.LoadBalancersConfig, Mixin):

    def __init__(self, title=None, ClassicLoadBalancersConfig=NOTHING, TargetGroupsConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClassicLoadBalancersConfig=ClassicLoadBalancersConfig, 
         TargetGroupsConfig=TargetGroupsConfig, **kwargs)
        (super(LoadBalancersConfig, self).__init__)(**processed_kwargs)


class SpotFleetRequestConfigData(troposphere.ec2.SpotFleetRequestConfigData, Mixin):

    def __init__(self, title=None, IamFleetRole=REQUIRED, TargetCapacity=REQUIRED, AllocationStrategy=NOTHING, ExcessCapacityTerminationPolicy=NOTHING, InstanceInterruptionBehavior=NOTHING, LaunchSpecifications=NOTHING, LaunchTemplateConfigs=NOTHING, LoadBalancersConfig=NOTHING, ReplaceUnhealthyInstances=NOTHING, SpotPrice=NOTHING, TerminateInstancesWithExpiration=NOTHING, Type=NOTHING, ValidFrom=NOTHING, ValidUntil=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IamFleetRole=IamFleetRole, 
         TargetCapacity=TargetCapacity, 
         AllocationStrategy=AllocationStrategy, 
         ExcessCapacityTerminationPolicy=ExcessCapacityTerminationPolicy, 
         InstanceInterruptionBehavior=InstanceInterruptionBehavior, 
         LaunchSpecifications=LaunchSpecifications, 
         LaunchTemplateConfigs=LaunchTemplateConfigs, 
         LoadBalancersConfig=LoadBalancersConfig, 
         ReplaceUnhealthyInstances=ReplaceUnhealthyInstances, 
         SpotPrice=SpotPrice, 
         TerminateInstancesWithExpiration=TerminateInstancesWithExpiration, 
         Type=Type, 
         ValidFrom=ValidFrom, 
         ValidUntil=ValidUntil, **kwargs)
        (super(SpotFleetRequestConfigData, self).__init__)(**processed_kwargs)


class SpotFleet(troposphere.ec2.SpotFleet, Mixin):

    def __init__(self, title, template=None, validation=True, SpotFleetRequestConfigData=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SpotFleetRequestConfigData=SpotFleetRequestConfigData, **kwargs)
        (super(SpotFleet, self).__init__)(**processed_kwargs)


class PlacementGroup(troposphere.ec2.PlacementGroup, Mixin):

    def __init__(self, title, template=None, validation=True, Strategy=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Strategy=Strategy, **kwargs)
        (super(PlacementGroup, self).__init__)(**processed_kwargs)


class SubnetCidrBlock(troposphere.ec2.SubnetCidrBlock, Mixin):

    def __init__(self, title, template=None, validation=True, Ipv6CidrBlock=REQUIRED, SubnetId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Ipv6CidrBlock=Ipv6CidrBlock, 
         SubnetId=SubnetId, **kwargs)
        (super(SubnetCidrBlock, self).__init__)(**processed_kwargs)


class VPCCidrBlock(troposphere.ec2.VPCCidrBlock, Mixin):

    def __init__(self, title, template=None, validation=True, VpcId=REQUIRED, AmazonProvidedIpv6CidrBlock=NOTHING, CidrBlock=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         VpcId=VpcId, 
         AmazonProvidedIpv6CidrBlock=AmazonProvidedIpv6CidrBlock, 
         CidrBlock=CidrBlock, **kwargs)
        (super(VPCCidrBlock, self).__init__)(**processed_kwargs)


class TagSpecifications(troposphere.ec2.TagSpecifications, Mixin):

    def __init__(self, title=None, ResourceType=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ResourceType=ResourceType, 
         Tags=Tags, **kwargs)
        (super(TagSpecifications, self).__init__)(**processed_kwargs)


class SpotOptions(troposphere.ec2.SpotOptions, Mixin):

    def __init__(self, title=None, BlockDurationMinutes=NOTHING, InstanceInterruptionBehavior=NOTHING, MaxPrice=NOTHING, SpotInstanceType=NOTHING, ValidUntil=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BlockDurationMinutes=BlockDurationMinutes, 
         InstanceInterruptionBehavior=InstanceInterruptionBehavior, 
         MaxPrice=MaxPrice, 
         SpotInstanceType=SpotInstanceType, 
         ValidUntil=ValidUntil, **kwargs)
        (super(SpotOptions, self).__init__)(**processed_kwargs)


class InstanceMarketOptions(troposphere.ec2.InstanceMarketOptions, Mixin):

    def __init__(self, title=None, MarketType=NOTHING, SpotOptions=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MarketType=MarketType, 
         SpotOptions=SpotOptions, **kwargs)
        (super(InstanceMarketOptions, self).__init__)(**processed_kwargs)


class LaunchTemplateCreditSpecification(troposphere.ec2.LaunchTemplateCreditSpecification, Mixin):

    def __init__(self, title=None, CpuCredits=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         CpuCredits=CpuCredits, **kwargs)
        (super(LaunchTemplateCreditSpecification, self).__init__)(**processed_kwargs)


class LaunchTemplateData(troposphere.ec2.LaunchTemplateData, Mixin):

    def __init__(self, title=None, BlockDeviceMappings=NOTHING, CpuOptions=NOTHING, CreditSpecification=NOTHING, DisableApiTermination=NOTHING, EbsOptimized=NOTHING, ElasticGpuSpecifications=NOTHING, IamInstanceProfile=NOTHING, ImageId=NOTHING, InstanceInitiatedShutdownBehavior=NOTHING, InstanceMarketOptions=NOTHING, InstanceType=NOTHING, KernelId=NOTHING, KeyName=NOTHING, LicenseSpecifications=NOTHING, Monitoring=NOTHING, NetworkInterfaces=NOTHING, Placement=NOTHING, RamDiskId=NOTHING, SecurityGroups=NOTHING, SecurityGroupIds=NOTHING, TagSpecifications=NOTHING, UserData=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BlockDeviceMappings=BlockDeviceMappings, 
         CpuOptions=CpuOptions, 
         CreditSpecification=CreditSpecification, 
         DisableApiTermination=DisableApiTermination, 
         EbsOptimized=EbsOptimized, 
         ElasticGpuSpecifications=ElasticGpuSpecifications, 
         IamInstanceProfile=IamInstanceProfile, 
         ImageId=ImageId, 
         InstanceInitiatedShutdownBehavior=InstanceInitiatedShutdownBehavior, 
         InstanceMarketOptions=InstanceMarketOptions, 
         InstanceType=InstanceType, 
         KernelId=KernelId, 
         KeyName=KeyName, 
         LicenseSpecifications=LicenseSpecifications, 
         Monitoring=Monitoring, 
         NetworkInterfaces=NetworkInterfaces, 
         Placement=Placement, 
         RamDiskId=RamDiskId, 
         SecurityGroups=SecurityGroups, 
         SecurityGroupIds=SecurityGroupIds, 
         TagSpecifications=TagSpecifications, 
         UserData=UserData, **kwargs)
        (super(LaunchTemplateData, self).__init__)(**processed_kwargs)


class LaunchTemplate(troposphere.ec2.LaunchTemplate, Mixin):

    def __init__(self, title, template=None, validation=True, LaunchTemplateData=NOTHING, LaunchTemplateName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         LaunchTemplateData=LaunchTemplateData, 
         LaunchTemplateName=LaunchTemplateName, **kwargs)
        (super(LaunchTemplate, self).__init__)(**processed_kwargs)


class TrafficMirrorFilter(troposphere.ec2.TrafficMirrorFilter, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, NetworkServices=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         NetworkServices=NetworkServices, 
         Tags=Tags, **kwargs)
        (super(TrafficMirrorFilter, self).__init__)(**processed_kwargs)


class TrafficMirrorPortRange(troposphere.ec2.TrafficMirrorPortRange, Mixin):

    def __init__(self, title=None, FromPort=REQUIRED, ToPort=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FromPort=FromPort, 
         ToPort=ToPort, **kwargs)
        (super(TrafficMirrorPortRange, self).__init__)(**processed_kwargs)


class TrafficMirrorFilterRule(troposphere.ec2.TrafficMirrorFilterRule, Mixin):

    def __init__(self, title, template=None, validation=True, DestinationCidrBlock=REQUIRED, RuleAction=REQUIRED, RuleNumber=REQUIRED, SourceCidrBlock=REQUIRED, TrafficDirection=REQUIRED, TrafficMirrorFilterId=REQUIRED, Description=NOTHING, DestinationPortRange=NOTHING, Protocol=NOTHING, SourcePortRange=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DestinationCidrBlock=DestinationCidrBlock, 
         RuleAction=RuleAction, 
         RuleNumber=RuleNumber, 
         SourceCidrBlock=SourceCidrBlock, 
         TrafficDirection=TrafficDirection, 
         TrafficMirrorFilterId=TrafficMirrorFilterId, 
         Description=Description, 
         DestinationPortRange=DestinationPortRange, 
         Protocol=Protocol, 
         SourcePortRange=SourcePortRange, **kwargs)
        (super(TrafficMirrorFilterRule, self).__init__)(**processed_kwargs)


class TrafficMirrorSession(troposphere.ec2.TrafficMirrorSession, Mixin):

    def __init__(self, title, template=None, validation=True, NetworkInterfaceId=REQUIRED, SessionNumber=REQUIRED, TrafficMirrorFilterId=REQUIRED, TrafficMirrorTargetId=REQUIRED, Description=NOTHING, PacketLength=NOTHING, Tags=NOTHING, VirtualNetworkId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         NetworkInterfaceId=NetworkInterfaceId, 
         SessionNumber=SessionNumber, 
         TrafficMirrorFilterId=TrafficMirrorFilterId, 
         TrafficMirrorTargetId=TrafficMirrorTargetId, 
         Description=Description, 
         PacketLength=PacketLength, 
         Tags=Tags, 
         VirtualNetworkId=VirtualNetworkId, **kwargs)
        (super(TrafficMirrorSession, self).__init__)(**processed_kwargs)


class TrafficMirrorTarget(troposphere.ec2.TrafficMirrorTarget, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, NetworkInterfaceId=NOTHING, NetworkLoadBalancerArn=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         NetworkInterfaceId=NetworkInterfaceId, 
         NetworkLoadBalancerArn=NetworkLoadBalancerArn, 
         Tags=Tags, **kwargs)
        (super(TrafficMirrorTarget, self).__init__)(**processed_kwargs)


class TransitGateway(troposphere.ec2.TransitGateway, Mixin):

    def __init__(self, title, template=None, validation=True, AmazonSideAsn=NOTHING, AutoAcceptSharedAttachments=NOTHING, DefaultRouteTableAssociation=NOTHING, DefaultRouteTablePropagation=NOTHING, DnsSupport=NOTHING, Tags=NOTHING, VpnEcmpSupport=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AmazonSideAsn=AmazonSideAsn, 
         AutoAcceptSharedAttachments=AutoAcceptSharedAttachments, 
         DefaultRouteTableAssociation=DefaultRouteTableAssociation, 
         DefaultRouteTablePropagation=DefaultRouteTablePropagation, 
         DnsSupport=DnsSupport, 
         Tags=Tags, 
         VpnEcmpSupport=VpnEcmpSupport, **kwargs)
        (super(TransitGateway, self).__init__)(**processed_kwargs)


class TransitGatewayAttachment(troposphere.ec2.TransitGatewayAttachment, Mixin):

    def __init__(self, title, template=None, validation=True, SubnetIds=REQUIRED, TransitGatewayId=REQUIRED, VpcId=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SubnetIds=SubnetIds, 
         TransitGatewayId=TransitGatewayId, 
         VpcId=VpcId, 
         Tags=Tags, **kwargs)
        (super(TransitGatewayAttachment, self).__init__)(**processed_kwargs)


class TransitGatewayRoute(troposphere.ec2.TransitGatewayRoute, Mixin):

    def __init__(self, title, template=None, validation=True, TransitGatewayRouteTableId=REQUIRED, Blackhole=NOTHING, DestinationCidrBlock=NOTHING, TransitGatewayAttachmentId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TransitGatewayRouteTableId=TransitGatewayRouteTableId, 
         Blackhole=Blackhole, 
         DestinationCidrBlock=DestinationCidrBlock, 
         TransitGatewayAttachmentId=TransitGatewayAttachmentId, **kwargs)
        (super(TransitGatewayRoute, self).__init__)(**processed_kwargs)


class TransitGatewayRouteTable(troposphere.ec2.TransitGatewayRouteTable, Mixin):

    def __init__(self, title, template=None, validation=True, TransitGatewayId=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TransitGatewayId=TransitGatewayId, 
         Tags=Tags, **kwargs)
        (super(TransitGatewayRouteTable, self).__init__)(**processed_kwargs)


class TransitGatewayRouteTableAssociation(troposphere.ec2.TransitGatewayRouteTableAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, TransitGatewayAttachmentId=REQUIRED, TransitGatewayRouteTableId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TransitGatewayAttachmentId=TransitGatewayAttachmentId, 
         TransitGatewayRouteTableId=TransitGatewayRouteTableId, **kwargs)
        (super(TransitGatewayRouteTableAssociation, self).__init__)(**processed_kwargs)


class TransitGatewayRouteTablePropagation(troposphere.ec2.TransitGatewayRouteTablePropagation, Mixin):

    def __init__(self, title, template=None, validation=True, TransitGatewayAttachmentId=REQUIRED, TransitGatewayRouteTableId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TransitGatewayAttachmentId=TransitGatewayAttachmentId, 
         TransitGatewayRouteTableId=TransitGatewayRouteTableId, **kwargs)
        (super(TransitGatewayRouteTablePropagation, self).__init__)(**processed_kwargs)


class FleetLaunchTemplateSpecificationRequest(troposphere.ec2.FleetLaunchTemplateSpecificationRequest, Mixin):

    def __init__(self, title=None, LaunchTemplateId=NOTHING, LaunchTemplateName=NOTHING, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LaunchTemplateId=LaunchTemplateId, 
         LaunchTemplateName=LaunchTemplateName, 
         Version=Version, **kwargs)
        (super(FleetLaunchTemplateSpecificationRequest, self).__init__)(**processed_kwargs)


class FleetLaunchTemplateOverridesRequest(troposphere.ec2.FleetLaunchTemplateOverridesRequest, Mixin):

    def __init__(self, title=None, AvailabilityZone=NOTHING, InstanceType=NOTHING, MaxPrice=NOTHING, Priority=NOTHING, SubnetId=NOTHING, WeightedCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AvailabilityZone=AvailabilityZone, 
         InstanceType=InstanceType, 
         MaxPrice=MaxPrice, 
         Priority=Priority, 
         SubnetId=SubnetId, 
         WeightedCapacity=WeightedCapacity, **kwargs)
        (super(FleetLaunchTemplateOverridesRequest, self).__init__)(**processed_kwargs)


class FleetLaunchTemplateConfigRequest(troposphere.ec2.FleetLaunchTemplateConfigRequest, Mixin):

    def __init__(self, title=None, LaunchTemplateSpecification=NOTHING, Overrides=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LaunchTemplateSpecification=LaunchTemplateSpecification, 
         Overrides=Overrides, **kwargs)
        (super(FleetLaunchTemplateConfigRequest, self).__init__)(**processed_kwargs)


class OnDemandOptionsRequest(troposphere.ec2.OnDemandOptionsRequest, Mixin):

    def __init__(self, title=None, AllocationStrategy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllocationStrategy=AllocationStrategy, **kwargs)
        (super(OnDemandOptionsRequest, self).__init__)(**processed_kwargs)


class SpotOptionsRequest(troposphere.ec2.SpotOptionsRequest, Mixin):

    def __init__(self, title=None, AllocationStrategy=NOTHING, InstanceInterruptionBehavior=NOTHING, InstancePoolsToUseCount=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllocationStrategy=AllocationStrategy, 
         InstanceInterruptionBehavior=InstanceInterruptionBehavior, 
         InstancePoolsToUseCount=InstancePoolsToUseCount, **kwargs)
        (super(SpotOptionsRequest, self).__init__)(**processed_kwargs)


class TargetCapacitySpecificationRequest(troposphere.ec2.TargetCapacitySpecificationRequest, Mixin):

    def __init__(self, title=None, DefaultTargetCapacityType=NOTHING, OnDemandTargetCapacity=NOTHING, SpotTargetCapacity=NOTHING, TotalTargetCapacity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultTargetCapacityType=DefaultTargetCapacityType, 
         OnDemandTargetCapacity=OnDemandTargetCapacity, 
         SpotTargetCapacity=SpotTargetCapacity, 
         TotalTargetCapacity=TotalTargetCapacity, **kwargs)
        (super(TargetCapacitySpecificationRequest, self).__init__)(**processed_kwargs)


class EC2Fleet(troposphere.ec2.EC2Fleet, Mixin):

    def __init__(self, title, template=None, validation=True, LaunchTemplateConfigs=REQUIRED, ExcessCapacityTerminationPolicy=NOTHING, OnDemandOptions=NOTHING, ReplaceUnhealthyInstances=NOTHING, SpotOptions=NOTHING, TagSpecifications=NOTHING, TargetCapacitySpecification=NOTHING, TerminateInstancesWithExpiration=NOTHING, Type=NOTHING, ValidFrom=NOTHING, ValidUntil=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         LaunchTemplateConfigs=LaunchTemplateConfigs, 
         ExcessCapacityTerminationPolicy=ExcessCapacityTerminationPolicy, 
         OnDemandOptions=OnDemandOptions, 
         ReplaceUnhealthyInstances=ReplaceUnhealthyInstances, 
         SpotOptions=SpotOptions, 
         TagSpecifications=TagSpecifications, 
         TargetCapacitySpecification=TargetCapacitySpecification, 
         TerminateInstancesWithExpiration=TerminateInstancesWithExpiration, 
         Type=Type, 
         ValidFrom=ValidFrom, 
         ValidUntil=ValidUntil, **kwargs)
        (super(EC2Fleet, self).__init__)(**processed_kwargs)


class CapacityReservation(troposphere.ec2.CapacityReservation, Mixin):

    def __init__(self, title, template=None, validation=True, AvailabilityZone=REQUIRED, InstanceCount=REQUIRED, InstancePlatform=REQUIRED, InstanceType=REQUIRED, EbsOptimized=NOTHING, EndDate=NOTHING, EndDateType=NOTHING, EphemeralStorage=NOTHING, InstanceMatchCriteria=NOTHING, TagSpecifications=NOTHING, Tenancy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AvailabilityZone=AvailabilityZone, 
         InstanceCount=InstanceCount, 
         InstancePlatform=InstancePlatform, 
         InstanceType=InstanceType, 
         EbsOptimized=EbsOptimized, 
         EndDate=EndDate, 
         EndDateType=EndDateType, 
         EphemeralStorage=EphemeralStorage, 
         InstanceMatchCriteria=InstanceMatchCriteria, 
         TagSpecifications=TagSpecifications, 
         Tenancy=Tenancy, **kwargs)
        (super(CapacityReservation, self).__init__)(**processed_kwargs)


class ClientVpnAuthorizationRule(troposphere.ec2.ClientVpnAuthorizationRule, Mixin):

    def __init__(self, title, template=None, validation=True, ClientVpnEndpointId=REQUIRED, TargetNetworkCidr=REQUIRED, AccessGroupId=NOTHING, AuthorizeAllGroups=NOTHING, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClientVpnEndpointId=ClientVpnEndpointId, 
         TargetNetworkCidr=TargetNetworkCidr, 
         AccessGroupId=AccessGroupId, 
         AuthorizeAllGroups=AuthorizeAllGroups, 
         Description=Description, **kwargs)
        (super(ClientVpnAuthorizationRule, self).__init__)(**processed_kwargs)


class CertificateAuthenticationRequest(troposphere.ec2.CertificateAuthenticationRequest, Mixin):

    def __init__(self, title=None, ClientRootCertificateChainArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClientRootCertificateChainArn=ClientRootCertificateChainArn, **kwargs)
        (super(CertificateAuthenticationRequest, self).__init__)(**processed_kwargs)


class DirectoryServiceAuthenticationRequest(troposphere.ec2.DirectoryServiceAuthenticationRequest, Mixin):

    def __init__(self, title=None, DirectoryId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DirectoryId=DirectoryId, **kwargs)
        (super(DirectoryServiceAuthenticationRequest, self).__init__)(**processed_kwargs)


class ClientAuthenticationRequest(troposphere.ec2.ClientAuthenticationRequest, Mixin):

    def __init__(self, title=None, Type=REQUIRED, ActiveDirectory=NOTHING, MutualAuthentication=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         ActiveDirectory=ActiveDirectory, 
         MutualAuthentication=MutualAuthentication, **kwargs)
        (super(ClientAuthenticationRequest, self).__init__)(**processed_kwargs)


class ConnectionLogOptions(troposphere.ec2.ConnectionLogOptions, Mixin):

    def __init__(self, title=None, Enabled=REQUIRED, CloudwatchLogGroup=NOTHING, CloudwatchLogStream=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         CloudwatchLogGroup=CloudwatchLogGroup, 
         CloudwatchLogStream=CloudwatchLogStream, **kwargs)
        (super(ConnectionLogOptions, self).__init__)(**processed_kwargs)


class ClientVpnEndpoint(troposphere.ec2.ClientVpnEndpoint, Mixin):

    def __init__(self, title, template=None, validation=True, AuthenticationOptions=REQUIRED, ClientCidrBlock=REQUIRED, ConnectionLogOptions=REQUIRED, ServerCertificateArn=REQUIRED, Description=NOTHING, DnsServers=NOTHING, SplitTunnel=NOTHING, TagSpecifications=NOTHING, TransportProtocol=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         AuthenticationOptions=AuthenticationOptions, 
         ClientCidrBlock=ClientCidrBlock, 
         ConnectionLogOptions=ConnectionLogOptions, 
         ServerCertificateArn=ServerCertificateArn, 
         Description=Description, 
         DnsServers=DnsServers, 
         SplitTunnel=SplitTunnel, 
         TagSpecifications=TagSpecifications, 
         TransportProtocol=TransportProtocol, **kwargs)
        (super(ClientVpnEndpoint, self).__init__)(**processed_kwargs)


class ClientVpnRoute(troposphere.ec2.ClientVpnRoute, Mixin):

    def __init__(self, title, template=None, validation=True, ClientVpnEndpointId=REQUIRED, DestinationCidrBlock=REQUIRED, TargetVpcSubnetId=REQUIRED, Description=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClientVpnEndpointId=ClientVpnEndpointId, 
         DestinationCidrBlock=DestinationCidrBlock, 
         TargetVpcSubnetId=TargetVpcSubnetId, 
         Description=Description, **kwargs)
        (super(ClientVpnRoute, self).__init__)(**processed_kwargs)


class ClientVpnTargetNetworkAssociation(troposphere.ec2.ClientVpnTargetNetworkAssociation, Mixin):

    def __init__(self, title, template=None, validation=True, ClientVpnEndpointId=REQUIRED, SubnetId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ClientVpnEndpointId=ClientVpnEndpointId, 
         SubnetId=SubnetId, **kwargs)
        (super(ClientVpnTargetNetworkAssociation, self).__init__)(**processed_kwargs)
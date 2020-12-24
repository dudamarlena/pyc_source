# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/services/test_ec2.py
# Compiled at: 2020-02-03 17:04:46
# Size of source mod 2**32: 4407 bytes
from unittest import TestCase
from moto import mock_ec2, mock_elbv2, mock_autoscaling, mock_elb
from casper.services.ec2 import EC2Service
from casper.services.base import get_service, BaseService
from tests.utils import aws_credentials, create_subnet, create_static_instances
import pytest, boto3

@pytest.mark.usefixtures('aws_credentials')
class TestEC2Service(TestCase):

    def test_get_service(self):
        test_service = 'ec2'
        self.assertTrue(issubclass(get_service(test_service), BaseService))
        self.assertTrue(isinstance(get_service(test_service)(), EC2Service))

    @mock_ec2
    @mock_elbv2
    def test_get_cloud_resources_aws_alb(self):
        subnets = create_subnet()
        elb_client = boto3.client('elbv2', region_name='us-east-1')
        count = 200
        for i in range(count):
            _ = elb_client.create_load_balancer(Name=f"testalb{i}", Subnets=subnets)

        ec2 = EC2Service()
        test_group = 'aws_alb'
        resources = ec2.get_cloud_resources(group=test_group)
        self.assertEqual(count, len(resources.keys()))

    @mock_ec2
    @mock_elb
    def test_get_cloud_resources_aws_elb(self):
        listeners = [
         {'Protocol':'http', 
          'LoadBalancerPort':80,  'InstancePort':9000}]
        elb_client = boto3.client('elb', region_name='us-east-1')
        count = 200
        for i in range(count):
            _ = elb_client.create_load_balancer(LoadBalancerName=f"testelb{i}",
              Listeners=listeners)

        ec2 = EC2Service()
        test_group = 'aws_elb'
        resources = ec2.get_cloud_resources(group=test_group)
        self.assertEqual(count, len(resources.keys()))

    @mock_ec2
    def test_get_cloud_resources_aws_security_group(self):
        ec2_client = boto3.client('ec2', region_name='us-east-1')
        count = 1000
        sg = []
        for i in range(count):
            sg.append(ec2_client.create_security_group(Description=f"test sg {i}",
              GroupName=f"testsg{i}"))

        ec2 = EC2Service()
        test_group = 'aws_security_group'
        resources = ec2.get_cloud_resources(group=test_group)
        self.assertEqual(count + 2, len(resources.keys()), 'Created sg plus the two default sgs')
        self.assertIn(sg[0]['GroupId'], set(resources.keys()))

    @mock_ec2
    @mock_autoscaling
    def test_get_cloud_resources_aws_instance(self):
        ec2 = EC2Service()
        subnets = create_subnet()
        count = 200
        instances = create_static_instances(count)
        autoscaling_client = boto3.client('autoscaling', region_name='us-east-1')
        _ = autoscaling_client.create_auto_scaling_group(AutoScalingGroupName='autoscaler1',
          MinSize=300,
          MaxSize=300,
          VPCZoneIdentifier=(subnets[0]),
          InstanceId=(instances[0]['InstanceId']))
        test_group = 'aws_instance'
        resources = ec2.get_cloud_resources(group=test_group)
        self.assertEqual(count, len(resources.keys()))
        self.assertEqual('ami-04b9e92b5572fa0d1', resources[instances[0]['InstanceId']]['ImageId'])

    @mock_ec2
    @mock_autoscaling
    def test_get_cloud_resources_aws_autoscaling_group(self):
        subnets = create_subnet()
        instances = create_static_instances(1)
        autoscaling_client = boto3.client('autoscaling', region_name='us-east-1')
        count = 300
        for i in range(count):
            _ = autoscaling_client.create_auto_scaling_group(AutoScalingGroupName=f"autoscaler{i}",
              MinSize=1,
              MaxSize=1,
              VPCZoneIdentifier=(subnets[0]),
              InstanceId=(instances[0]['InstanceId']))

        ec2 = EC2Service()
        test_group = 'aws_autoscaling_group'
        resources = ec2.get_cloud_resources(group=test_group)
        self.assertEqual(count, len(resources.keys()))
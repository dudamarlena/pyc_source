# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/stdplusAwsHelpers/ec2.py
# Compiled at: 2018-12-11 10:21:21
# Size of source mod 2**32: 872 bytes
import yaml

def describeInstances(ec2Client, InstanceIds):
    response = ec2Client.describe_instances(InstanceIds=InstanceIds)
    instanceDescriptions = response['Reservations']
    instances = {}
    for instance in instanceDescriptions:
        instance = instance['Instances'][0]
        instanceId = instance['InstanceId']
        instances[instanceId] = instance

    return instances


def instanceIdsToPrivateIps(ec2Client, instanceIds):
    if instanceIds:
        instances = describeInstances(ec2Client, instanceIds)
        result = {}
        for instanceId, instance in instances.items():
            result[instanceId] = []
            for networkInterface in instance['NetworkInterfaces']:
                privateIp = networkInterface['PrivateIpAddress']
                result[instanceId].append(privateIp)

        return result
    return {}
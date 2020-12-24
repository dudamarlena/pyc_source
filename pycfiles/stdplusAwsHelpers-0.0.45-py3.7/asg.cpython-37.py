# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/stdplusAwsHelpers/asg.py
# Compiled at: 2018-12-11 10:21:21
# Size of source mod 2**32: 465 bytes


def getInstanceIds(asgClient, asgName):
    asgDescription = asgClient.describe_auto_scaling_groups(AutoScalingGroupNames=[asgName])
    if asgDescription['AutoScalingGroups']:
        if asgDescription['AutoScalingGroups'][0]:
            instances = asgDescription['AutoScalingGroups'][0]['Instances']
            instanceIds = []
            for instance in instances:
                instanceIds.append(instance['InstanceId'])

            return instanceIds
    return []
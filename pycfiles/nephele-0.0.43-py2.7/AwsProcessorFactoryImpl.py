# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/AwsProcessorFactoryImpl.py
# Compiled at: 2017-08-01 10:51:26
import AwsAutoScalingGroup, AwsInstance, AwsLogGroup, AwsRole, AwsStack, AwsEni

class AwsProcessorFactoryImpl:

    def AutoScalingGroup(self, scalingGroup, parent):
        reload(AwsAutoScalingGroup)
        return AwsAutoScalingGroup.AwsAutoScalingGroup(scalingGroup, parent)

    def Eni(self, physicalId, parent):
        reload(AwsEni)
        return AwsEni.AwsEni(physicalId, parent)

    def Instance(self, instanceId, parent):
        reload(AwsInstance)
        return AwsInstance.AwsInstance(instanceId, parent)

    def Stack(self, stack, logicalName, parent):
        reload(AwsStack)
        return AwsStack.AwsStack(stack, logicalName, parent)

    def LogGroup(self, logGroupId, parent):
        reload(AwsLogGroup)
        return AwsLogGroup.AwsLogGroup(logGroupId, parent)

    def Role(self, roleId, parent):
        reload(AwsRole)
        return AwsRole.AwsRole(roleId, parent)
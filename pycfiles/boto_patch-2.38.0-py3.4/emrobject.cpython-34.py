# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/emr/emrobject.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 12903 bytes
"""
This module contains EMR response objects
"""
from boto.resultset import ResultSet

class EmrObject(object):
    Fields = set()

    def __init__(self, connection=None):
        self.connection = connection

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name in self.Fields:
            setattr(self, name.lower(), value)


class RunJobFlowResponse(EmrObject):
    Fields = set(['JobFlowId'])


class AddInstanceGroupsResponse(EmrObject):
    Fields = set(['InstanceGroupIds', 'JobFlowId'])


class ModifyInstanceGroupsResponse(EmrObject):
    Fields = set(['RequestId'])


class Arg(EmrObject):

    def __init__(self, connection=None):
        self.value = None

    def endElement(self, name, value, connection):
        self.value = value


class StepId(Arg):
    pass


class SupportedProduct(Arg):
    pass


class JobFlowStepList(EmrObject):

    def __ini__(self, connection=None):
        self.connection = connection
        self.stepids = None

    def startElement(self, name, attrs, connection):
        if name == 'StepIds':
            self.stepids = ResultSet([('member', StepId)])
            return self.stepids
        else:
            return


class BootstrapAction(EmrObject):
    Fields = set([
     'Args',
     'Name',
     'Path',
     'ScriptPath'])

    def startElement(self, name, attrs, connection):
        if name == 'Args':
            self.args = ResultSet([('member', Arg)])
            return self.args


class KeyValue(EmrObject):
    Fields = set([
     'Key',
     'Value'])


class Step(EmrObject):
    Fields = set([
     'ActionOnFailure',
     'CreationDateTime',
     'EndDateTime',
     'Jar',
     'LastStateChangeReason',
     'MainClass',
     'Name',
     'StartDateTime',
     'State'])

    def __init__(self, connection=None):
        self.connection = connection
        self.args = None

    def startElement(self, name, attrs, connection):
        if name == 'Args':
            self.args = ResultSet([('member', Arg)])
            return self.args
        if name == 'Properties':
            self.properties = ResultSet([('member', KeyValue)])
            return self.properties


class InstanceGroup(EmrObject):
    Fields = set([
     'BidPrice',
     'CreationDateTime',
     'EndDateTime',
     'InstanceGroupId',
     'InstanceRequestCount',
     'InstanceRole',
     'InstanceRunningCount',
     'InstanceType',
     'LastStateChangeReason',
     'LaunchGroup',
     'Market',
     'Name',
     'ReadyDateTime',
     'StartDateTime',
     'State'])


class JobFlow(EmrObject):
    Fields = set([
     'AmiVersion',
     'AvailabilityZone',
     'CreationDateTime',
     'Ec2KeyName',
     'EndDateTime',
     'HadoopVersion',
     'Id',
     'InstanceCount',
     'JobFlowId',
     'KeepJobFlowAliveWhenNoSteps',
     'LastStateChangeReason',
     'LogUri',
     'MasterInstanceId',
     'MasterInstanceType',
     'MasterPublicDnsName',
     'Name',
     'NormalizedInstanceHours',
     'ReadyDateTime',
     'RequestId',
     'SlaveInstanceType',
     'StartDateTime',
     'State',
     'TerminationProtected',
     'Type',
     'Value',
     'VisibleToAllUsers'])

    def __init__(self, connection=None):
        self.connection = connection
        self.steps = None
        self.instancegroups = None
        self.bootstrapactions = None

    def startElement(self, name, attrs, connection):
        if name == 'Steps':
            self.steps = ResultSet([('member', Step)])
            return self.steps
        else:
            if name == 'InstanceGroups':
                self.instancegroups = ResultSet([('member', InstanceGroup)])
                return self.instancegroups
            if name == 'BootstrapActions':
                self.bootstrapactions = ResultSet([('member', BootstrapAction)])
                return self.bootstrapactions
            if name == 'SupportedProducts':
                self.supported_products = ResultSet([('member', SupportedProduct)])
                return self.supported_products
            return


class ClusterTimeline(EmrObject):
    Fields = set([
     'CreationDateTime',
     'ReadyDateTime',
     'EndDateTime'])


class ClusterStateChangeReason(EmrObject):
    Fields = set([
     'Code',
     'Message'])


class ClusterStatus(EmrObject):
    Fields = set([
     'State',
     'StateChangeReason',
     'Timeline'])

    def __init__(self, connection=None):
        self.connection = connection
        self.timeline = None

    def startElement(self, name, attrs, connection):
        if name == 'Timeline':
            self.timeline = ClusterTimeline()
            return self.timeline
        else:
            if name == 'StateChangeReason':
                self.statechangereason = ClusterStateChangeReason()
                return self.statechangereason
            return


class Ec2InstanceAttributes(EmrObject):
    Fields = set([
     'Ec2KeyName',
     'Ec2SubnetId',
     'Ec2AvailabilityZone',
     'IamInstanceProfile'])


class Application(EmrObject):
    Fields = set([
     'Name',
     'Version',
     'Args',
     'AdditionalInfo'])


class Cluster(EmrObject):
    Fields = set([
     'Id',
     'Name',
     'LogUri',
     'RequestedAmiVersion',
     'RunningAmiVersion',
     'AutoTerminate',
     'TerminationProtected',
     'VisibleToAllUsers',
     'MasterPublicDnsName',
     'NormalizedInstanceHours',
     'ServiceRole'])

    def __init__(self, connection=None):
        self.connection = connection
        self.status = None
        self.ec2instanceattributes = None
        self.applications = None
        self.tags = None

    def startElement(self, name, attrs, connection):
        if name == 'Status':
            self.status = ClusterStatus()
            return self.status
        else:
            if name == 'Ec2InstanceAttributes':
                self.ec2instanceattributes = Ec2InstanceAttributes()
                return self.ec2instanceattributes
            if name == 'Applications':
                self.applications = ResultSet([('member', Application)])
                return self.applications
            if name == 'Tags':
                self.tags = ResultSet([('member', KeyValue)])
                return self.tags
            return


class ClusterSummary(EmrObject):
    Fields = set([
     'Id',
     'Name',
     'NormalizedInstanceHours'])

    def __init__(self, connection):
        self.connection = connection
        self.status = None

    def startElement(self, name, attrs, connection):
        if name == 'Status':
            self.status = ClusterStatus()
            return self.status
        else:
            return


class ClusterSummaryList(EmrObject):
    Fields = set([
     'Marker'])

    def __init__(self, connection):
        self.connection = connection
        self.clusters = None

    def startElement(self, name, attrs, connection):
        if name == 'Clusters':
            self.clusters = ResultSet([('member', ClusterSummary)])
            return self.clusters
        else:
            return


class StepConfig(EmrObject):
    Fields = set([
     'Jar',
     'MainClass'])

    def __init__(self, connection=None):
        self.connection = connection
        self.properties = None
        self.args = None

    def startElement(self, name, attrs, connection):
        if name == 'Properties':
            self.properties = ResultSet([('member', KeyValue)])
            return self.properties
        else:
            if name == 'Args':
                self.args = ResultSet([('member', Arg)])
                return self.args
            return


class HadoopStep(EmrObject):
    Fields = set([
     'Id',
     'Name',
     'ActionOnFailure'])

    def __init__(self, connection=None):
        self.connection = connection
        self.config = None
        self.status = None

    def startElement(self, name, attrs, connection):
        if name == 'Config':
            self.config = StepConfig()
            return self.config
        else:
            if name == 'Status':
                self.status = ClusterStatus()
                return self.status
            return


class InstanceGroupInfo(EmrObject):
    Fields = set([
     'Id',
     'Name',
     'Market',
     'InstanceGroupType',
     'BidPrice',
     'InstanceType',
     'RequestedInstanceCount',
     'RunningInstanceCount'])

    def __init__(self, connection=None):
        self.connection = connection
        self.status = None

    def startElement(self, name, attrs, connection):
        if name == 'Status':
            self.status = ClusterStatus()
            return self.status
        else:
            return


class InstanceGroupList(EmrObject):
    Fields = set([
     'Marker'])

    def __init__(self, connection=None):
        self.connection = connection
        self.instancegroups = None

    def startElement(self, name, attrs, connection):
        if name == 'InstanceGroups':
            self.instancegroups = ResultSet([('member', InstanceGroupInfo)])
            return self.instancegroups
        else:
            return


class InstanceInfo(EmrObject):
    Fields = set([
     'Id',
     'Ec2InstanceId',
     'PublicDnsName',
     'PublicIpAddress',
     'PrivateDnsName',
     'PrivateIpAddress'])

    def __init__(self, connection=None):
        self.connection = connection
        self.status = None

    def startElement(self, name, attrs, connection):
        if name == 'Status':
            self.status = ClusterStatus()
            return self.status
        else:
            return


class InstanceList(EmrObject):
    Fields = set([
     'Marker'])

    def __init__(self, connection=None):
        self.connection = connection
        self.instances = None

    def startElement(self, name, attrs, connection):
        if name == 'Instances':
            self.instances = ResultSet([('member', InstanceInfo)])
            return self.instances
        else:
            return


class StepSummary(EmrObject):
    Fields = set([
     'Id',
     'Name'])

    def __init__(self, connection=None):
        self.connection = connection
        self.status = None
        self.config = None

    def startElement(self, name, attrs, connection):
        if name == 'Status':
            self.status = ClusterStatus()
            return self.status
        else:
            if name == 'Config':
                self.config = StepConfig()
                return self.config
            return


class StepSummaryList(EmrObject):
    Fields = set([
     'Marker'])

    def __init__(self, connection=None):
        self.connection = connection
        self.steps = None

    def startElement(self, name, attrs, connection):
        if name == 'Steps':
            self.steps = ResultSet([('member', StepSummary)])
            return self.steps
        else:
            return


class BootstrapActionList(EmrObject):
    Fields = set([
     'Marker'])

    def __init__(self, connection=None):
        self.connection = connection
        self.actions = None

    def startElement(self, name, attrs, connection):
        if name == 'BootstrapActions':
            self.actions = ResultSet([('member', BootstrapAction)])
            return self.actions
        else:
            return
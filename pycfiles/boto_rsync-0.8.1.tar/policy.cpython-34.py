# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/autoscale/policy.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6230 bytes
from boto.resultset import ResultSet
from boto.ec2.elb.listelement import ListElement

class Alarm(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.name = None
        self.alarm_arn = None

    def __repr__(self):
        return 'Alarm:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'AlarmName':
            self.name = value
        else:
            if name == 'AlarmARN':
                self.alarm_arn = value
            else:
                setattr(self, name, value)


class AdjustmentType(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.adjustment_type = None

    def __repr__(self):
        return 'AdjustmentType:%s' % self.adjustment_type

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'AdjustmentType':
            self.adjustment_type = value


class MetricCollectionTypes(object):

    class BaseType(object):
        arg = ''

        def __init__(self, connection):
            self.connection = connection
            self.val = None

        def __repr__(self):
            return '%s:%s' % (self.arg, self.val)

        def startElement(self, name, attrs, connection):
            pass

        def endElement(self, name, value, connection):
            if name == self.arg:
                self.val = value

    class Metric(BaseType):
        arg = 'Metric'

    class Granularity(BaseType):
        arg = 'Granularity'

    def __init__(self, connection=None):
        self.connection = connection
        self.metrics = []
        self.granularities = []

    def __repr__(self):
        return 'MetricCollectionTypes:<%s, %s>' % (self.metrics, self.granularities)

    def startElement(self, name, attrs, connection):
        if name == 'Granularities':
            self.granularities = ResultSet([('member', self.Granularity)])
            return self.granularities
        if name == 'Metrics':
            self.metrics = ResultSet([('member', self.Metric)])
            return self.metrics

    def endElement(self, name, value, connection):
        pass


class ScalingPolicy(object):

    def __init__(self, connection=None, **kwargs):
        """
        Scaling Policy

        :type name: str
        :param name: Name of scaling policy.

        :type adjustment_type: str
        :param adjustment_type: Specifies the type of adjustment. Valid values are `ChangeInCapacity`, `ExactCapacity` and `PercentChangeInCapacity`.

        :type as_name: str or int
        :param as_name: Name or ARN of the Auto Scaling Group.

        :type scaling_adjustment: int
        :param scaling_adjustment: Value of adjustment (type specified in `adjustment_type`).

        :type min_adjustment_step: int
        :param min_adjustment_step: Value of min adjustment step required to
            apply the scaling policy (only make sense when use `PercentChangeInCapacity` as adjustment_type.).

        :type cooldown: int
        :param cooldown: Time (in seconds) before Alarm related Scaling Activities can start after the previous Scaling Activity ends.

        """
        self.name = kwargs.get('name', None)
        self.adjustment_type = kwargs.get('adjustment_type', None)
        self.as_name = kwargs.get('as_name', None)
        self.scaling_adjustment = kwargs.get('scaling_adjustment', None)
        self.cooldown = kwargs.get('cooldown', None)
        self.connection = connection
        self.min_adjustment_step = kwargs.get('min_adjustment_step', None)

    def __repr__(self):
        return 'ScalingPolicy(%s group:%s adjustment:%s)' % (self.name,
         self.as_name,
         self.adjustment_type)

    def startElement(self, name, attrs, connection):
        if name == 'Alarms':
            self.alarms = ResultSet([('member', Alarm)])
            return self.alarms

    def endElement(self, name, value, connection):
        if name == 'PolicyName':
            self.name = value
        else:
            if name == 'AutoScalingGroupName':
                self.as_name = value
            else:
                if name == 'PolicyARN':
                    self.policy_arn = value
                else:
                    if name == 'ScalingAdjustment':
                        self.scaling_adjustment = int(value)
                    else:
                        if name == 'Cooldown':
                            self.cooldown = int(value)
                        else:
                            if name == 'AdjustmentType':
                                self.adjustment_type = value
                            elif name == 'MinAdjustmentStep':
                                self.min_adjustment_step = int(value)

    def delete(self):
        return self.connection.delete_policy(self.name, self.as_name)


class TerminationPolicies(list):

    def __init__(self, connection=None, **kwargs):
        pass

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'member':
            self.append(value)
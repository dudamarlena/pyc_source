# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/elb/instancestate.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2658 bytes


class InstanceState(object):
    __doc__ = '\n    Represents the state of an EC2 Load Balancer Instance\n    '

    def __init__(self, load_balancer=None, description=None, state=None, instance_id=None, reason_code=None):
        """
        :ivar boto.ec2.elb.loadbalancer.LoadBalancer load_balancer: The
            load balancer this instance is registered to.
        :ivar str description: A description of the instance.
        :ivar str instance_id: The EC2 instance ID.
        :ivar str reason_code: Provides information about the cause of
            an OutOfService instance. Specifically, it indicates whether the
            cause is Elastic Load Balancing or the instance behind the
            LoadBalancer.
        :ivar str state: Specifies the current state of the instance.
        """
        self.load_balancer = load_balancer
        self.description = description
        self.state = state
        self.instance_id = instance_id
        self.reason_code = reason_code

    def __repr__(self):
        return 'InstanceState:(%s,%s)' % (self.instance_id, self.state)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Description':
            self.description = value
        else:
            if name == 'State':
                self.state = value
            else:
                if name == 'InstanceId':
                    self.instance_id = value
                else:
                    if name == 'ReasonCode':
                        self.reason_code = value
                    else:
                        setattr(self, name, value)
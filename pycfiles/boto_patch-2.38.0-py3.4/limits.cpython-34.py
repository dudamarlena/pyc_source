# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/autoscale/limits.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1958 bytes


class AccountLimits(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.max_autoscaling_groups = None
        self.max_launch_configurations = None

    def __repr__(self):
        return 'AccountLimits: [%s, %s]' % (self.max_autoscaling_groups,
         self.max_launch_configurations)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'RequestId':
            self.request_id = value
        else:
            if name == 'MaxNumberOfAutoScalingGroups':
                self.max_autoscaling_groups = int(value)
            else:
                if name == 'MaxNumberOfLaunchConfigurations':
                    self.max_launch_configurations = int(value)
                else:
                    setattr(self, name, value)
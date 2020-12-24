# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/autoscale/scheduled.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3060 bytes
from datetime import datetime

class ScheduledUpdateGroupAction(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.name = None
        self.action_arn = None
        self.as_group = None
        self.time = None
        self.start_time = None
        self.end_time = None
        self.recurrence = None
        self.desired_capacity = None
        self.max_size = None
        self.min_size = None

    def __repr__(self):
        return 'ScheduledUpdateGroupAction:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'DesiredCapacity':
            self.desired_capacity = value
        else:
            if name == 'ScheduledActionName':
                self.name = value
            else:
                if name == 'AutoScalingGroupName':
                    self.as_group = value
                else:
                    if name == 'MaxSize':
                        self.max_size = int(value)
                    else:
                        if name == 'MinSize':
                            self.min_size = int(value)
                        else:
                            if name == 'ScheduledActionARN':
                                self.action_arn = value
                            else:
                                if name == 'Recurrence':
                                    self.recurrence = value
                                elif name == 'Time':
                                    try:
                                        self.time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                                    except ValueError:
                                        self.time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

                                elif name == 'StartTime':
                                    try:
                                        self.start_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                                    except ValueError:
                                        self.start_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

                                elif name == 'EndTime':
                                    try:
                                        self.end_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                                    except ValueError:
                                        self.end_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')

                                else:
                                    setattr(self, name, value)
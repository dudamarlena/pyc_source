# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/bundleinstance.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2754 bytes
__doc__ = '\nRepresents an EC2 Bundle Task\n'
from boto.ec2.ec2object import EC2Object

class BundleInstanceTask(EC2Object):

    def __init__(self, connection=None):
        super(BundleInstanceTask, self).__init__(connection)
        self.id = None
        self.instance_id = None
        self.progress = None
        self.start_time = None
        self.state = None
        self.bucket = None
        self.prefix = None
        self.upload_policy = None
        self.upload_policy_signature = None
        self.update_time = None
        self.code = None
        self.message = None

    def __repr__(self):
        return 'BundleInstanceTask:%s' % self.id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'bundleId':
            self.id = value
        else:
            if name == 'instanceId':
                self.instance_id = value
            else:
                if name == 'progress':
                    self.progress = value
                else:
                    if name == 'startTime':
                        self.start_time = value
                    else:
                        if name == 'state':
                            self.state = value
                        else:
                            if name == 'bucket':
                                self.bucket = value
                            else:
                                if name == 'prefix':
                                    self.prefix = value
                                else:
                                    if name == 'uploadPolicy':
                                        self.upload_policy = value
                                    else:
                                        if name == 'uploadPolicySignature':
                                            self.upload_policy_signature = value
                                        else:
                                            if name == 'updateTime':
                                                self.update_time = value
                                            else:
                                                if name == 'code':
                                                    self.code = value
                                                else:
                                                    if name == 'message':
                                                        self.message = value
                                                    else:
                                                        setattr(self, name, value)
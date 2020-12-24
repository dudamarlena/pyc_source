# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/AwsInstance.py
# Compiled at: 2017-08-01 10:58:24
from AwsProcessor import AwsProcessor
from stdplusAwsHelpers.AwsConnectionFactory import AwsConnectionFactory
from pprint import pprint

class AwsInstance(AwsProcessor):

    def __init__(self, instanceId, parent):
        """Construct an AwsRole command processor"""
        AwsProcessor.__init__(self, parent.raw_prompt + '/instance:' + instanceId, parent)
        self.instanceId = instanceId
        self.do_refresh('')

    def do_refresh(self, args):
        """Refresh the view of the log group"""
        client = AwsConnectionFactory.getEc2Client()
        response = client.describe_instances(InstanceIds=[self.instanceId])
        self.instance = response['Reservations'][0]['Instances'][0]

    def do_pprint(self, args):
        pprint(self.instance)

    def do_tags(self, args):
        for entry in self.instance['Tags']:
            print ("'{}': '{}'").format(entry['Key'], entry['Value'])
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/AwsEni.py
# Compiled at: 2017-05-24 08:32:29
from AwsProcessor import AwsProcessor
from stdplusAwsHelpers.AwsConnectionFactory import AwsConnectionFactory
from pprint import pprint

class AwsEni(AwsProcessor):

    def __init__(self, physicalId, parent):
        """Construct an AwsEni command processor"""
        AwsProcessor.__init__(self, parent.raw_prompt + '/eni:' + physicalId, parent)
        self.physicalId = physicalId
        self.do_refresh('')

    def do_refresh(self, args):
        """Refresh the view of the eni"""
        pprint(AwsConnectionFactory.getEc2Client().describe_network_interfaces(NetworkInterfaceIds=[self.physicalId]))
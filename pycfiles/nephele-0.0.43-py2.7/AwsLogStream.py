# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/AwsLogStream.py
# Compiled at: 2017-05-24 08:32:43
from AwsProcessor import AwsProcessor
from stdplusAwsHelpers.AwsConnectionFactory import AwsConnectionFactory
from CommandArgumentParser import CommandArgumentParser
from pprint import pprint

class AwsLogStream(AwsProcessor):

    def __init__(self, logStream, parent):
        """Construct an AwsLogStream command processor"""
        AwsProcessor.__init__(self, parent.raw_prompt + '/logStream:' + logStream['logStreamName'], parent)
        self.stackResource = None
        self.logStream = logStream
        self.do_tail([])
        return

    def do_tail(self, args):
        """Tail the logs"""
        response = AwsConnectionFactory.getLogClient().get_log_events(logGroupName=self.logStream['logGroupName'], logStreamName=self.logStream['logStreamName'], limit=10, startFromHead=False)
        pprint(response)
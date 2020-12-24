# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/contrib/ymlmessage.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1885 bytes
"""
This module was contributed by Chris Moyer.  It provides a subclass of the
SQS Message class that supports YAML as the body of the message.

This module requires the yaml module.
"""
from boto.sqs.message import Message
import yaml

class YAMLMessage(Message):
    __doc__ = '\n    The YAMLMessage class provides a YAML compatible message. Encoding and\n    decoding are handled automaticaly.\n\n    Access this message data like such:\n\n    m.data = [ 1, 2, 3]\n    m.data[0] # Returns 1\n\n    This depends on the PyYAML package\n    '

    def __init__(self, queue=None, body='', xml_attrs=None):
        self.data = None
        super(YAMLMessage, self).__init__(queue, body)

    def set_body(self, body):
        self.data = yaml.safe_load(body)

    def get_body(self):
        return yaml.dump(self.data)
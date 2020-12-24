# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/contrib/ymlmessage.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1885 bytes
__doc__ = '\nThis module was contributed by Chris Moyer.  It provides a subclass of the\nSQS Message class that supports YAML as the body of the message.\n\nThis module requires the yaml module.\n'
from boto.sqs.message import Message
import yaml

class YAMLMessage(Message):
    """YAMLMessage"""

    def __init__(self, queue=None, body='', xml_attrs=None):
        self.data = None
        super(YAMLMessage, self).__init__(queue, body)

    def set_body(self, body):
        self.data = yaml.safe_load(body)

    def get_body(self):
        return yaml.dump(self.data)
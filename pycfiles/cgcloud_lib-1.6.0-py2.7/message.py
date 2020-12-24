# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/lib/message.py
# Compiled at: 2016-11-22 15:21:45
import base64, json

class UnknownVersion(Exception):

    def __init__(self, version):
        super(UnknownVersion, self).__init__('Unknown message version %d' % version)
        self.version = version


class Message(object):
    """
    A message, mostly for passing information about events to agents. The message version is used
    to differentiate between incompatible message formats. For example, adding a field is a
    compatible change if there is a default value for that field, and does not require
    incrementing the version. Message consumers should ignore versions they don't understand.
    """
    TYPE_UPDATE_SSH_KEYS = 1

    @classmethod
    def from_sqs(cls, sqs_message):
        """
        :param sqs_message: the SQS message to initializes this instance from, assuiming that the
        SQS message originates from a SQS queue that is subscribed to an SNS topic :type
        sqs_message: SQSMessage

        :return: the parsed message or None if the message is of an unkwown version
        :rtype: Message
        """
        sns_message = json.loads(sqs_message.get_body())
        return Message.from_sns(sns_message['Message'])

    @classmethod
    def from_sns(cls, message):
        return cls.from_dict(json.loads(base64.standard_b64decode(message)))

    @classmethod
    def from_dict(cls, message):
        version = message['version']
        if version == 1:
            return cls(type=message['type'])
        raise UnknownVersion(version)

    def __init__(self, type):
        super(Message, self).__init__()
        self.type = type

    def to_dict(self):
        return dict(version=1, type=self.type)

    def to_sns(self):
        return base64.standard_b64encode(json.dumps(self.to_dict()))
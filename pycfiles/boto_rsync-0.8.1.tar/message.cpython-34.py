# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sqs/message.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 9892 bytes
__doc__ = '\nSQS Message\n\nA Message represents the data stored in an SQS queue.  The rules for what is allowed within an SQS\nMessage are here:\n\n    http://docs.amazonwebservices.com/AWSSimpleQueueService/2008-01-01/SQSDeveloperGuide/Query_QuerySendMessage.html\n\nSo, at it\'s simplest level a Message just needs to allow a developer to store bytes in it and get the bytes\nback out.  However, to allow messages to have richer semantics, the Message class must support the\nfollowing interfaces:\n\nThe constructor for the Message class must accept a keyword parameter "queue" which is an instance of a\nboto Queue object and represents the queue that the message will be stored in.  The default value for\nthis parameter is None.\n\nThe constructor for the Message class must accept a keyword parameter "body" which represents the\ncontent or body of the message.  The format of this parameter will depend on the behavior of the\nparticular Message subclass.  For example, if the Message subclass provides dictionary-like behavior to the\nuser the body passed to the constructor should be a dict-like object that can be used to populate\nthe initial state of the message.\n\nThe Message class must provide an encode method that accepts a value of the same type as the body\nparameter of the constructor and returns a string of characters that are able to be stored in an\nSQS message body (see rules above).\n\nThe Message class must provide a decode method that accepts a string of characters that can be\nstored (and probably were stored!) in an SQS message and return an object of a type that is consistent\nwith the "body" parameter accepted on the class constructor.\n\nThe Message class must provide a __len__ method that will return the size of the encoded message\nthat would be stored in SQS based on the current state of the Message object.\n\nThe Message class must provide a get_body method that will return the body of the message in the\nsame format accepted in the constructor of the class.\n\nThe Message class must provide a set_body method that accepts a message body in the same format\naccepted by the constructor of the class.  This method should alter to the internal state of the\nMessage object to reflect the state represented in the message body parameter.\n\nThe Message class must provide a get_body_encoded method that returns the current body of the message\nin the format in which it would be stored in SQS.\n'
import base64, boto
from boto.compat import StringIO
from boto.compat import six
from boto.sqs.attributes import Attributes
from boto.sqs.messageattributes import MessageAttributes
from boto.exception import SQSDecodeError

class RawMessage(object):
    """RawMessage"""

    def __init__(self, queue=None, body=''):
        self.queue = queue
        self.set_body(body)
        self.id = None
        self.receipt_handle = None
        self.md5 = None
        self.attributes = Attributes(self)
        self.message_attributes = MessageAttributes(self)
        self.md5_message_attributes = None

    def __len__(self):
        return len(self.encode(self._body))

    def startElement(self, name, attrs, connection):
        if name == 'Attribute':
            return self.attributes
        if name == 'MessageAttribute':
            return self.message_attributes

    def endElement(self, name, value, connection):
        if name == 'Body':
            self.set_body(value)
        else:
            if name == 'MessageId':
                self.id = value
            else:
                if name == 'ReceiptHandle':
                    self.receipt_handle = value
                else:
                    if name == 'MD5OfBody':
                        self.md5 = value
                    else:
                        if name == 'MD5OfMessageAttributes':
                            self.md5_message_attributes = value
                        else:
                            setattr(self, name, value)

    def endNode(self, connection):
        self.set_body(self.decode(self.get_body()))

    def encode(self, value):
        """Transform body object into serialized byte array format."""
        return value

    def decode(self, value):
        """Transform seralized byte array into any object."""
        return value

    def set_body(self, body):
        """Override the current body for this object, using decoded format."""
        self._body = body

    def get_body(self):
        return self._body

    def get_body_encoded(self):
        """
        This method is really a semi-private method used by the Queue.write
        method when writing the contents of the message to SQS.
        You probably shouldn't need to call this method in the normal course of events.
        """
        return self.encode(self.get_body())

    def delete(self):
        if self.queue:
            return self.queue.delete_message(self)

    def change_visibility(self, visibility_timeout):
        if self.queue:
            self.queue.connection.change_message_visibility(self.queue, self.receipt_handle, visibility_timeout)


class Message(RawMessage):
    """Message"""

    def encode(self, value):
        if not isinstance(value, six.binary_type):
            value = value.encode('utf-8')
        return base64.b64encode(value).decode('utf-8')

    def decode(self, value):
        try:
            value = base64.b64decode(value.encode('utf-8')).decode('utf-8')
        except:
            boto.log.warning('Unable to decode message')
            return value

        return value


class MHMessage(Message):
    """MHMessage"""

    def __init__(self, queue=None, body=None, xml_attrs=None):
        if body is None or body == '':
            body = {}
        super(MHMessage, self).__init__(queue, body)

    def decode(self, value):
        try:
            msg = {}
            fp = StringIO(value)
            line = fp.readline()
            while line:
                delim = line.find(':')
                key = line[0:delim]
                value = line[delim + 1:].strip()
                msg[key.strip()] = value.strip()
                line = fp.readline()

        except:
            raise SQSDecodeError('Unable to decode message', self)

        return msg

    def encode(self, value):
        s = ''
        for item in value.items():
            s = s + '%s: %s\n' % (item[0], item[1])

        return s

    def __contains__(self, key):
        return key in self._body

    def __getitem__(self, key):
        if key in self._body:
            return self._body[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        self._body[key] = value
        self.set_body(self._body)

    def keys(self):
        return self._body.keys()

    def values(self):
        return self._body.values()

    def items(self):
        return self._body.items()

    def has_key(self, key):
        return key in self._body

    def update(self, d):
        self._body.update(d)
        self.set_body(self._body)

    def get(self, key, default=None):
        return self._body.get(key, default)


class EncodedMHMessage(MHMessage):
    """EncodedMHMessage"""

    def decode(self, value):
        try:
            value = base64.b64decode(value.encode('utf-8')).decode('utf-8')
        except:
            raise SQSDecodeError('Unable to decode message', self)

        return super(EncodedMHMessage, self).decode(value)

    def encode(self, value):
        value = super(EncodedMHMessage, self).encode(value)
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')
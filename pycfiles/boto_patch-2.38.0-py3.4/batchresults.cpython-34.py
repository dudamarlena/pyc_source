# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sqs/batchresults.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3515 bytes
"""
A set of results returned by SendMessageBatch.
"""

class ResultEntry(dict):
    __doc__ = '\n    The result (successful or unsuccessful) of a single\n    message within a send_message_batch request.\n\n    In the case of a successful result, this dict-like\n    object will contain the following items:\n\n    :ivar id: A string containing the user-supplied ID of the message.\n    :ivar message_id: A string containing the SQS ID of the new message.\n    :ivar message_md5: A string containing the MD5 hash of the message body.\n\n    In the case of an error, this object will contain the following\n    items:\n\n    :ivar id: A string containing the user-supplied ID of the message.\n    :ivar sender_fault: A boolean value.\n    :ivar error_code: A string containing a short description of the error.\n    :ivar error_message: A string containing a description of the error.\n    '

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Id':
            self['id'] = value
        else:
            if name == 'MessageId':
                self['message_id'] = value
            else:
                if name == 'MD5OfMessageBody':
                    self['message_md5'] = value
                else:
                    if name == 'SenderFault':
                        self['sender_fault'] = value
                    else:
                        if name == 'Code':
                            self['error_code'] = value
                        elif name == 'Message':
                            self['error_message'] = value


class BatchResults(object):
    __doc__ = '\n    A container for the results of a send_message_batch request.\n\n    :ivar results: A list of successful results.  Each item in the\n        list will be an instance of :class:`ResultEntry`.\n\n    :ivar errors: A list of unsuccessful results.  Each item in the\n        list will be an instance of :class:`ResultEntry`.\n    '

    def __init__(self, parent):
        self.parent = parent
        self.results = []
        self.errors = []

    def startElement(self, name, attrs, connection):
        if name.endswith('MessageBatchResultEntry'):
            entry = ResultEntry()
            self.results.append(entry)
            return entry
        if name == 'BatchResultErrorEntry':
            entry = ResultEntry()
            self.errors.append(entry)
            return entry

    def endElement(self, name, value, connection):
        setattr(self, name, value)
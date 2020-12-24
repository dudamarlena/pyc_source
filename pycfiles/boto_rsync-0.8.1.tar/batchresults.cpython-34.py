# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sqs/batchresults.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3515 bytes
__doc__ = '\nA set of results returned by SendMessageBatch.\n'

class ResultEntry(dict):
    """ResultEntry"""

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
    """BatchResults"""

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
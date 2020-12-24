# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sqs/messageattributes.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2487 bytes
__doc__ = '\nRepresents an SQS MessageAttribute Name/Value set\n'

class MessageAttributes(dict):

    def __init__(self, parent):
        self.parent = parent
        self.current_key = None
        self.current_value = None

    def startElement(self, name, attrs, connection):
        if name == 'Value':
            self.current_value = MessageAttributeValue(self)
            return self.current_value

    def endElement(self, name, value, connection):
        if name == 'MessageAttribute':
            self[self.current_key] = self.current_value
        else:
            if name == 'Name':
                self.current_key = value
            else:
                if name == 'Value':
                    pass
                else:
                    setattr(self, name, value)


class MessageAttributeValue(dict):

    def __init__(self, parent):
        self.parent = parent

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'DataType':
            self['data_type'] = value
        else:
            if name == 'StringValue':
                self['string_value'] = value
            else:
                if name == 'BinaryValue':
                    self['binary_value'] = value
                else:
                    if name == 'StringListValue':
                        self['string_list_value'] = value
                    elif name == 'BinaryListValue':
                        self['binary_list_value'] = value
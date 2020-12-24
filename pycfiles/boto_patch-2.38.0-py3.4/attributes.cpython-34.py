# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sqs/attributes.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1718 bytes
"""
Represents an SQS Attribute Name/Value set
"""

class Attributes(dict):

    def __init__(self, parent):
        self.parent = parent
        self.current_key = None
        self.current_value = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Attribute':
            self[self.current_key] = self.current_value
        else:
            if name == 'Name':
                self.current_key = value
            else:
                if name == 'Value':
                    self.current_value = value
                else:
                    setattr(self, name, value)
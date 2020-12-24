# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/event.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1876 bytes


class Event(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.message = None
        self.source_identifier = None
        self.source_type = None
        self.engine = None
        self.date = None

    def __repr__(self):
        return '"%s"' % self.message

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'SourceIdentifier':
            self.source_identifier = value
        else:
            if name == 'SourceType':
                self.source_type = value
            else:
                if name == 'Message':
                    self.message = value
                else:
                    if name == 'Date':
                        self.date = value
                    else:
                        setattr(self, name, value)
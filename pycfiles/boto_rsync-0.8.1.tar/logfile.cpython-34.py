# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/logfile.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2533 bytes


class LogFile(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.size = None
        self.log_filename = None
        self.last_written = None

    def __repr__(self):
        return '%s' % self.log_filename

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'LastWritten':
            self.last_written = value
        else:
            if name == 'LogFileName':
                self.log_filename = value
            else:
                if name == 'Size':
                    self.size = value
                else:
                    setattr(self, name, value)


class LogFileObject(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.log_filename = None

    def __repr__(self):
        return 'LogFileObject: %s/%s' % (self.dbinstance_id, self.log_filename)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'LogFileData':
            self.data = value
        else:
            if name == 'AdditionalDataPending':
                self.additional_data_pending = value
            else:
                if name == 'Marker':
                    self.marker = value
                else:
                    setattr(self, name, value)
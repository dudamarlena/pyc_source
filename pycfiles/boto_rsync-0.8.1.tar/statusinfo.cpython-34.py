# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/statusinfo.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2011 bytes


class StatusInfo(object):
    """StatusInfo"""

    def __init__(self, status_type=None, normal=None, status=None, message=None):
        self.status_type = status_type
        self.normal = normal
        self.status = status
        self.message = message

    def __repr__(self):
        return 'StatusInfo:%s' % self.message

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'StatusType':
            self.status_type = value
        else:
            if name == 'Normal':
                if value.lower() == 'true':
                    self.normal = True
                else:
                    self.normal = False
            else:
                if name == 'Status':
                    self.status = value
                else:
                    if name == 'Message':
                        self.message = value
                    else:
                        setattr(self, name, value)
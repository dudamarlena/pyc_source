# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/statusinfo.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2011 bytes


class StatusInfo(object):
    __doc__ = '\n    Describes a status message.\n    '

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
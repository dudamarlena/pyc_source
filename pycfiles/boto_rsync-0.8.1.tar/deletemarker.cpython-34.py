# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/deletemarker.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2087 bytes
from boto.s3.user import User

class DeleteMarker(object):

    def __init__(self, bucket=None, name=None):
        self.bucket = bucket
        self.name = name
        self.version_id = None
        self.is_latest = False
        self.last_modified = None
        self.owner = None

    def startElement(self, name, attrs, connection):
        if name == 'Owner':
            self.owner = User(self)
            return self.owner
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'Key':
            self.name = value
        else:
            if name == 'IsLatest':
                if value == 'true':
                    self.is_latest = True
                else:
                    self.is_latest = False
            else:
                if name == 'LastModified':
                    self.last_modified = value
                else:
                    if name == 'Owner':
                        pass
                    else:
                        if name == 'VersionId':
                            self.version_id = value
                        else:
                            setattr(self, name, value)
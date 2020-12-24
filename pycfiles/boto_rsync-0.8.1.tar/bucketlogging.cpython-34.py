# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/bucketlogging.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3183 bytes
import xml.sax.saxutils
from boto.s3.acl import Grant

class BucketLogging(object):

    def __init__(self, target=None, prefix=None, grants=None):
        self.target = target
        self.prefix = prefix
        if grants is None:
            self.grants = []
        else:
            self.grants = grants

    def __repr__(self):
        if self.target is None:
            return '<BucketLoggingStatus: Disabled>'
        grants = []
        for g in self.grants:
            if g.type == 'CanonicalUser':
                u = g.display_name
            else:
                if g.type == 'Group':
                    u = g.uri
                else:
                    u = g.email_address
            grants.append('%s = %s' % (u, g.permission))

        return '<BucketLoggingStatus: %s/%s (%s)>' % (self.target, self.prefix, ', '.join(grants))

    def add_grant(self, grant):
        self.grants.append(grant)

    def startElement(self, name, attrs, connection):
        if name == 'Grant':
            self.grants.append(Grant())
            return self.grants[(-1)]
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'TargetBucket':
            self.target = value
        else:
            if name == 'TargetPrefix':
                self.prefix = value
            else:
                setattr(self, name, value)

    def to_xml(self):
        s = '<?xml version="1.0" encoding="UTF-8"?>'
        s += '<BucketLoggingStatus xmlns="http://doc.s3.amazonaws.com/2006-03-01">'
        if self.target is not None:
            s += '<LoggingEnabled>'
            s += '<TargetBucket>%s</TargetBucket>' % self.target
            prefix = self.prefix or ''
            s += '<TargetPrefix>%s</TargetPrefix>' % xml.sax.saxutils.escape(prefix)
            if self.grants:
                s += '<TargetGrants>'
                for grant in self.grants:
                    s += grant.to_xml()

                s += '</TargetGrants>'
            s += '</LoggingEnabled>'
        s += '</BucketLoggingStatus>'
        return s
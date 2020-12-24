# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudfront/identity.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4483 bytes
import uuid

class OriginAccessIdentity(object):

    def __init__(self, connection=None, config=None, id='', s3_user_id='', comment=''):
        self.connection = connection
        self.config = config
        self.id = id
        self.s3_user_id = s3_user_id
        self.comment = comment
        self.etag = None

    def startElement(self, name, attrs, connection):
        if name == 'CloudFrontOriginAccessIdentityConfig':
            self.config = OriginAccessIdentityConfig()
            return self.config
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'Id':
            self.id = value
        else:
            if name == 'S3CanonicalUserId':
                self.s3_user_id = value
            else:
                if name == 'Comment':
                    self.comment = value
                else:
                    setattr(self, name, value)

    def update(self, comment=None):
        new_config = OriginAccessIdentityConfig(self.connection, self.config.caller_reference, self.config.comment)
        if comment is not None:
            new_config.comment = comment
        self.etag = self.connection.set_origin_identity_config(self.id, self.etag, new_config)
        self.config = new_config

    def delete(self):
        return self.connection.delete_origin_access_identity(self.id, self.etag)

    def uri(self):
        return 'origin-access-identity/cloudfront/%s' % self.id


class OriginAccessIdentityConfig(object):

    def __init__(self, connection=None, caller_reference='', comment=''):
        self.connection = connection
        if caller_reference:
            self.caller_reference = caller_reference
        else:
            self.caller_reference = str(uuid.uuid4())
        self.comment = comment

    def to_xml(self):
        s = '<?xml version="1.0" encoding="UTF-8"?>\n'
        s += '<CloudFrontOriginAccessIdentityConfig xmlns="http://cloudfront.amazonaws.com/doc/2009-09-09/">\n'
        s += '  <CallerReference>%s</CallerReference>\n' % self.caller_reference
        if self.comment:
            s += '  <Comment>%s</Comment>\n' % self.comment
        s += '</CloudFrontOriginAccessIdentityConfig>\n'
        return s

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Comment':
            self.comment = value
        else:
            if name == 'CallerReference':
                self.caller_reference = value
            else:
                setattr(self, name, value)


class OriginAccessIdentitySummary(object):

    def __init__(self, connection=None, id='', s3_user_id='', comment=''):
        self.connection = connection
        self.id = id
        self.s3_user_id = s3_user_id
        self.comment = comment
        self.etag = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Id':
            self.id = value
        else:
            if name == 'S3CanonicalUserId':
                self.s3_user_id = value
            else:
                if name == 'Comment':
                    self.comment = value
                else:
                    setattr(self, name, value)

    def get_origin_access_identity(self):
        return self.connection.get_origin_access_identity_info(self.id)
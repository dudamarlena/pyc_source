# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudfront/object.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1798 bytes
from boto.s3.key import Key

class Object(Key):

    def __init__(self, bucket, name=None):
        super(Object, self).__init__(bucket, name=name)
        self.distribution = bucket.distribution

    def __repr__(self):
        return '<Object: %s/%s>' % (self.distribution.config.origin, self.name)

    def url(self, scheme='http'):
        url = '%s://' % scheme
        url += self.distribution.domain_name
        if scheme.lower().startswith('rtmp'):
            url += '/cfx/st/'
        else:
            url += '/'
        url += self.name
        return url


class StreamingObject(Object):

    def url(self, scheme='rtmp'):
        return super(StreamingObject, self).url(scheme)
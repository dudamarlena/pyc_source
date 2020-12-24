# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/s3/prefix.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1661 bytes


class Prefix(object):

    def __init__(self, bucket=None, name=None):
        self.bucket = bucket
        self.name = name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Prefix':
            self.name = value
        else:
            setattr(self, name, value)

    @property
    def provider(self):
        provider = None
        if self.bucket:
            if self.bucket.connection:
                provider = self.bucket.connection.provider
        return provider
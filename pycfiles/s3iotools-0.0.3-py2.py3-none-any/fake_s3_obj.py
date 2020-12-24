# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/s3iotools-project/s3iotools/tests/fake_s3_obj.py
# Compiled at: 2019-05-19 22:48:53


class FakeS3Object(object):

    def __init__(self, key=None, last_modified=None, e_tag=None, content_length=None):
        self.key = key
        self.last_modified = last_modified
        self.e_tag = e_tag
        self.content_length = content_length
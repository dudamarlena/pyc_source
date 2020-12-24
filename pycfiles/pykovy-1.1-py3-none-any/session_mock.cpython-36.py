# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pykovi/session_mock.py
# Compiled at: 2019-11-11 14:22:41
# Size of source mod 2**32: 532 bytes
import os, awswrangler as aw

class SessionMock(aw.Session):

    @property
    def pandas(self):
        return super().pandas

    @pandas.setter
    def pandas(self, value: aw.Pandas):
        self._pandas = value

    @property
    def s3(self):
        return super().s3

    @s3.setter
    def s3(self, value: aw.S3):
        self._s3 = value

    @property
    def glue(self):
        return super().glue

    @glue.setter
    def glue(self, value: aw.Glue):
        self._glue = value
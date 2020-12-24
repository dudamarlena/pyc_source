# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
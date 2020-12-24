# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pkgsync/digest.py
# Compiled at: 2013-03-02 17:41:30
import hashlib

class Md5MismatchException(Exception):
    """
    The given md5sum does not match the md5sum of the file at the given path
    """
    pass


class IteratingMd5Checker(object):

    def __init__(self, path, against):
        self.path = path
        self.against = against

    def check(self):
        digest = self._digest()
        if not digest == self.against:
            raise Md5MismatchException(self.path, self.against)

    def _digest(self):
        md5 = hashlib.md5()
        with open(self.path, 'rb') as (f):
            for chunk in iter(lambda : f.read(128 * md5.block_size), ''):
                md5.update(chunk)

        return md5.hexdigest()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/utils.py
# Compiled at: 2012-09-04 10:29:23
import hmac, hashlib

class HashSum(object):
    """
    Make a hash from data and a secret key that will represent the data health
    in the remote side.
    """

    def __init__(self, key):
        self.key = key

    def sign(self, data, key=None):
        """
        Sign the data with key, and return the result checksum
        """
        a = hmac.new(str(self.key or key), data, hashlib.sha1)
        return a.hexdigest()

    def is_valid(self, data, checksum):
        """
        Check the data and checksum.
        """
        a = hmac.new(str(self.key), data, hashlib.sha1).hexdigest()
        return a == checksum


DefaultValidation = HashSum
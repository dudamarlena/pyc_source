# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/profpy/apis/utils/Token.py
# Compiled at: 2020-01-07 15:07:46
# Size of source mod 2**32: 960 bytes
import datetime

class Token(object):
    """Token"""

    def __init__(self, expires_in_seconds, in_token_id, in_token_type):
        """
        Constructor
        :param expires_in_seconds: The number of seconds from now in which the token expires
        :param in_token_id:        The token's unique id
        :param in_token_type:      The token's type
        """
        self.token = in_token_id
        self.expire_time = datetime.datetime.now() + datetime.timedelta(0, expires_in_seconds)
        self.type = in_token_type

    @property
    def is_expired(self):
        """
        :return: Whether or not the token is expired
        """
        return datetime.datetime.now() > self.expire_time

    @property
    def header(self):
        return {'Authorization':'Bearer {0}'.format(self.token), 
         'Content-Type':'application/json; charset=utf-8'}
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynosql/credentials/aws.py
# Compiled at: 2019-02-23 13:02:27
from pynosql.credentials.base_credentials import BaseCredentials, InvalidCredentials

class AWSCredentials(BaseCredentials):
    """ AWS Credentials Provider """

    def __init__(self, access_key_id, secret_access_key):
        """ AWS Credentials Provider

        :param access_key_id: str aws access key id
        :param secret_access_key: str aws secret key
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.check_credentials()

    @property
    def access_key(self):
        """ Access key property

        :return: str access key
        """
        return self.access_key_id

    @property
    def secret_key(self):
        """ Secret key property

        :return: str secret key
        """
        return self.secret_access_key

    def check_credentials(self):
        """ Check if credentials are not None

        :return: None
        """
        if not self.access_key or not self.secret_key:
            raise InvalidCredentials('Credentials must contain a value.')
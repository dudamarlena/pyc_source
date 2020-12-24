# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/credentials/cred_data.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 2001 bytes
import time, base64, hmac, hashlib, collections, urllib.parse as urllib_parse, synapseclient.core.utils

class SynapseCredentials(object):
    __doc__ = '\n    Credentials used to make requests to Synapse.\n    '

    @property
    def api_key(self):
        return base64.b64encode(self._api_key).decode()

    @api_key.setter
    def api_key(self, value):
        self._api_key = base64.b64decode(value)

    def __init__(self, username, api_key_string):
        self.username = username
        self.api_key = api_key_string

    def get_signed_headers(self, url):
        """
        Generates signed HTTP headers for accessing Synapse urls
        :param url:
        :return:
        """
        sig_timestamp = time.strftime(synapseclient.core.utils.ISO_FORMAT, time.gmtime())
        url = urllib_parse.urlparse(url).path
        sig_data = self.username + url + sig_timestamp
        signature = base64.b64encode(hmac.new(self._api_key, sig_data.encode('utf-8'), hashlib.sha1).digest())
        return {'userId':self.username, 
         'signatureTimestamp':sig_timestamp, 
         'signature':signature}

    def __repr__(self):
        return "SynapseCredentials(username='%s', api_key_string='%s')" % (self.username, self.api_key)


UserLoginArgs = collections.namedtuple('UserLoginArgs', [
 'username', 'password', 'api_key', 'skip_cache', 'session_token'])
UserLoginArgs.__new__.__defaults__ = (None, ) * len(UserLoginArgs._fields)
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_kms_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4128 bytes
import base64
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook
from googleapiclient.discovery import build

def _b64encode(s):
    """ Base 64 encodes a bytes object to a string """
    return base64.b64encode(s).decode('ascii')


def _b64decode(s):
    """ Base 64 decodes a string to bytes. """
    return base64.b64decode(s.encode('utf-8'))


class GoogleCloudKMSHook(GoogleCloudBaseHook):
    """GoogleCloudKMSHook"""

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None):
        super(GoogleCloudKMSHook, self).__init__(gcp_conn_id, delegate_to=delegate_to)

    def get_conn(self):
        """
        Returns a KMS service object.

        :rtype: googleapiclient.discovery.Resource
        """
        http_authorized = self._authorize()
        return build('cloudkms',
          'v1', http=http_authorized, cache_discovery=False)

    def encrypt(self, key_name, plaintext, authenticated_data=None):
        """
        Encrypts a plaintext message using Google Cloud KMS.

        :param key_name: The Resource Name for the key (or key version)
                         to be used for encyption. Of the form
                         ``projects/*/locations/*/keyRings/*/cryptoKeys/**``
        :type key_name: str
        :param plaintext: The message to be encrypted.
        :type plaintext: bytes
        :param authenticated_data: Optional additional authenticated data that
                                   must also be provided to decrypt the message.
        :type authenticated_data: bytes
        :return: The base 64 encoded ciphertext of the original message.
        :rtype: str
        """
        keys = self.get_conn().projects().locations().keyRings().cryptoKeys()
        body = {'plaintext': _b64encode(plaintext)}
        if authenticated_data:
            body['additionalAuthenticatedData'] = _b64encode(authenticated_data)
        request = keys.encrypt(name=key_name, body=body)
        response = request.execute(num_retries=(self.num_retries))
        ciphertext = response['ciphertext']
        return ciphertext

    def decrypt(self, key_name, ciphertext, authenticated_data=None):
        """
        Decrypts a ciphertext message using Google Cloud KMS.

        :param key_name: The Resource Name for the key to be used for decyption.
                         Of the form ``projects/*/locations/*/keyRings/*/cryptoKeys/**``
        :type key_name: str
        :param ciphertext: The message to be decrypted.
        :type ciphertext: str
        :param authenticated_data: Any additional authenticated data that was
                                   provided when encrypting the message.
        :type authenticated_data: bytes
        :return: The original message.
        :rtype: bytes
        """
        keys = self.get_conn().projects().locations().keyRings().cryptoKeys()
        body = {'ciphertext': ciphertext}
        if authenticated_data:
            body['additionalAuthenticatedData'] = _b64encode(authenticated_data)
        request = keys.decrypt(name=key_name, body=body)
        response = request.execute(num_retries=(self.num_retries))
        plaintext = _b64decode(response['plaintext'])
        return plaintext
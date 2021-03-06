# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pysecret-project/pysecret/aws.py
# Compiled at: 2019-04-10 22:37:47
# Size of source mod 2**32: 2091 bytes
import json, boto3, base64

class AWSSecret(object):

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, region_name=None, botocore_session=None, profile_name=None):
        ses = boto3.Session(aws_access_key_id=aws_access_key_id,
          aws_secret_access_key=aws_secret_access_key,
          aws_session_token=aws_session_token,
          region_name=region_name,
          botocore_session=botocore_session,
          profile_name=profile_name)
        self.kms_client = boto3.client('kms')
        self.sm_client = ses.client('secretsmanager')

    def kms_encrypt(self, kms_key_id, text):
        return base64.b64encode(self.kms_client.encrypt(KeyId=kms_key_id,
          Plaintext=(base64.b64encode(text.encode('utf-8'))))['CiphertextBlob']).decode('utf-8')

    def kms_decrypt(self, text):
        return base64.b64decode(self.kms_client.decrypt(CiphertextBlob=(base64.b64decode(text.encode('utf-8'))))['Plaintext']).decode('utf-8')

    def get_secret_value(self, secret_id, key):
        response = self.sm_client.get_secret_value(SecretId=secret_id)
        if 'SecretString' in response:
            secret = response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(response['SecretBinary'])
            secret = decoded_binary_secret
        return json.loads(secret)[key]


if __name__ == '__main__':
    aws_profile = 'sanhe'
    kms_key_id = 'a1679e4b-f415-4aa6-9637-5bee18f9eb64'
    aws = AWSSecret(profile_name=aws_profile)
    secret = 'Hello World'
    encrypted_text = aws.kms_encrypt(kms_key_id, secret)
    decrypted_text = aws.kms_decrypt(encrypted_text)
    assert secret != encrypted_text
    assert secret == decrypted_text
    secret_name = 'dev/learn-secret-manager'
    if not aws.get_secret_value(secret_name, 'a') == '1':
        raise AssertionError
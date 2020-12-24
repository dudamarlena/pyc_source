# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rachelle2/webprojects/toucan-connectors/toucan_connectors/google_credentials.py
# Compiled at: 2020-03-19 08:41:10
# Size of source mod 2**32: 2457 bytes
from pydantic import BaseModel, Field, HttpUrl, validator
CREDENTIALS_INFO_MESSAGE = 'This information is provided in your <a href="https://gspread.readthedocs.io/en/latest/oauth2.html">authentication file</a> downloadable from your <a href="https://console.developers.google.com/apis/credentials">Google Console</a>'

class GoogleCredentials(BaseModel):
    type = Field('service_account',
      title='Service account', description=CREDENTIALS_INFO_MESSAGE)
    type: str
    project_id = Field(..., title='Project ID', description=CREDENTIALS_INFO_MESSAGE)
    project_id: str
    private_key_id = Field(..., title='Private Key ID', description=CREDENTIALS_INFO_MESSAGE)
    private_key_id: str
    private_key = Field(...,
      title='Private Key',
      description=f'A private key in the form "-----BEGIN PRIVATE KEY-----\\nXXX...XXX\\n-----END PRIVATE KEY-----\\n". {CREDENTIALS_INFO_MESSAGE}')
    private_key: str
    client_email = Field(..., title='Client email', description=CREDENTIALS_INFO_MESSAGE)
    client_email: str
    client_id = Field(..., title='Client ID', description=CREDENTIALS_INFO_MESSAGE)
    client_id: str
    auth_uri = Field('https://accounts.google.com/o/oauth2/auth',
      title='Authentication URI',
      description=CREDENTIALS_INFO_MESSAGE)
    auth_uri: HttpUrl
    token_uri = Field('https://oauth2.googleapis.com/token',
      title='Token URI',
      description=f"{CREDENTIALS_INFO_MESSAGE}. You should not need to change the default value.")
    token_uri: HttpUrl
    auth_provider_x509_cert_url = Field('https://www.googleapis.com/oauth2/v1/certs',
      title='Authentication provider X509 certificate URL',
      description=f"{CREDENTIALS_INFO_MESSAGE}. You should not need to change the default value.")
    auth_provider_x509_cert_url: HttpUrl
    client_x509_cert_url = Field(...,
      title='Client X509 certification URL', description=CREDENTIALS_INFO_MESSAGE)
    client_x509_cert_url: HttpUrl

    @validator('private_key')
    def unescape_break_lines(cls, v):
        """
        `private_key` is a long string like
        '-----BEGIN PRIVATE KEY-----
xxx...zzz
-----END PRIVATE KEY-----

        As the breaking line are often escaped by the client,
        we need to be sure it's unescaped
        """
        return v.replace('\\n', '\n')


def get_google_oauth2_credentials(google_credentials):
    from google.oauth2.service_account import Credentials
    return Credentials.from_service_account_info(google_credentials.dict())
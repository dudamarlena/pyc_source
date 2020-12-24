# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/zeg/azure_blobs.py
# Compiled at: 2020-03-19 11:59:34
# Size of source mod 2**32: 1088 bytes
"""Generate sas tokens to download images from azure."""
from datetime import datetime, timedelta
import os
from azure.storage.blob import generate_container_sas, ContainerSasPermissions

def generate_signed_url(azure_container):
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    return generate_sas_with_sdk(connection_string, azure_container)


def build_creds(connection_string):
    return (
     connection_string.split('AccountName=')[1].split(';')[0],
     connection_string.split('AccountKey=')[1].split(';')[0])


def generate_sas_with_sdk(connection_string, azure_container):
    account_name, account_key = build_creds(connection_string)
    sas_token = generate_container_sas(account_name,
      azure_container,
      account_key=account_key,
      permission=ContainerSasPermissions(read=True),
      expiry=(datetime.utcnow() + timedelta(days=1)))
    return 'https://{}.blob.core.windows.net/{}/{{}}?{}'.format(account_name, azure_container, sas_token)
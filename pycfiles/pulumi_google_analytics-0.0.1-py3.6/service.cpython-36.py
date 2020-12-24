# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_analytics/service.py
# Compiled at: 2020-03-24 13:25:39
# Size of source mod 2**32: 871 bytes
from oauth2client.service_account import ServiceAccountCredentials
import pulumi
from googleapiclient.discovery import build

def get_key_file_location():
    """Returns google key file location"""
    config = pulumi.Config()
    return config.require('google_api_key_file')


def get_service(api_name, api_version, scopes, key_location):
    """Create a google service

    :api_name: the Tag Manager service object.
    :api_version: the path of the Tag Manager account from which to retrieve the container
    :scopes: name of the container
    :key_file_location: location of key file

    Returns:
      The google api service
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_location,
      scopes=scopes)
    service = build(api_name, api_version, credentials=credentials)
    return service
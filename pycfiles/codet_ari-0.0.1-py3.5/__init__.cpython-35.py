# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ari/__init__.py
# Compiled at: 2016-11-21 07:31:45
# Size of source mod 2**32: 641 bytes
"""ARI client library
"""
import ari.client, swaggerpy.http_client, urllib.parse
Client = client.Client

def connect(base_url, username, password):
    """Helper method for easily connecting to ARI.

    :param base_url: Base URL for Asterisk HTTP server (http://localhost:8088/)
    :param username: ARI username
    :param password: ARI password.
    :return:
    """
    split = urllib.parse.urlsplit(base_url)
    http_client = swaggerpy.http_client.SynchronousHttpClient()
    http_client.set_basic_auth(split.hostname, username, password)
    return Client(base_url, http_client)
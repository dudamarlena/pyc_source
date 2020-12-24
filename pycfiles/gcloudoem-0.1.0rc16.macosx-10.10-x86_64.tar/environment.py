# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/datastore/environment.py
# Compiled at: 2016-10-03 22:37:16
"""
Module to provide implicit behavior based on environment.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os, socket
from six.moves.http_client import HTTPConnection
try:
    from google.appengine.api import app_identity
except ImportError:
    app_identity = None

_DATASET_ENV_VAR_NAME = b'GOOGLE_CLOUD_PROJECT'
_GCD_DATASET_ENV_VAR_NAME = b'DATASTORE_DATASET'

def compute_engine_id():
    """
    Gets the Compute Engine project ID if it can be inferred.

    Uses 169.254.169.254 for the metadata server to avoid request latency from DNS lookup.

    See https://cloud.google.com/compute/docs/metadata#metadataserver for information about this IP address. (This IP is
    also used for Amazon EC2 instances, so the metadata flavor is crucial.)

    See https://github.com/google/oauth2client/issues/93 for context about DNS latency.

    :rtype: string or ``NoneType``
    :returns: Compute Engine project ID if the metadata service is available, else ``None``.
    """
    host = b'169.254.169.254'
    uri_path = b'/computeMetadata/v1/project/project-id'
    headers = {b'Metadata-Flavor': b'Google'}
    connection = HTTPConnection(host, timeout=0.1)
    try:
        try:
            connection.request(b'GET', uri_path, headers=headers)
            response = connection.getresponse()
            if response.status == 200:
                return response.read()
        except socket.error:
            pass

    finally:
        connection.close()

    return


def determine_default_dataset_id(dataset_id=None):
    """Determine default dataset ID explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * GCLOUD_DATASET_ID environment variable
    * DATASTORE_DATASET environment variable (for ``gcd`` testing)
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type dataset_id: string
    :param dataset_id: Optional. The dataset ID to use as default.

    :rtype: string or ``NoneType``
    :returns: Default dataset ID if it can be determined.
    """
    if dataset_id is None:
        dataset_id = os.getenv(_DATASET_ENV_VAR_NAME)
    if dataset_id is None:
        dataset_id = os.getenv(_GCD_DATASET_ENV_VAR_NAME)
    if dataset_id is None:
        dataset_id = compute_engine_id()
    return dataset_id
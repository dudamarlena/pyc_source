# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/exceptions.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 5034 bytes
"""
**********
Exceptions
**********

.. autoclass:: synapseclient.exceptions.SynapseError
.. autoclass:: synapseclient.exceptions.SynapseAuthenticationError
.. autoclass:: synapseclient.exceptions.SynapseFileCacheError
.. autoclass:: synapseclient.exceptions.SynapseMalformedEntityError
.. autoclass:: synapseclient.exceptions.SynapseProvenanceError
.. autoclass:: synapseclient.exceptions.SynapseHTTPError

"""
import requests
from synapseclient.core import utils

class SynapseError(Exception):
    __doc__ = 'Generic exception thrown by the client.'


class SynapseMd5MismatchError(SynapseError, IOError):
    __doc__ = 'Error raised when MD5 computed for a download file fails to match the MD5 of its file handle.'


class SynapseFileNotFoundError(SynapseError):
    __doc__ = 'Error thrown when a local file is not found in Synapse.'


class SynapseTimeoutError(SynapseError):
    __doc__ = 'Timed out waiting for response from Synapse.'


class SynapseAuthenticationError(SynapseError):
    __doc__ = 'Unauthorized access.'


class SynapseNoCredentialsError(SynapseAuthenticationError):
    __doc__ = 'No credentials for authentication'


class SynapseFileCacheError(SynapseError):
    __doc__ = 'Error related to local file storage.'


class SynapseMalformedEntityError(SynapseError):
    __doc__ = 'Unexpected structure of Entities.'


class SynapseUnmetAccessRestrictions(SynapseError):
    __doc__ = 'Request cannot be completed due to unmet access restrictions.'


class SynapseProvenanceError(SynapseError):
    __doc__ = 'Incorrect usage of provenance objects.'


class SynapseHTTPError(SynapseError, requests.exceptions.HTTPError):
    __doc__ = 'Wraps recognized HTTP errors.  See\n    `HTTPError <http://docs.python-requests.org/en/latest/api/?highlight=exceptions#requests.exceptions.HTTPError>`_'


def _raise_for_status(response, verbose=False):
    """
    Replacement for requests.response.raise_for_status(). 
    Catches and wraps any Synapse-specific HTTP errors with appropriate text.
    """
    message = None
    if 400 <= response.status_code < 500:
        message = '%s Client Error: %s' % (response.status_code, response.reason)
    else:
        if 500 <= response.status_code < 600:
            message = '%s Server Error: %s' % (response.status_code, response.reason)
    if message is not None:
        if utils.is_json(response.headers.get('content-type', None)):
            if 'reason' in response.json():
                message += '\n%s' % response.json()['reason']
        else:
            message += '\n%s' % response.text
        if verbose:
            try:
                message += '\n\n>>>>>> Request <<<<<<\n%s %s' % (response.request.url, response.request.method)
                message += '\n>>> Headers: %s' % response.request.headers
                message += '\n>>> Body: %s' % response.request.body
            except:
                message += '\nCould not append all request info'

            try:
                message += '\n\n>>>>>> Response <<<<<<\n%s' % str(response)
                message += '\n>>> Headers: %s' % response.headers
                message += '\n>>> Body: %s\n\n' % response.text
            except:
                message += '\nCould not append all response info'

        raise SynapseHTTPError(message, response=response)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/server_info.py
# Compiled at: 2020-02-11 04:03:57
"""Server information and capability registration for the API."""
from __future__ import unicode_literals
import logging
from django.conf import settings
from reviewboard import get_version_string, get_package_version, is_release
from reviewboard.admin.server import get_server_url
_registered_capabilities = {}
_capabilities_defaults = {b'diffs': {b'base_commit_ids': True, 
              b'moved_files': True, 
              b'validation': {b'base_commit_ids': True}}, 
   b'extra_data': {b'json_patching': True}, 
   b'review_requests': {b'commit_ids': True, 
                        b'trivial_publish': True}, 
   b'scmtools': {b'git': {b'empty_files': True, 
                          b'symlinks': True}, 
                 b'mercurial': {b'empty_files': True}, 
                 b'perforce': {b'moved_files': True, 
                               b'empty_files': True}, 
                 b'svn': {b'empty_files': True}}, 
   b'text': {b'markdown': True, 
             b'per_field_text_types': True, 
             b'can_include_raw_values': True}}

def get_server_info(request=None):
    """Return server information for use in the API.

    This is used for the root resource and for the deprecated server
    info resource.

    Args:
        request (django.http.HttpRequest, optional):
            The HTTP request from the client.

    Returns:
        dict:
        A dictionary of information about the server and its capabilities.
    """
    return {b'product': {b'name': b'Review Board', 
                    b'version': get_version_string(), 
                    b'package_version': get_package_version(), 
                    b'is_release': is_release()}, 
       b'site': {b'url': get_server_url(request=request), 
                 b'administrators': [ {b'name': name, b'email': email} for name, email in settings.ADMINS
                                  ], 
                 b'time_zone': settings.TIME_ZONE}, 
       b'capabilities': get_capabilities()}


def get_capabilities():
    """Return the capabilities made available in the API.

    Returns:
        dict:
        The dictionary of capabilities.
    """
    capabilities = _capabilities_defaults.copy()
    capabilities.update(_registered_capabilities)
    return capabilities


def register_webapi_capabilities(capabilities_id, caps):
    """Register a set of web API capabilities.

    These capabilities will appear in the dictionary of available
    capabilities with the ID as their key.

    A capabilties_id attribute passed in, and can only be registerd once.
    A KeyError will be thrown if attempting to register a second time.

    Args:
        capabilities_id (unicode):
            A unique ID representing this collection of capabilities.
            This can only be used once until unregistered.

        caps (dict):
            The dictionary of capabilities to register. Each key msut
            be a string, and each value should be a boolean or a
            dictionary of string keys to booleans.

    Raises:
        KeyError:
            The capabilities ID has already been used.
    """
    if not capabilities_id:
        raise ValueError(b'The capabilities_id attribute must not be None')
    if capabilities_id in _registered_capabilities:
        raise KeyError(b'"%s" is already a registered set of capabilities' % capabilities_id)
    if capabilities_id in _capabilities_defaults:
        raise KeyError(b'"%s" is reserved for the default set of capabilities' % capabilities_id)
    _registered_capabilities[capabilities_id] = caps


def unregister_webapi_capabilities(capabilities_id):
    """Unregister a previously registered set of web API capabilities.

    Args:
        capabilities_id (unicode):
            The unique ID representing a registered collection of capabilities.

    Raises:
        KeyError:
            A set of capabilities matching the ID were not found.
    """
    try:
        del _registered_capabilities[capabilities_id]
    except KeyError:
        logging.error(b'Failed to unregister unknown web API capabilities "%s".', capabilities_id)
        raise KeyError(b'"%s" is not a registered web API capabilities set' % capabilities_id)
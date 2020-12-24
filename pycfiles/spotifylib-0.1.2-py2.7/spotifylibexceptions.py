# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/spotifylib/spotifylibexceptions.py
# Compiled at: 2017-10-13 08:20:21
"""
Main module Exceptions file

Put your exception classes here
"""
__author__ = 'Oriol Fabregas <fabregas.oriol@gmail.com>'
__docformat__ = 'plaintext'
__date__ = '18-09-2017'

class SpotifyError(Exception):
    """
    Generic error handler while interacting with Spotify API

    These errors appear when trying to get access grants and we get a ``400`` Error

    Examples:
    ---------
        - Wrong client_id
        ``'INVALID_CLIENT: Invalid client'``

        - Wrong response_type
        ``'response_type must be code or token'``

        - Invalid scope
        ``'INVALID_SCOPE: Invalid scope'``

        - Invalid CSRF cookie
        ``'{"error":"errorCSRF"}'``

        - Invalid redirect_uri
        ``'Illegal redirect_uri'``
    """
    pass
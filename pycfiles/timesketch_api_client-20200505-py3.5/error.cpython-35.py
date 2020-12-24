# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/error.py
# Compiled at: 2019-11-22 09:03:26
# Size of source mod 2**32: 1141 bytes
"""Timesketch API client library."""
from __future__ import unicode_literals
import bs4

def error_message(response, message=None, error=RuntimeError):
    """Raise an error using error message extracted from response."""
    if not message:
        message = 'Unknown error, with error: '
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    text = ''
    if soup.p:
        text = soup.p.string
    raise error('{0:s}, with error [{1:d}] {2!s} {3:s}'.format(message, response.status_code, response.reason, text))
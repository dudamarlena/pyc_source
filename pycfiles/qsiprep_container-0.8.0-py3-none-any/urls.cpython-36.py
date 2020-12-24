# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_internal/utils/urls.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 1481 bytes
import os, sys
from pip._vendor.six.moves.urllib import parse as urllib_parse
from pip._vendor.six.moves.urllib import request as urllib_request
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional, Text, Union

def get_url_scheme(url):
    if ':' not in url:
        return
    else:
        return url.split(':', 1)[0].lower()


def path_to_url(path):
    """
    Convert a path to a file: URL.  The path will be made absolute and have
    quoted path parts.
    """
    path = os.path.normpath(os.path.abspath(path))
    url = urllib_parse.urljoin('file:', urllib_request.pathname2url(path))
    return url


def url_to_path(url):
    """
    Convert a file: URL to a path.
    """
    if not url.startswith('file:'):
        raise AssertionError('You can only turn file: urls into filenames (not %r)' % url)
    else:
        _, netloc, path, _, _ = urllib_parse.urlsplit(url)
        if not netloc or netloc == 'localhost':
            netloc = ''
        else:
            if sys.platform == 'win32':
                netloc = '\\\\' + netloc
            else:
                raise ValueError('non-local file URIs are not supported on this platform: %r' % url)
    path = urllib_request.url2pathname(netloc + path)
    return path
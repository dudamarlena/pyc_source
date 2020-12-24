# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/xmlschema_acue/components/xmlschema_acue/tests/xmlschema_acue_tests/testtools/helpers/url.py
# Compiled at: 2019-05-15 06:00:08
try:
    from pathlib import PureWindowsPath, PurePath
except ImportError:
    from pathlib2 import PureWindowsPath, PurePath

from xmlschema_acue.compat import urlsplit, uses_relative

def is_windows_path(path):
    """Checks if the path argument is a Windows platform path."""
    return '\\' in path or ':' in path or '|' in path


def add_leading_slash(path):
    if path and path[0] not in ('/', '\\'):
        return '/' + path
    return path


class URLMismatchError(Exception):
    pass


class URLSchemeMismatchError(URLMismatchError):
    pass


class URLNetLocationMismatchError(URLMismatchError):
    pass


class URLQueryMismatchError(URLMismatchError):
    pass


class URLFragmentMismatchError(URLMismatchError):
    pass


class URLPathMismatchError(URLMismatchError):
    pass


def check_url(url, expected):
    url_parts = urlsplit(url)
    if urlsplit(expected).scheme not in uses_relative:
        expected = add_leading_slash(expected)
    expected_parts = urlsplit(expected, scheme='file')
    if url_parts.scheme != expected_parts.scheme:
        raise URLSchemeMismatchError('Schemes differ.')
    if url_parts.netloc != expected_parts.netloc:
        raise URLNetLocationMismatchError('Netloc parts differ.')
    if url_parts.query != expected_parts.query:
        raise URLQueryMismatchError('Query parts differ.')
    if url_parts.fragment != expected_parts.fragment:
        raise URLFragmentMismatchError('Fragment parts differ.')
    if is_windows_path(url_parts.path) or is_windows_path(expected_parts.path):
        path = PureWindowsPath(url_parts.path)
        expected_path = PureWindowsPath(add_leading_slash(expected_parts.path))
    else:
        path = PurePath(url_parts.path)
        expected_path = PurePath(expected_parts.path)
    if path != expected_path:
        raise URLPathMismatchError('Paths differ.')
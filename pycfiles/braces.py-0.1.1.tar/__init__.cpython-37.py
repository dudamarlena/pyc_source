# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\braces\__init__.py
# Compiled at: 2020-03-31 08:41:02
# Size of source mod 2**32: 1646 bytes
__doc__ = 'Library that implements braces for Python Programming Language.'
__title__ = 'braces'
__author__ = 'NeKitDS'
__copyright__ = 'Copyright 2020 NeKitDS'
__license__ = 'MIT'
__version__ = '0.1.0'
from collections import namedtuple
import re, token
from .const import EXCEPT, TOKEN
from .register_codec import decode
from .token_transform import SmallToken, test_compile, transform
VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
_normal_re = '^\\s*(?:(?P<major>\\d+)(?P<split>[\\.-])?(?P<minor>\\d+)?(?P=split)?(?P<micro>\\d+)?(?P<releaselevel>a|b|rc|f|dev)?(?P<serial>\\d+)?)\\s*$'
_compiled_re = re.compile(_normal_re, re.MULTILINE)

def make_version_details(ver: str) -> VersionInfo:
    match = _compiled_re.match(ver)
    if match is None:
        return VersionInfo(0, 0, 0, 'final', 0)
    args = {}
    for key, value in match.groupdict().items():
        if key == 'split':
            continue
        elif key == 'releaselevel':
            if value is None:
                value = 'f'
            value = {'a':'alpha', 
             'b':'beta', 
             'rc':'candidate', 
             'f':'final', 
             'dev':'developer'}.get(value, 'final')
        elif not value is None:
            if not value.isdigit():
                value = 0
        else:
            value = int(value)
        args[key] = value

    return VersionInfo(**args)


version_info = make_version_details(__version__)
del namedtuple
del re
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/truverifi/_compat.py
# Compiled at: 2019-04-30 01:18:17
# Size of source mod 2**32: 694 bytes
import sys
PYTHON_VERSION = sys.version_info

def _is_python_version(*args, **kwargs):
    major = kwargs.get('major', None)
    minor = kwargs.get('minor', None)
    patch = kwargs.get('patch', None)
    result = True
    if major:
        result = result and major == PYTHON_VERSION.major
    if minor:
        result = result and minor == PYTHON_VERSION.minor
    if patch:
        result = result and patch == PYTHON_VERSION.micro
    return result


PY2 = _is_python_version(major=2)
if PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin
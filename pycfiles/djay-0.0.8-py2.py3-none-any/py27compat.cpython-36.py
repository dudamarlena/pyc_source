# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/setuptools/setuptools/py27compat.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 536 bytes
"""
Compatibility Support for Python 2.7 and earlier
"""
import platform
from setuptools.extern import six

def get_all_headers(message, key):
    """
    Given an HTTPMessage, return all headers matching a given key.
    """
    return message.get_all(key)


if six.PY2:

    def get_all_headers(message, key):
        return message.getheaders(key)


linux_py2_ascii = platform.system() == 'Linux' and six.PY2
rmtree_safe = str if linux_py2_ascii else (lambda x: x)
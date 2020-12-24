# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\__init__.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 410 bytes
"""
Module `chatette_qiu`
A generator of example sentences based on templates.
"""
import pkg_resources
try:
    __version__ = pkg_resources.require('chatette_qiu')[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "<couldn't retrieve version number>"
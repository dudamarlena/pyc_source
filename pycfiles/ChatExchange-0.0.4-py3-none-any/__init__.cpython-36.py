# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\__init__.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 410 bytes
__doc__ = '\nModule `chatette_qiu`\nA generator of example sentences based on templates.\n'
import pkg_resources
try:
    __version__ = pkg_resources.require('chatette_qiu')[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "<couldn't retrieve version number>"
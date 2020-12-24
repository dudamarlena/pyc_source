# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/_config.py
# Compiled at: 2020-03-03 08:28:12
# Size of source mod 2**32: 1904 bytes
"""This module contains library wide configuration.
"""
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '16/12/2019'
import silx.resources

class Config(object):
    __doc__ = '\n    Class containing shared global configuration for the darfix project.\n\n    .. versionadded:: 0.3\n    '
    DEFAULT_COLORMAP_NAME = 'jet'

    def __init__(self):
        silx.resources.register_resource_directory('darfix', 'darfix.resources')
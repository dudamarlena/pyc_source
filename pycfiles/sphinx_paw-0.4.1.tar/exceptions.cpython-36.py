# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarin/dev/sphinx-mediatel/src/sphinx_paw/exceptions.py
# Compiled at: 2019-11-19 10:51:04
# Size of source mod 2**32: 382 bytes
"""Internal exception classes"""

class ExtensionException(Exception):
    __doc__ = 'Base class for all exctension exceptions'


class RequireConfigSection(Exception):
    __doc__ = 'Configuration section missed'


class RequireConfigOption(Exception):
    __doc__ = 'Configuration option missed'


class RequireExtensionModule(Exception):
    __doc__ = 'Extension module missed'
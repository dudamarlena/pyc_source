# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/rawkit/errors.py
# Compiled at: 2015-07-19 23:38:28
# Size of source mod 2**32: 651 bytes
""":mod:`rawkit.errors` --- Errors thrown by rawkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These errors are thrown by various rawkit functions and methods when things go
wrong. They will only be raised by rawkit; for lower level errors raised by the
underlying libraw bindings, see :class:`libraw.errors`.
"""

class InvalidFileType(ValueError):
    __doc__ = '\n    Raised when an invalid file type or file extension is passed to a rawkit\n    method.\n    '


class NoFileSpecified(ValueError):
    __doc__ = '\n    Raised when the method or function excpects a `filename` argument, but no\n    file name (or a value of `None`) was specified.\n    '
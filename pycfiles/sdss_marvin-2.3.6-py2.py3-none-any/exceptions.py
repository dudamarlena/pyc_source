# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/marvin_brain/python/brain/core/exceptions.py
# Compiled at: 2018-01-12 14:08:14
"""

exceptions.py

Licensed under a 3-clause BSD license.

Revision history:
    13 Feb 2016 J. Sánchez-Gallego
      Initial version

"""
from __future__ import division
from __future__ import print_function
__all__ = [
 'BrainError', 'BrainUserWarning', 'BrainSkippedTestWargning',
 'BrainNotImplemented', 'BrainApiAuthError']

class BrainError(Exception):
    pass


class BrainApiAuthError(BrainError):
    pass


class BrainNotImplemented(BrainError):
    """A Brain exception for not yet implemented features."""

    def __init__(self, message=None):
        message = 'This feature is not implemented yet.' if not message else message
        super(BrainNotImplemented, self).__init__(message)


class BrainMissingDependence(BrainError):
    """A custom exception for missing dependences."""
    pass


class BrainWarning(Warning):
    """Base warning for Brain."""
    pass


class BrainUserWarning(UserWarning, BrainWarning):
    """The primary warning class."""
    pass


class BrainSkippedTestWargning(BrainUserWarning):
    """A warning for when a test is skipped."""
    pass
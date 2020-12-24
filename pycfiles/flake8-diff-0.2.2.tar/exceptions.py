# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/greg/Dropbox/code/dealertrack/flake8-diff/flake8diff/exceptions.py
# Compiled at: 2015-07-13 15:56:52
from __future__ import unicode_literals, print_function
import six

@six.python_2_unicode_compatible
class BaseError(Exception):

    def __str__(self):
        return self.message


class Flake8NotInstalledError(BaseError):
    """
    Exception when run_flake8 installation cannot be found.
    """
    message = b'flake8 installation could not be found. Is it on $PATH?'


class NotLocatableVCSError(BaseError):
    """
    Exceptions for when VCS cannot be determined automatically
    """
    message = b'VCS could not be determined automatically'


class UnsupportedVCSError(BaseError):
    """
    Exception for handling unknown VCS
    """

    def __init__(self, vcs=None):
        msg = b'{0} VCS is not supported'
        self.message = msg.format(vcs)
        super(UnsupportedVCSError, self).__init__()


class VCSNotInstalledError(BaseError):
    """
    Exception for when particular vcs installation
    cannot be found.
    """

    def __init__(self, vcs=None):
        msg = b'VCS "{0}" installation could not be found. Is it on $PATH?'
        self.message = msg.format(vcs)
        super(VCSNotInstalledError, self).__init__()


class WrongVCSSpecified(BaseError):
    """
    Exception for when particular vcs installation
    cannot be found.
    """

    def __init__(self, vcs=None):
        self.message = (b'This is not a "{0}" repository').format(vcs or b'')
        super(WrongVCSSpecified, self).__init__()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\clients\errors.py
# Compiled at: 2017-04-19 05:14:02
from __future__ import unicode_literals

class SCMError(Exception):
    """A generic error from an SCM."""
    pass


class AuthenticationError(Exception):
    """An error for when authentication fails."""
    pass


class MergeError(Exception):
    """An error for when merging two branches fails."""
    pass


class PushError(Exception):
    """An error for when pushing a branch to upstream fails."""
    pass


class AmendError(Exception):
    """An error for when amending a commit fails."""
    pass


class OptionsCheckError(Exception):
    """An error for when command-line options are used incorrectly."""
    pass


class InvalidRevisionSpecError(Exception):
    """An error for when the specified revisions are invalid."""
    pass


class MinimumVersionError(Exception):
    """An error for when software doesn't meet version requirements."""
    pass


class TooManyRevisionsError(InvalidRevisionSpecError):
    """An error for when too many revisions were specified."""

    def __init__(self):
        super(TooManyRevisionsError, self).__init__(b'Too many revisions specified')


class EmptyChangeError(Exception):
    """An error for when there are no changed files."""

    def __init__(self):
        super(EmptyChangeError, self).__init__(b"Couldn't find any affected files for this change.")
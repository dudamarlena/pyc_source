# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/checkpoint/error.py
# Compiled at: 2009-01-07 02:32:05
"""Error classes for Checkpoint"""
from textwrap import dedent
from traceback import format_stack
__all__ = [
 'NoChanges', 'CheckpointBug', 'CheckpointError', 'RepositoryLocked',
 'NotFound', 'InvalidCommand', 'FileError', 'RepositoryError',
 'UnsupportedFileType', 'VersionError', 'UninitializedRepositoryError',
 'MirrorLocked']

class NoChanges(Warning):
    """Indicates no changes were made to repository or directory"""
    pass


class CheckpointBug(Exception):
    """Error indicates a bug in the checkpoint API"""

    def __init__(self, message=''):
        self.message = 'Unrecoverable Error!\n' + message + '\n' + 'Traceback (most recent call last):\n%s' % format_stack() + dedent('\n                This could be a bug in Checkpoint.\n                Please report this bug as described at\n                http://something something something....\n            ')


class CheckpointError(Exception):
    """Base class for anticipated errors in the checkpoint package"""

    def __init__(self, message=None):
        self.message = message
        if self.message is None:
            self.message = dedent(self.__class__.__doc__)
        return


class RepositoryLocked(CheckpointError):
    """Repository is locked."""

    def __init__(self):
        self.message = dedent("\n            --------------------------------------------------------------\n            !!! Repository is Locked! !!!\n        \n            This could be because another process has the repository open.\n    \n            Most likely though, it means the last repository command has \n            failed or crashed, leaving the repository dirty.  Try the \n            'recover' command to attempt to fix the repository.  If that \n            doesn't work, manual crash-recovery may be the only option.  \n            Check the documentation for more information.\n            --------------------------------------------------------------\n            \n        ")


class MirrorLocked(CheckpointError):
    """Mirror is locked."""

    def __init__(self):
        self.message = dedent("\n            --------------------------------------------------------------\n            !!! Mirror is Locked! !!!\n\n            This could be because another process has the mirror open.\n\n            Most likely though, it means the last mirror command has \n            failed or crashed, leaving the mirror dirty.  Try the \n            'recover' command to attempt to fix the mirror.  If that \n            doesn't work, manual crash-recovery may be the only option.  \n            Check the documentation for more information.\n            --------------------------------------------------------------\n            \n        ")


class NotFound(CheckpointError):
    """Specified file or directory does not exist."""

    def __init__(self, path):
        self.message = 'File or directory not found: %r' % path


class InvalidCommand(CheckpointError):
    """Specified command is not a valid Checkpoint command."""
    pass


class FileError(CheckpointError):
    """File operation error - error during rm, copy, mv, etc."""
    pass


class RepositoryError(CheckpointError):
    """Repository operation error - error during read, write, or create."""
    pass


class UninitializedRepositoryError(CheckpointError):
    """Repository must be initialized for this operation to succeed."""
    pass


class UninitializedMirrorError(CheckpointError):
    """Mirror must be initialized for this operation to succeed."""
    pass


class UnsupportedFileType(CheckpointError):
    """Unsupported file type (link, socket, pipe, device) was encountered."""

    def __init__(self, path):
        self.message = 'Unsupported file type: %r' % path


class VersionError(CheckpointError):
    """Repository format is incompatible with this version of Checkpoint."""
    pass
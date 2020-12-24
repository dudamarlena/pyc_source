# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/utils/temp_dir.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import
import logging, os.path, tempfile
from pip._internal.utils.misc import rmtree
logger = logging.getLogger(__name__)

class TempDirectory(object):
    """Helper class that owns and cleans up a temporary directory.

    This class can be used as a context manager or as an OO representation of a
    temporary directory.

    Attributes:
        path
            Location to the created temporary directory or None
        delete
            Whether the directory should be deleted when exiting
            (when used as a contextmanager)

    Methods:
        create()
            Creates a temporary directory and stores its path in the path
            attribute.
        cleanup()
            Deletes the temporary directory and sets path attribute to None

    When used as a context manager, a temporary directory is created on
    entering the context and, if the delete attribute is True, on exiting the
    context the created directory is deleted.
    """

    def __init__(self, path=None, delete=None, kind='temp'):
        super(TempDirectory, self).__init__()
        if path is None and delete is None:
            delete = True
        self.path = path
        self.delete = delete
        self.kind = kind
        return

    def __repr__(self):
        return ('<{} {!r}>').format(self.__class__.__name__, self.path)

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, exc, value, tb):
        if self.delete:
            self.cleanup()

    def create(self):
        """Create a temporary directory and store it's path in self.path
        """
        if self.path is not None:
            logger.debug(('Skipped creation of temporary directory: {}').format(self.path))
            return
        else:
            self.path = os.path.realpath(tempfile.mkdtemp(prefix=('pip-{}-').format(self.kind)))
            logger.debug(('Created temporary directory: {}').format(self.path))
            return

    def cleanup(self):
        """Remove the temporary directory created and reset state
        """
        if self.path is not None and os.path.exists(self.path):
            rmtree(self.path)
        self.path = None
        return
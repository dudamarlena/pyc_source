# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_internal/utils/temp_dir.py
# Compiled at: 2019-02-14 00:35:06
from __future__ import absolute_import
import errno, itertools, logging, os.path, tempfile
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
        """Create a temporary directory and store its path in self.path
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


class AdjacentTempDirectory(TempDirectory):
    """Helper class that creates a temporary directory adjacent to a real one.

    Attributes:
        original
            The original directory to create a temp directory for.
        path
            After calling create() or entering, contains the full
            path to the temporary directory.
        delete
            Whether the directory should be deleted when exiting
            (when used as a contextmanager)

    """
    LEADING_CHARS = '-~.=%0123456789'

    def __init__(self, original, delete=None):
        super(AdjacentTempDirectory, self).__init__(delete=delete)
        self.original = original.rstrip('/\\')

    @classmethod
    def _generate_names(cls, name):
        """Generates a series of temporary names.

        The algorithm replaces the leading characters in the name
        with ones that are valid filesystem characters, but are not
        valid package names (for both Python and pip definitions of
        package).
        """
        for i in range(1, len(name)):
            for candidate in itertools.combinations_with_replacement(cls.LEADING_CHARS, i - 1):
                new_name = '~' + ('').join(candidate) + name[i:]
                if new_name != name:
                    yield new_name

        for i in range(len(cls.LEADING_CHARS)):
            for candidate in itertools.combinations_with_replacement(cls.LEADING_CHARS, i):
                new_name = '~' + ('').join(candidate) + name
                if new_name != name:
                    yield new_name

    def create(self):
        root, name = os.path.split(self.original)
        for candidate in self._generate_names(name):
            path = os.path.join(root, candidate)
            try:
                os.mkdir(path)
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    raise
            else:
                self.path = os.path.realpath(path)
                break

        if not self.path:
            self.path = os.path.realpath(tempfile.mkdtemp(prefix=('pip-{}-').format(self.kind)))
        logger.debug(('Created temporary directory: {}').format(self.path))
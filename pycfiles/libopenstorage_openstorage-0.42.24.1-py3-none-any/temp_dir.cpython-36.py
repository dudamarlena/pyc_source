# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/utils/temp_dir.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 5521 bytes
from __future__ import absolute_import
import errno, itertools, logging, os.path, tempfile
from pip._internal.utils.misc import rmtree
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional
logger = logging.getLogger(__name__)

class TempDirectory(object):
    __doc__ = 'Helper class that owns and cleans up a temporary directory.\n\n    This class can be used as a context manager or as an OO representation of a\n    temporary directory.\n\n    Attributes:\n        path\n            Location to the created temporary directory\n        delete\n            Whether the directory should be deleted when exiting\n            (when used as a contextmanager)\n\n    Methods:\n        cleanup()\n            Deletes the temporary directory\n\n    When used as a context manager, if the delete attribute is True, on\n    exiting the context the temporary directory is deleted.\n    '

    def __init__(self, path=None, delete=None, kind='temp'):
        super(TempDirectory, self).__init__()
        if path is None:
            if delete is None:
                delete = True
        if path is None:
            path = self._create(kind)
        self._path = path
        self._deleted = False
        self.delete = delete
        self.kind = kind

    @property
    def path(self):
        assert not self._deleted, 'Attempted to access deleted path: {}'.format(self._path)
        return self._path

    def __repr__(self):
        return '<{} {!r}>'.format(self.__class__.__name__, self.path)

    def __enter__(self):
        return self

    def __exit__(self, exc, value, tb):
        if self.delete:
            self.cleanup()

    def _create(self, kind):
        """Create a temporary directory and store its path in self.path
        """
        path = os.path.realpath(tempfile.mkdtemp(prefix=('pip-{}-'.format(kind))))
        logger.debug('Created temporary directory: {}'.format(path))
        return path

    def cleanup(self):
        """Remove the temporary directory created and reset state
        """
        self._deleted = True
        if os.path.exists(self._path):
            rmtree(self._path)


class AdjacentTempDirectory(TempDirectory):
    __doc__ = 'Helper class that creates a temporary directory adjacent to a real one.\n\n    Attributes:\n        original\n            The original directory to create a temp directory for.\n        path\n            After calling create() or entering, contains the full\n            path to the temporary directory.\n        delete\n            Whether the directory should be deleted when exiting\n            (when used as a contextmanager)\n\n    '
    LEADING_CHARS = '-~.=%0123456789'

    def __init__(self, original, delete=None):
        self.original = original.rstrip('/\\')
        super(AdjacentTempDirectory, self).__init__(delete=delete)

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
                new_name = '~' + ''.join(candidate) + name[i:]
                if new_name != name:
                    yield new_name

        for i in range(len(cls.LEADING_CHARS)):
            for candidate in itertools.combinations_with_replacement(cls.LEADING_CHARS, i):
                new_name = '~' + ''.join(candidate) + name
                if new_name != name:
                    yield new_name

    def _create(self, kind):
        root, name = os.path.split(self.original)
        for candidate in self._generate_names(name):
            path = os.path.join(root, candidate)
            try:
                os.mkdir(path)
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    raise

            path = os.path.realpath(path)
            break
        else:
            path = os.path.realpath(tempfile.mkdtemp(prefix=('pip-{}-'.format(kind))))

        logger.debug('Created temporary directory: {}'.format(path))
        return path
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/utils/filesystem.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 5948 bytes
import errno, fnmatch, os, os.path, random, sys
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from pip._vendor.retrying import retry
from pip._vendor.six import PY2
from pip._internal.utils.compat import get_path_uid
from pip._internal.utils.misc import format_size
from pip._internal.utils.typing import MYPY_CHECK_RUNNING, cast
if MYPY_CHECK_RUNNING:
    from typing import Any, BinaryIO, Iterator, List, Union

    class NamedTemporaryFileResult(BinaryIO):

        @property
        def file(self):
            pass


else:

    def check_path_owner(path):
        return sys.platform == 'win32' or hasattr(os, 'geteuid') or True
        assert os.path.isabs(path)
        previous = None
        while path != previous:
            if os.path.lexists(path):
                if os.geteuid() == 0:
                    try:
                        path_uid = get_path_uid(path)
                    except OSError:
                        return False
                    else:
                        return path_uid == 0
                return os.access(path, os.W_OK)
            else:
                previous, path = path, os.path.dirname(path)

        return False


    @contextmanager
    def adjacent_tmp_file(path, **kwargs):
        """Return a file-like object pointing to a tmp file next to path.

    The file is created securely and is ensured to be written to disk
    after the context reaches its end.

    kwargs will be passed to tempfile.NamedTemporaryFile to control
    the way the temporary file will be opened.
    """
        with NamedTemporaryFile(delete=False, 
         dir=os.path.dirname(path), 
         prefix=os.path.basename(path), 
         suffix='.tmp', **kwargs) as (f):
            result = cast('NamedTemporaryFileResult', f)
            try:
                yield result
            finally:
                result.file.flush()
                os.fsync(result.file.fileno())


    _replace_retry = retry(stop_max_delay=1000, wait_fixed=250)
    if PY2:

        @_replace_retry
        def replace(src, dest):
            try:
                os.rename(src, dest)
            except OSError:
                os.remove(dest)
                os.rename(src, dest)


    else:
        replace = _replace_retry(os.replace)

def test_writable_dir(path):
    """Check if a directory is writable.

    Uses os.access() on POSIX, tries creating files on Windows.
    """
    while not os.path.isdir(path):
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent

    if os.name == 'posix':
        return os.access(path, os.W_OK)
    return _test_writable_dir_win(path)


def _test_writable_dir_win(path):
    basename = 'accesstest_deleteme_fishfingers_custard_'
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(10):
        name = basename + ''.join((random.choice(alphabet) for _ in range(6)))
        file = os.path.join(path, name)
        try:
            fd = os.open(file, os.O_RDWR | os.O_CREAT | os.O_EXCL)
        except OSError as e:
            try:
                if e.errno == errno.EEXIST:
                    continue
                if e.errno == errno.EPERM or e.errno == errno.EACCES:
                    return False
                raise
            finally:
                e = None
                del e

        else:
            os.close(fd)
            os.unlink(file)
            return True

    raise EnvironmentError('Unexpected condition testing for writable directory')


def find_files(path, pattern):
    """Returns a list of absolute paths of files beneath path, recursively,
    with filenames which match the UNIX-style shell glob pattern."""
    result = []
    for root, dirs, files in os.walk(path):
        matches = fnmatch.filter(files, pattern)
        result.extend((os.path.join(root, f) for f in matches))

    return result


def file_size(path):
    if os.path.islink(path):
        return 0
    return os.path.getsize(path)


def format_file_size(path):
    return format_size(file_size(path))


def directory_size(path):
    size = 0.0
    for root, _dirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            size += file_size(file_path)

    return size


def format_directory_size(path):
    return format_size(directory_size(path))
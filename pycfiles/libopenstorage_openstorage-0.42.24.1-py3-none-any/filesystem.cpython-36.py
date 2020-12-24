# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/utils/filesystem.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 3334 bytes
import os, os.path, shutil, stat
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from pip._vendor.retrying import retry
from pip._vendor.six import PY2
from pip._internal.utils.compat import get_path_uid
from pip._internal.utils.misc import cast
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import BinaryIO, Iterator

    class NamedTemporaryFileResult(BinaryIO):

        @property
        def file(self):
            pass


else:

    def check_path_owner(path):
        if not hasattr(os, 'geteuid'):
            return True
        else:
            previous = None
            while path != previous:
                if os.path.lexists(path):
                    if os.geteuid() == 0:
                        try:
                            path_uid = get_path_uid(path)
                        except OSError:
                            return False

                        return path_uid == 0
                    else:
                        return os.access(path, os.W_OK)
                else:
                    previous, path = path, os.path.dirname(path)

            return False


    def copy2_fixed(src, dest):
        """Wrap shutil.copy2() but map errors copying socket files to
    SpecialFileError as expected.

    See also https://bugs.python.org/issue37700.
    """
        try:
            shutil.copy2(src, dest)
        except (OSError, IOError):
            for f in [src, dest]:
                try:
                    is_socket_file = is_socket(f)
                except OSError:
                    pass
                else:
                    if is_socket_file:
                        raise shutil.SpecialFileError('`%s` is a socket' % f)

            raise


    def is_socket(path):
        return stat.S_ISSOCK(os.lstat(path).st_mode)


    @contextmanager
    def adjacent_tmp_file(path):
        """Given a path to a file, open a temp file next to it securely and ensure
    it is written to disk after the context reaches its end.
    """
        with NamedTemporaryFile(delete=False,
          dir=(os.path.dirname(path)),
          prefix=(os.path.basename(path)),
          suffix='.tmp') as (f):
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
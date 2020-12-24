# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_vendor/pep517/dirtools.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 1129 bytes
import os, io, contextlib, tempfile, shutil, errno, zipfile

@contextlib.contextmanager
def tempdir():
    """Create a temporary directory in a context manager."""
    td = tempfile.mkdtemp()
    try:
        yield td
    finally:
        shutil.rmtree(td)


def mkdir_p(*args, **kwargs):
    """Like `mkdir`, but does not raise an exception if the
    directory already exists.
    """
    try:
        return (os.mkdir)(*args, **kwargs)
    except OSError as exc:
        try:
            if exc.errno != errno.EEXIST:
                raise
        finally:
            exc = None
            del exc


def dir_to_zipfile(root):
    """Construct an in-memory zip file for a directory."""
    buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(buffer, 'w')
    for root, dirs, files in os.walk(root):
        for path in dirs:
            fs_path = os.path.join(root, path)
            rel_path = os.path.relpath(fs_path, root)
            zip_file.writestr(rel_path + '/', '')

        for path in files:
            fs_path = os.path.join(root, path)
            rel_path = os.path.relpath(fs_path, root)
            zip_file.write(fs_path, rel_path)

    return zip_file
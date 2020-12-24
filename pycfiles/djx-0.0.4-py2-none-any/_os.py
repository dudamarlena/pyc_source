# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/_os.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import os, sys, tempfile
from os.path import abspath, dirname, isabs, join, normcase, normpath, sep
from django.core.exceptions import SuspiciousFileOperation
from django.utils import six
from django.utils.encoding import force_text
if six.PY2:
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
if six.PY3 or os.name == b'nt':
    abspathu = abspath
else:

    def abspathu(path):
        """
        Version of os.path.abspath that uses the unicode representation
        of the current working directory, thus avoiding a UnicodeDecodeError
        in join when the cwd has non-ASCII characters.
        """
        if not isabs(path):
            path = join(os.getcwdu(), path)
        return normpath(path)


def upath(path):
    """
    Always return a unicode path.
    """
    if six.PY2 and not isinstance(path, six.text_type):
        return path.decode(fs_encoding)
    return path


def npath(path):
    """
    Always return a native path, that is unicode on Python 3 and bytestring on
    Python 2.
    """
    if six.PY2 and not isinstance(path, bytes):
        return path.encode(fs_encoding)
    return path


def safe_join(base, *paths):
    """
    Joins one or more path components to the base path component intelligently.
    Returns a normalized, absolute version of the final path.

    The final path must be located inside of the base path component (otherwise
    a ValueError is raised).
    """
    base = force_text(base)
    paths = [ force_text(p) for p in paths ]
    final_path = abspathu(join(base, *paths))
    base_path = abspathu(base)
    if not normcase(final_path).startswith(normcase(base_path + sep)) and normcase(final_path) != normcase(base_path) and dirname(normcase(base_path)) != normcase(base_path):
        raise SuspiciousFileOperation((b'The joined path ({}) is located outside of the base path component ({})').format(final_path, base_path))
    return final_path


def symlinks_supported():
    """
    A function to check if creating symlinks are supported in the
    host platform and/or if they are allowed to be created (e.g.
    on Windows it requires admin permissions).
    """
    tmpdir = tempfile.mkdtemp()
    original_path = os.path.join(tmpdir, b'original')
    symlink_path = os.path.join(tmpdir, b'symlink')
    os.makedirs(original_path)
    try:
        try:
            os.symlink(original_path, symlink_path)
            supported = True
        except (OSError, NotImplementedError, AttributeError):
            supported = False
        else:
            os.remove(symlink_path)

    finally:
        os.rmdir(original_path)
        os.rmdir(tmpdir)
        return supported
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/_os.py
# Compiled at: 2018-07-11 18:15:30
import os, stat, sys
from os.path import join, normcase, normpath, abspath, isabs, sep, dirname
from django.utils.encoding import force_text
from django.utils import six
try:
    WindowsError = WindowsError
except NameError:

    class WindowsError(Exception):
        pass


if not six.PY3:
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
if six.PY3 or os.name == 'nt':
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
    if not six.PY3:
        return path.decode(fs_encoding)
    return path


def npath(path):
    """
    Always return a native path, that is unicode on Python 3 and bytestring on
    Python 2.
    """
    if not six.PY3 and not isinstance(path, bytes):
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
        raise ValueError('The joined path (%s) is located outside of the base path component (%s)' % (
         final_path, base_path))
    return final_path


def rmtree_errorhandler(func, path, exc_info):
    """
    On Windows, some files are read-only (e.g. in in .svn dirs), so when
    rmtree() tries to remove them, an exception is thrown.
    We catch that here, remove the read-only attribute, and hopefully
    continue without problems.
    """
    exctype, value = exc_info[:2]
    if exctype is not WindowsError or 'Access is denied' not in str(value):
        raise
    if os.stat(path).st_mode & stat.S_IREAD != stat.S_IREAD:
        raise
    os.chmod(path, stat.S_IWRITE)
    func(path)
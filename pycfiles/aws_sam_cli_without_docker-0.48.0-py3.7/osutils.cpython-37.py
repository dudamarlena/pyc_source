# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/osutils.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 4241 bytes
"""
Common OS utilities
"""
import logging, os, shutil, stat, sys, tempfile
from contextlib import contextmanager
LOG = logging.getLogger(__name__)

@contextmanager
def mkdir_temp(mode=493, ignore_errors=False):
    """
    Context manager that makes a temporary directory and yields it name. Directory is deleted
    after the context exits

    Parameters
    ----------
    mode : octal
        Permissions to apply to the directory. Defaults to '755' because don't want directories world writable

    ignore_errors : boolean
        If true, we will log a debug statement on failure to clean up the temp directory, rather than failing.
        Defaults to False

    Returns
    -------
    str
        Path to the directory

    """
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        os.chmod(temp_dir, mode)
        yield temp_dir
    finally:
        if temp_dir:
            if ignore_errors:
                shutil.rmtree(temp_dir, False, rmtree_callback)
            else:
                shutil.rmtree(temp_dir)


def rmtree_callback(function, path, excinfo):
    """
    Callback function for shutil.rmtree to change permissions on the file path, so that
    it's delete-able incase the file path is read-only.
    :param function: platform and implementation dependent function.
    :param path: argument to the function that caused it to fail.
    :param excinfo: tuple returned by sys.exc_info()
    :return:
    """
    try:
        os.chmod(path=path, mode=(stat.S_IWRITE))
        os.remove(path)
    except OSError:
        LOG.debug('rmtree failed in %s for %s, details: %s', function, path, excinfo)


def stdout():
    """
    Returns the stdout as a byte stream in a Py2/PY3 compatible manner

    Returns
    -------
    io.BytesIO
        Byte stream of Stdout
    """
    return sys.stdout.buffer


def stderr():
    """
    Returns the stderr as a byte stream in a Py2/PY3 compatible manner

    Returns
    -------
    io.BytesIO
        Byte stream of stderr
    """
    return sys.stderr.buffer


def remove(path):
    if path:
        try:
            os.remove(path)
        except OSError:
            pass


@contextmanager
def tempfile_platform_independent():
    _tempfile = tempfile.NamedTemporaryFile(delete=False)
    try:
        yield _tempfile
    finally:
        _tempfile.close()
        remove(_tempfile.name)


def copytree(source, destination, ignore=None):
    """
    Similar to shutil.copytree except that it removes the limitation that the destination directory should
    be present.
    :type source: str
    :param source:
        Path to the source folder to copy
    :type destination: str
    :param destination:
        Path to destination folder
    :type ignore: function
    :param ignore:
        A function that returns a set of file names to ignore, given a list of available file names. Similar to the
        ``ignore`` property of ``shutils.copytree`` method
    """
    if not os.path.exists(destination):
        os.makedirs(destination)
        try:
            shutil.copystat(source, destination)
        except OSError as ex:
            try:
                LOG.debug('Unable to copy file access times from %s to %s', source, destination, exc_info=ex)
            finally:
                ex = None
                del ex

    else:
        names = os.listdir(source)
        if ignore is not None:
            ignored_names = ignore(source, names)
        else:
            ignored_names = set()
    for name in names:
        if name in ignored_names:
            continue
        new_source = os.path.join(source, name)
        new_destination = os.path.join(destination, name)
        if os.path.isdir(new_source):
            copytree(new_source, new_destination, ignore=ignore)
        else:
            shutil.copy2(new_source, new_destination)
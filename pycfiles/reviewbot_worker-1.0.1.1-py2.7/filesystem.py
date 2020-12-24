# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/utils/filesystem.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
import logging, os, shutil, tempfile
from contextlib import contextmanager
tmpdirs = []
tmpfiles = []

@contextmanager
def chdir(path):
    """Temporarily change directory into the given working directory.

    Args:
        path (unicode):
            The directory to operate within.
    """
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


def cleanup_tempfiles():
    """Clean up all temporary files.

    This will delete all the files created by :py:func:`make_tempfile`.
    """
    global tmpdirs
    global tmpfiles
    for tmpdir in tmpdirs:
        try:
            logging.debug(b'Removing temporary directory %s', tmpdir)
            shutil.rmtree(tmpdir)
        except:
            pass

    for tmpfile in tmpfiles:
        try:
            logging.debug(b'Removing temporary file %s', tmpfile)
            os.unlink(tmpfile)
        except:
            pass

    tmpdirs = []
    tmpfiles = []


def make_tempfile(content=None, extension=b''):
    """Create a temporary file and return the path.

    Args:
        content (bytes, optional):
            Optional content to put in the file.

        extension (unicode, optional):
            An optional file extension to add to the end of the filename.

    Returns:
        unicode:
        The name of the new file.
    """
    fd, tmpfile = tempfile.mkstemp(suffix=extension)
    if content:
        os.write(fd, content)
    os.close(fd)
    tmpfiles.append(tmpfile)
    return tmpfile


def make_tempdir():
    """Create a temporary directory and return the path.

    Returns:
        unicode:
        The name of the new directory.
    """
    tmpdir = tempfile.mkdtemp()
    tmpdirs.append(tmpdir)
    return tmpdir
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/tmpfiles.py
# Compiled at: 2016-06-01 04:16:38
__doc__ = '\nFiles added to tmpfiles are removed at program exit.\n'
import os, shutil, atexit
from tempfile import mkstemp, mkdtemp
from . import utils
_FILES = []
_DIRS = []

def _exit_handler():
    """Called at program exit"""
    for f in _FILES:
        try:
            os.unlink(f)
        except OSError:
            pass

    for d in _DIRS:
        try:
            shutil.rmtree(d)
        except OSError:
            pass


def _mkdir(directory):
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as err:
            raise ValueError('Failed to create directory: %s' % err)


def add(filename):
    """
    Remove the named file at program exit.
    """
    if len(_FILES) + len(_DIRS) == 0:
        atexit.register(_exit_handler)
    _FILES.append(filename)


def create(directory=utils.get_tempdir(), prefix='crmsh_'):
    """
    Create a temporary file and remove it at program exit.
    Returns (fd, filename)
    """
    _mkdir(directory)
    fd, fname = mkstemp(dir=directory, prefix=prefix)
    add(fname)
    return (
     fd, fname)


def create_dir(directory=utils.get_tempdir(), prefix='crmsh_'):
    """
    Create a temporary directory and remove it at program exit.
    """
    _mkdir(directory)
    ret = mkdtemp(dir=directory, prefix=prefix)
    if len(_FILES) + len(_DIRS) == 0:
        atexit.register(_exit_handler)
    _DIRS.append(ret)
    return ret
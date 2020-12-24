# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/makesense/utils.py
# Compiled at: 2014-10-21 08:35:55
"""
makesense.utils
------------------

Helper functions used throughout makesense.
"""
from __future__ import unicode_literals
import errno, logging, os, sys, contextlib
PY3 = sys.version > b'3'
if PY3:
    pass
else:
    import codecs

def make_sure_path_exists(path):
    """
    Ensures that a directory exists.
    :param path: A directory path.
    """
    logging.debug((b'Making sure path exists: {0}').format(path))
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False

    return True


def unicode_open(filename, *args, **kwargs):
    """
    Opens a file as usual on Python 3, and with UTF-8 encoding on Python 2.
    :param filename: Name of file to open.
    """
    kwargs[b'encoding'] = b'utf-8'
    if PY3:
        return open(filename, *args, **kwargs)
    return codecs.open(filename, *args, **kwargs)


@contextlib.contextmanager
def work_in(dirname=None):
    """
    Context manager version of os.chdir. When exited, returns to the working
    directory prior to entering.
    """
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)

    return
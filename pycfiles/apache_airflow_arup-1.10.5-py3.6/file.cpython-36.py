# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/file.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 1888 bytes
from __future__ import absolute_import
from __future__ import unicode_literals
import errno, os, shutil
from tempfile import mkdtemp
from contextlib import contextmanager

@contextmanager
def TemporaryDirectory(suffix='', prefix=None, dir=None):
    name = mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
    try:
        yield name
    finally:
        try:
            shutil.rmtree(name)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise e


def mkdirs(path, mode):
    """
    Creates the directory specified by path, creating intermediate directories
    as necessary. If directory already exists, this is a no-op.

    :param path: The directory to create
    :type path: str
    :param mode: The mode to give to the directory e.g. 0o755, ignores umask
    :type mode: int
    """
    try:
        try:
            o_umask = os.umask(0)
            os.makedirs(path, mode)
        except OSError:
            if not os.path.isdir(path):
                raise

    finally:
        os.umask(o_umask)
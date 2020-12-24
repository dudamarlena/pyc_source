# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/file.py
# Compiled at: 2015-06-11 18:25:25
from __future__ import absolute_import
import os, sys
from tempfile import NamedTemporaryFile
from contextlib import contextmanager
from django.core.files.base import File
from django.conf import settings

@contextmanager
def smart_open(filename=None, mode='r', *args, **kwargs):
    if filename and filename != '-':
        fh = open(filename, mode, *args, **kwargs)
    elif '+' in mode:
        raise NotImplementedError("Mode '+' is not supported by smart_open.")
    elif 'a' in mode:
        raise NotImplementedError("Mode 'a' is not supported by smart_open.")
    elif 'w' in mode:
        fh = sys.stdout
    elif 'r' in mode:
        fh = sys.stdin
    try:
        yield fh
    finally:
        if fh is not sys.stdout and fh is not sys.stdin:
            fh.close()


@contextmanager
def tempfile(**kwargs):
    f = NamedTemporaryFile(**kwargs)
    yield f


@contextmanager
def tempfilename(**kwargs):
    """
    Reserve a temporary file for future use.

    This is useful if you want to get a temporary file name, write to it in the
    future and ensure that if an exception is thrown the temporary file is removed.
    """
    kwargs.update(delete=False)
    try:
        f = NamedTemporaryFile(**kwargs)
        f.close()
        yield f.name
    except Exception:
        if os.path.exists(f.name):
            os.unlink(f.name)
        raise


class FileSystemFile(File):
    """
    A filesystem file that can be used with FileSystemStorage.
    """

    def __init__(self, file):
        super(FileSystemFile, self).__init__(file)

    def temporary_file_path(self):
        """
        Returns the full path of this file.
        """
        return self.file.name

    def close(self):
        try:
            return self.file.close()
        except OSError as e:
            if e.errno != 2:
                raise


def makedirs(p):
    """
    A makedirs that avoids a race conditions for multiple processes attempting to create the same directory.
    """
    try:
        os.makedirs(p, settings.FILE_UPLOAD_PERMISSIONS)
    except OSError:
        if not os.path.isdir(p):
            raise
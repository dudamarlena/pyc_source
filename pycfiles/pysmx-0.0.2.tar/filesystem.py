# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/utils/filesystem.py
# Compiled at: 2010-05-30 09:35:01
import os
from pysmvt import settings
from pysutils import NotGiven

def mkdirs(newdir, mode=NotGiven):
    """
        a "safe" verision of makedirs() that will only create the directory
        if it doesn't already exist.  This avoids having to catch an Error
        Exception that might be a result of the directory already existing
        or might be a result of an error creating the directory.  By checking
        for the diretory first, any exception was created by the directory
        not being able to be created.
    """
    if mode is NotGiven:
        mode = settings.default.dir_mode
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired dir, '%s', already exists." % newdir)
    else:
        os.makedirs(newdir, mode)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/naphatkrit/Dropbox/Documents/code/easyci/easyci/utils/contextmanagers.py
# Compiled at: 2015-09-02 22:04:30
import os, shutil, tempfile
from contextlib import contextmanager

@contextmanager
def chdir(path):
    """Change the working directory to `path` for the duration of this context
    manager.

    Args:
        path (str)
    """
    cur_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cur_cwd)


@contextmanager
def temp_dir():
    """Create a temporary folder for the duration of this context manager,
    deleting it afterwards.

    Yields:
        str - path to the temporary folder
    """
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)
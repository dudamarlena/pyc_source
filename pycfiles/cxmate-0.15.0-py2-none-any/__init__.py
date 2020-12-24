# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/__init__.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: __init__.py '
import os, atexit, shutil, tempfile
__version__ = '0.12.3'
WORK_DIR = tempfile.mkdtemp(prefix='cxmanage_api-')
atexit.register(lambda : shutil.rmtree(WORK_DIR))

def temp_file():
    """
    Create a temporary file that will be cleaned up at exit.

    :returns: File name of the temporary file created.
    :rtype: string

    """
    file_, filename = tempfile.mkstemp(dir=WORK_DIR)
    os.close(file_)
    return filename


def temp_dir():
    """
    Create a temporary directory that will be cleaned up at exit.

    :returns: Path to the temporary directory created.
    :rtype: string

    """
    return tempfile.mkdtemp(dir=WORK_DIR)
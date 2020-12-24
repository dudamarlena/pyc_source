# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pytff/datasets/__init__.py
# Compiled at: 2016-11-23 11:05:08
from __future__ import unicode_literals
import os, codecs
__doc__ = b'PyTFF datasets'
PATH = os.path.abspath(os.path.dirname(__file__))

def get(datasetname, filename):
    """Retrieve a full path to datasetfile or raises an IOError

    """
    path = os.path.join(PATH, datasetname, filename)
    if datasetname and filename and not datasetname.startswith(b'_') and not filename.startswith(b'_') and os.path.isfile(path):
        return path
    raise IOError((b"Dataset file '{}' not exists").format(path))


def info(datasetname):
    """Return information about a given dataset as plain text

    """
    dspath = os.path.join(PATH, datasetname)
    path = os.path.join(dspath, b'_info.txt')
    if os.path.isdir(dspath):
        infotext = b''
        if os.path.isfile(path):
            with codecs.open(path, encoding=b'utf8') as (fp):
                infotext = fp.read()
        return infotext
    raise IOError(b'Dataset do not exists')


def ls():
    """List all existing datasests in dictiornay where every key is a dataset
    name and a value is file of this dataset

    """
    files = {}
    for dirpath, dirnames, filenames in os.walk(PATH):
        basename = os.path.basename(dirpath)
        if dirpath != PATH and not basename.startswith(b'_'):
            container = files.setdefault(basename, [])
            container.extend(fn for fn in filenames if not fn.startswith(b'_'))

    return files
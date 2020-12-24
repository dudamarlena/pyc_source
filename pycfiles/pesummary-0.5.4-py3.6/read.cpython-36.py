# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/io/read.py
# Compiled at: 2020-05-08 05:31:08
# Size of source mod 2**32: 1288 bytes
import importlib

def read(path, package='gw', file_format=None):
    """Read in a results file.

    Parameters
    ----------
    path: str
        path to results file
    package: str
        the package you wish to use
    file_format: str
        the file format you wish to use. Default None. If None, the read
        function loops through all possible options
    """
    module = importlib.import_module('pesummary.{}.file.read'.format(package))
    return getattr(module, 'read')(path, file_format=file_format)
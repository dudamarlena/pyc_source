# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/local/docker/utils.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1023 bytes
"""
Helper methods that aid with changing the mount path to unix style.
"""
import os, re, posixpath, pathlib

def to_posix_path(code_path):
    r"""
    Change the code_path to be of unix-style if running on windows when supplied with an absolute windows path.

    Parameters
    ----------
    code_path : str
        Directory in the host operating system that should be mounted within the container.
    Returns
    -------
    str
        Posix equivalent of absolute windows style path.
    Examples
    --------
    >>> to_posix_path('/Users/UserName/sam-app')
    /Users/UserName/sam-app
    >>> to_posix_path('C:\\Users\\UserName\\AppData\\Local\\Temp\\mydir')
    /c/Users/UserName/AppData/Local/Temp/mydir
    """
    if os.name == 'nt':
        return re.sub('^([A-Za-z])+:', lambda match: posixpath.sep + match.group().replace(':', '').lower(), pathlib.PureWindowsPath(code_path).as_posix())
    return code_path
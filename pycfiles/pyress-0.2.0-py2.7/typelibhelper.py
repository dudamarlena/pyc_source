# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\iress\typelibhelper.py
# Compiled at: 2012-04-24 02:41:05
"""
Useful functions for loading the latest version
of a typelib given just it's IID.

"""
from win32com.client import gencache
from _winreg import OpenKey, HKEY_CLASSES_ROOT, QueryInfoKey, EnumKey

def GetTypelibVersions(IID):
    """
    Returns the list of installed versions of a
    given typelib. Versions are returned as a list
    of two element tuples of the form (major, minor)
    where major, minor are integers.

    """
    versions = []
    with OpenKey(HKEY_CLASSES_ROOT, 'Typelib\\' + IID) as (key):
        subkeycount, _, _ = QueryInfoKey(key)
        for i in range(subkeycount):
            rawversion = EnumKey(key, i)
            if rawversion.count('.') != 1:
                continue
            rawmajor, rawminor = rawversion.split('.')
            major, minor = int(rawmajor, 16), int(rawminor, 16)
            versions.append((major, minor))

    return versions


def GetTypelibLatestVersion(IID):
    """
    Returns a 2 element tuple containing the latest
    major and minor version of the given typelib. Returns
    (None, None) if the typelib wasn't found.

    """
    versions = GetTypelibVersions(IID)
    versions.sort()
    if versions:
        return versions[(-1)]
    else:
        return (None, None)


def EnsureLatestVersion(IID):
    """
    Returns the win32com wrapped module for the
    latest version of the given typelib.

    The Python wrapper will be generated if it
    doesn't already exist.

    """
    major, minor = GetTypelibLatestVersion(IID)
    if major:
        return gencache.EnsureModule(IID, 0, major, minor)
    else:
        return
        return
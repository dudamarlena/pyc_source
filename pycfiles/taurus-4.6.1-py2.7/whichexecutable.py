# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/whichexecutable.py
# Compiled at: 2019-08-19 15:09:29
"""Find path of executable specified by filename"""
__all__ = [
 'whichfile']
__docformat__ = 'restructuredtext'
import os

def whichfile(filename, exts=None):
    r"""Find path of executable specified by filename.
    It Takes into consideration
    the PATHEXT variable (found in MS Windows systems) to try also executable
    names extended with executable extensions.

    Example::

      # on a debian machine with taurus installed in the default path:
      whichfile('taurus') --> '/usr/bin/taurus'

      # or, on a winXP machine:
      whichfile('command') --> 'C:\WINDOWS\system32\command.COM'

    :param filename: (str) executable name.
    :param exts: (list<str>) a list of valid executable extensions.
                 If None given, the PATHEXT environmental variable is used
                 if available.

    :return: (str) absolute path to the executable in the file system
    """
    path = os.getenv('PATH', '').split(os.path.pathsep)
    if exts is None:
        exts = os.getenv('PATHEXT', '').split(os.path.pathsep)
    if '' not in exts:
        exts.insert(0, '')
    for p in path:
        p = os.path.join(p, filename)
        for e in exts:
            pext = p + e
            if os.access(pext, os.X_OK):
                return pext

    return
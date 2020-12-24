# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/HaufeWingDBG/utils.py
# Compiled at: 2012-12-06 04:08:33
"""WingDBG utility methods"""
import os, sys, string, random
if sys.platform != 'win32':
    import pwd
from zLOG import ERROR, LOG

def findInternalWinghome(winghome):
    """Find the pathname of the internal winghome setting.

    On OS X, this may add components to the path that are normally hidden from 
    the user.  Returns None if winghome seem to be valid.

    """
    if not os.path.isdir(winghome):
        return
    else:
        if os.path.isfile(os.path.join(winghome, 'bin', 'wingdb.py')) or os.path.isfile(os.path.join(winghome, 'src', 'wingdb.py')):
            return winghome
        if sys.platform[:6] == 'darwin':
            for extra in ['Contents/MacOS', 'WingIDE.app/Contents/MacOS']:
                internal = os.path.join(winghome, extra)
                if os.path.isfile(os.path.join(internal, 'bin', 'wingdb.py')) or os.path.isfile(os.path.join(internal, 'src', 'wingdb.py')):
                    return internal

        return


def getWingIDEDir(netserver=None):
    """Get the Wing IDE profile directory for the current user.
    
    If the debugger core has not been loaded yet, this may not be precisely
    correct because of the absence of a GetUserName function on win32. 
    Returns None if the dir doesn't and can't exist -- this occurs on
    Unix when the user has no home dir.

    """
    if sys.platform == 'win32':
        if netserver is not None:
            return netserver.abstract._GetUserWingProfileDir()
        else:
            username = getUsername()
            if username is None:
                username = '$(USERNAME)'
            return os.path.join('c:\\Documents and Settings', username, 'Application Data', 'Wing IDE 4')

    else:
        path = os.path.expanduser('~/.wingide4')
        if path in ('~/.wingide4', '/.wingide4'):
            return
        return path
    return


def getUsername(netserver=None):
    """Get the name of the user running the current process. 

    Returns None if name can't be determined.

    """
    try:
        if sys.platform == 'win32':
            if netserver is not None:
                try:
                    return netserver.dbgserver.dbgtracer.GetUserName()
                except OSError:
                    pass

            try:
                import win32api, pywintypes
                try:
                    return win32api.GetUserName()
                except pywintypes.error:
                    pass

            except ImportError:
                pass

            return os.environ.get('USERNAME', None)
        else:
            uid = os.getuid()
            return pwd.getpwuid(uid)[0]

    except (IndexError, OSError):
        return

    return


def generatePRandomPW(pwlen=16, mix_case=1):
    """Generate a pseudo-random password.
    
    Generate a pseudo-random password of given length, optionally 
    with mixed case.  Warning: the randomness is not cryptographically 
    very strong.

    """
    if mix_case:
        chars = string.ascii_letters + string.digits
    else:
        chars = string.ascii_lowercase + string.digits
    pw = ''
    for i in range(0, pwlen):
        pw += random.choice(chars)

    return pw
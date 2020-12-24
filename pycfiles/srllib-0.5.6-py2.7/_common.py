# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\srllib\_common.py
# Compiled at: 2012-05-11 12:09:02
"""Shared stuff.

@var logger: The srllib L{logger<logging.Logger>}.
"""
import logging, platform
__all__ = [
 'get_os', 'get_os_name', 'get_os_version', 'Os_Linux',
 'Os_Windows', 'logger']

class _NullHandler(logging.Handler):
    """Default do-nothing logging handler.

    Since this is a library, we want to swallow log messages, unless the
    application has enabled logging.
    """

    def emit(self, record):
        """Swallow message."""
        pass


logger = logging.getLogger('srllib')
logger.handlers = [
 _NullHandler()]
Os_Linux = 'linux'
Os_Windows = 'windows'
Os_Mac = 'darwin'
Os_Solaris = 'sunos'
OsCollection_Posix = (
 Os_Linux, Os_Mac, Os_Solaris)
Os_Posix = OsCollection_Posix

def get_os():
    """ Get the current operating system.

    Lower-case strings are used to identify operating systems.
    @return: A pair of OS identifier and OS release (e.g. "xp") strings.
    """
    name, host, rls, ver, mach, proc = platform.uname()
    name = name.lower()
    if name == 'microsoft':
        name = rls.lower()
        rls = ver
    return (name, rls)


def get_os_name():
    """ Get the name of the current operating system.

    This convenience function simply returns the first element of the tuple
    returned by L{get_os}.
    """
    return get_os()[0]


def get_os_version():
    """ Get the version of the current operating system.

    This convenience function simply returns the second element of the tuple
    returned by L{get_os}.
    """
    return get_os()[1]
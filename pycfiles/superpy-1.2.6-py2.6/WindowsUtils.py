# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\superpy\utils\WindowsUtils.py
# Compiled at: 2010-06-04 07:07:10
"""Module containing useful utitlies for windows machines.
"""
import logging, os
try:
    import win32api, win32con, win32process
except ImportError, e:
    if os.name in ('nt', ):
        logging.error('\n        Could not import win32api, win32con, win32process due to exception:\n        %s\n        Have you installed python win32 tools?\n        ' % str(e))
    else:
        logging.debug('Unable to do import due to exception: %s\n        If you are not running on windows, this is not a problem.\n        ')

def SetPriority(priority, pid=None):
    """Set priority for current windows process.

    INPUTS:

    -- priority:       String in [IDLE_PRIORITY_CLASS,
                       BELOW_NORMAL_PRIORITY_CLASS, NORMAL_PRIORITY_CLASS,
                       ABOVE_NORMAL_PRIORITY_CLASS, HIGH_PRIORITY_CLASS,
                       REALTIME_PRIORITY_CLASS] indicating priority.

    -- pid=None:       Optional process id. None indicates current process. 

    -------------------------------------------------------

    PURPOSE:    Set priority for windows process.

    """
    logging.debug('Setting priority to %s' % str(priority))
    if pid is None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    if isinstance(priority, (str, unicode)):
        priority = getattr(win32process, priority)
    win32process.SetPriorityClass(handle, priority)
    return


def GetUNCPath(arg):
    """Return full UNC path for a given local path.
    
    INPUTS:
    
    -- arg:        A local path to translate to UNC.
    
    -------------------------------------------------------
    
    RETURNS:    UNC path matching local path.
    
    """
    (drive, path) = os.path.splitdrive(os.path.abspath(arg))
    uncDrive = win32net.NetUseGetInfo(None, drive, 0)['remote']
    fullUNCSrcPath = uncDrive + path
    return fullUNCSrcPath
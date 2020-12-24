# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-ppc/egg/affinity/__init__.py
# Compiled at: 2006-03-22 22:11:37
import sys
if sys.platform in ('win32', ):
    import win32api, win32con, win32process, pywintypes

    def _get_handle_for_pid(pid, ro=True):
        if pid == 0:
            pHandle = win32process.GetCurrentProcess()
        else:
            flags = win32con.PROCESS_QUERY_INFORMATION
            if not ro:
                flags |= win32con.PROCESS_SET_INFORMATION
            try:
                pHandle = win32api.OpenProcess(flags, 0, pid)
            except pywintypes.error, e:
                raise ValueError, e

        return pHandle


    def set_process_affinity_mask(pid, value):
        pHandle = _get_handle_for_pid(pid, False)
        current = win32process.GetProcessAffinityMask(pHandle)[0]
        try:
            win32process.SetProcessAffinityMask(pHandle, value)
        except win32process.error, e:
            raise ValueError, e

        return current


    def get_process_affinity_mask(pid):
        pHandle = _get_handle_for_pid(pid)
        try:
            return win32process.GetProcessAffinityMask(pHandle)[0]
        except win32process.error, e:
            raise ValueError, e


elif sys.platform in 'linux2':
    from _affinity import set_process_affinity_mask, get_process_affinity_mask
else:

    def set_process_affinity_mask(pid, value):
        raise NotImplementedError


    def get_process_affinity_mask(pid):
        raise NotImplementedError
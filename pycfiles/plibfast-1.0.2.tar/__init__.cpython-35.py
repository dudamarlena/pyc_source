# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jacquem/workspace/CTA/CTA_Analysis/PLIBS_8_BASE/PLIB_PYTHON/plibfast/math/__init__.py
# Compiled at: 2016-04-01 09:22:04
# Size of source mod 2**32: 602 bytes
import ctypes, os, numpy as np, sys
__all__ = [
 'reduction']
_path = os.path.dirname(__file__) + '/..'
libvec = np.ctypeslib.load_library('alloc', _path)
libvec.plib_fast_reduction.argtypes = [np.ctypeslib.ndpointer(ctypes.c_float, flags='C_CONTIGUOUS,ALIGNED'), ctypes.c_uint64]
libvec.plib_fast_reduction.restype = ctypes.c_float

def reduction(tab):
    """
        Compute sum of all tab's elements
        Parameters
        ----------
        tab: C_CONTINMGUOUS, ALIGNED numpy array of ctypes.c_float
        Returns
        --------
        sum of all tab's elements
        """
    return libvec.plib_fast_reduction(tab, tab.size)
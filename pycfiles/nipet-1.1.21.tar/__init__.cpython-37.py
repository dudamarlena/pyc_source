# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pawel/Dropbox/NiftyPET/NIPET/niftypet/nipet/dinf/__init__.py
# Compiled at: 2020-01-22 17:43:14
# Size of source mod 2**32: 271 bytes
from .dinf import dev_info

def gpuinfo(extended=False):
    """ Run the CUDA dev_info shared library to get info about the installed GPU devices. 
        """
    if extended:
        info = dev_info(1)
        print(info)
    else:
        info = dev_info(0)
    return info
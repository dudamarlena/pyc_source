# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/gpu.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 1699 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '09/11/2018'
import logging
_logger = logging.getLogger(__name__)

def getNumberOfDevice():
    try:
        import pycuda
        from pycuda import compiler
        import pycuda.driver as drv
        drv.init()
        return drv.Device.count()
    except:
        _logger.error('fail to discover the number of gpu')
        return
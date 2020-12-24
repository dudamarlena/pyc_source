# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Documents/VentasMedicas/openpay_python/build/lib/openpay/util.py
# Compiled at: 2018-02-27 01:49:10
# Size of source mod 2**32: 233 bytes
import logging, sys
logger = logging.getLogger('stripe')
__all__ = [
 'utf8']

def utf8(value):
    if isinstance(value, str) and sys.version_info < (3, 0):
        return value.encode('utf-8')
    else:
        return value
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/titi/aha/pythonpath/eagexp/__init__.py
# Compiled at: 2012-12-04 11:50:06
"""
https://github.com/ponty/eagexp
"""
import logging
USE_DISPLAY = 0
try:
    from pyvirtualdisplay.display import Display
    USE_DISPLAY = 1
except:
    import warnings
    warnings.warn('pyvirtualdisplay was not found, no background GUI work is possible')

__version__ = '0.1.0'
log = logging.getLogger(__name__)
log.debug('version=' + __version__)
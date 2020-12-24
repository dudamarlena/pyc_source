# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/guillem.cabrera/pyvtt/build/lib/pyvtt/__init__.py
# Compiled at: 2018-03-05 05:29:37
# Size of source mod 2**32: 560 bytes
from pyvtt.vtttime import WebVTTTime
from pyvtt.vttitem import WebVTTItem
from pyvtt.vttfile import WebVTTFile
from pyvtt.vttexc import Error, InvalidItem, InvalidTimeString
from pyvtt.version import VERSION, VERSION_STRING
__all__ = [
 'WebVTTFile', 'WebVTTItem', 'WebVTTFile', 'SUPPORT_UTF_32_LE',
 'SUPPORT_UTF_32_BE', 'InvalidItem', 'InvalidTimeString']
ERROR_PASS = WebVTTFile.ERROR_PASS
ERROR_LOG = WebVTTFile.ERROR_LOG
ERROR_RAISE = WebVTTFile.ERROR_RAISE
open = WebVTTFile.open
stream = WebVTTFile.stream
from_string = WebVTTFile.from_string
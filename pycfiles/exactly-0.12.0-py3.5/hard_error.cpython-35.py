# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/hard_error.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 261 bytes
from exactly_lib.common.report_rendering.text_doc import TextRenderer

class HardErrorException(Exception):

    def __init__(self, error: TextRenderer):
        self._error = error

    @property
    def error(self) -> TextRenderer:
        return self._error
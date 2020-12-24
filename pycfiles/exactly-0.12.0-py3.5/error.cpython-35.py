# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/cli/program_modes/help/error.py
# Compiled at: 2016-12-07 11:34:17
# Size of source mod 2**32: 102 bytes


class HelpError(Exception):

    def __init__(self, msg: str):
        self.msg = msg
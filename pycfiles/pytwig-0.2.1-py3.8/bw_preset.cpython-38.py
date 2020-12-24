# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/bw_preset.py
# Compiled at: 2020-02-17 04:03:46
# Size of source mod 2**32: 247 bytes
from pytwig import bw_file
from pytwig import bw_object

class BW_Preset_File(bw_file.BW_File):

    def __init__(self):
        super().__init__('preset')
        self.contents = bw_object.BW_Object(1377)

    def get_preset(self):
        return self.contents.get(5153)
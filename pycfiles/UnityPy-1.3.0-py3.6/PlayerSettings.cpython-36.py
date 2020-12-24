# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\PlayerSettings.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 1570 bytes
from .Object import Object

class PlayerSettings(Object):

    def __init__(self, reader):
        super().__init__(reader=reader)
        if self.version[0] > 5 or self.version[0] == 5 and self.version[1] >= 4:
            self.productGUID = reader.read_bytes(16)
        else:
            self.AndroidProfiler = reader.read_boolean()
            reader.align_stream()
            self.defaultScreenOrientation = reader.read_int()
            self.targetDevice = reader.read_int()
            if self.version[0] < 5 or self.version[0] == 5 and self.version[1] < 3:
                if self.version[0] < 5:
                    self.targetPlatform = reader.read_int()
                    if self.version[0] > 4 or self.version[0] == 4 and self.version[1] >= 6:
                        self.targetIOSGraphics = reader.read_int()
                self.targetResolution = reader.read_int()
            else:
                self.useOnDemandResources = reader.read_boolean()
                reader.align_stream()
        if self.version[0] > 3 or self.version[0] == 3 and self.version[1] >= 5:
            self.accelerometerFrequency = reader.read_int()
        self.companyName = reader.read_aligned_string()
        self.productName = reader.read_aligned_string()
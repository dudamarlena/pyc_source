# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/data/christian/Documents/workspace/Yeti/yeti/modules/datastreamer.py
# Compiled at: 2016-03-05 20:53:53
# Size of source mod 2**32: 303 bytes
import yeti
try:
    import simplestreamer
    imported_simplestreamer = True
except ImportError:
    imported_simplestreamer = False

class DataStreamer(yeti.Module):

    def module_init(self):
        if imported_simplestreamer:
            self.simplestreamer = simplestreamer.SimpleStreamer(5804)
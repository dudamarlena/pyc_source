# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jbn/s/code/foorep/foorep/plugins/pe.py
# Compiled at: 2012-12-14 06:53:15
from foorep import Plugin
from datetime import datetime

class Pe(Plugin):

    def analyze(self, path):
        try:
            import pefile
        except ImportError:
            return

        try:
            pe = pefile.PE(path)
        except pefile.PEFormatError:
            return

        result = {'type': 'pefile', 
           'value': {'image_base': hex(pe.OPTIONAL_HEADER.ImageBase), 
                     'entry_point': hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint), 
                     'machine_type': pefile.MACHINE_TYPE[pe.FILE_HEADER.Machine], 
                     'dll': pe.FILE_HEADER.IMAGE_FILE_DLL, 
                     'subsystem': pefile.SUBSYSTEM_TYPE[pe.OPTIONAL_HEADER.Subsystem], 
                     'timestamp': datetime.fromtimestamp(pe.FILE_HEADER.TimeDateStamp), 
                     'number_of_rva_and_sizes': pe.OPTIONAL_HEADER.NumberOfRvaAndSizes}}
        return result
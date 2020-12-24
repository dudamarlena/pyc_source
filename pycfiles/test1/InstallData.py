# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\InstallData.py
# Compiled at: 2005-10-04 17:52:22
from Ft.Lib.DistExt import InstallMisc, Structures

class InstallData(InstallMisc.InstallMisc):
    __module__ = __name__
    command_name = 'install_data'
    description = 'install read-only platform-independent files'

    def _get_distribution_filelists(self):
        filelists = []
        if self.distribution.has_data_files():
            filelists.extend(self.distribution.data_files)
        return filelists
# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\DistExt\InstallLocalState.py
# Compiled at: 2005-09-18 19:05:02
import InstallMisc

class InstallLocalState(InstallMisc.InstallMisc):
    __module__ = __name__
    command_name = 'install_localstate'
    description = 'install modifiable host-specific data'

    def _get_distribution_filelists(self):
        return self.distribution.localstate_files
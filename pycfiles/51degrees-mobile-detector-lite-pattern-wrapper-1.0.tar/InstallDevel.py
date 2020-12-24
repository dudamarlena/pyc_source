# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\InstallDevel.py
# Compiled at: 2005-09-18 19:05:02
import InstallMisc

class InstallDevel(InstallMisc.InstallMisc):
    __module__ = __name__
    command_name = 'install_devel'
    description = 'install developer files (tests and profiles)'

    def _get_distribution_filelists(self):
        return self.distribution.devel_files
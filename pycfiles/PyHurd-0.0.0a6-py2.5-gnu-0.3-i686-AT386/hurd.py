# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.gnu-0.3-i686-AT386/egg/hurd.py
# Compiled at: 2008-12-29 11:18:19
"""
pyHurd - A pytonish GNU/Hurd
"""
__copyright__ = '\nCopyright (C) 2008 Anatoly A. Kazantsev\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 2 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along\nwith this program; if not, write to the Free Software Foundation, Inc.,\n51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.\n'
from _hurd import IO, File, _getdport
from _fcntl import *

class Port(IO, File):

    def __init__(self, *args, **kwargs):
        IO.__init__(self, *args, **kwargs)

    @staticmethod
    def lookup(filename, flags, mode=0):
        import _glibc
        port_name = _glibc.file_name_lookup(filename, flags, mode)
        if port_name:
            return Port(port_name=port_name)
        else:
            return
        return

    @staticmethod
    def getdport(fd):
        port_name = _getdport(fd)
        if port_name:
            return Port(port_name=port_name)
        else:
            return
        return
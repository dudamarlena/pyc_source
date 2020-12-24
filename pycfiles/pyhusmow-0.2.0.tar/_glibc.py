# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.gnu-0.3-i686-AT386/egg/_glibc.py
# Compiled at: 2008-12-28 13:20:40
__doc__ = '\npyHurd - A pytonish GNU/Hurd\n'
__copyright__ = '\nCopyright (C) 2008 Anatoly A. Kazantsev\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 2 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along\nwith this program; if not, write to the Free Software Foundation, Inc.,\n51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.\n'
import cython
from _mach import MACH_PORT_NULL

@cython.locals(io=IO)
def file_name_lookup(filename, flags, mode=0):
    port = _file_name_lookup(filename, flags, mode)
    if port == _MACH_PORT_NULL:
        return MACH_PORT_NULL
    return port
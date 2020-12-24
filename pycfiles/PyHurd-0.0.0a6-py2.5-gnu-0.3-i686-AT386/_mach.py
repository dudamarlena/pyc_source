# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.gnu-0.3-i686-AT386/egg/_mach.py
# Compiled at: 2008-12-28 13:51:20
"""
pyHurd - A pytonish GNU/Hurd
"""
__copyright__ = '\nCopyright (C) 2008 Anatoly A. Kazantsev\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation; either version 2 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along\nwith this program; if not, write to the Free Software Foundation, Inc.,\n51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.\n'
MACH_PORT_NULL = None

class MachPort:

    def __cinit__(cls, *args, **kwargs):
        cls.mach_port = _MACH_PORT_NULL

    def __init__(self, port_name=MACH_PORT_NULL):
        if port_name:
            self.mach_port = port_name

    def __dealloc__(self):
        mach_port_deallocate(mach_task_self(), self.mach_port)
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Disks/Physical.py
# Compiled at: 2007-08-31 18:49:26
"""
Module containing the Disk object for a Physical Disk
Inherits from: pyVC.Disks.Base
"""
__revision__ = '$Revision: 296 $'
from pyVC.Disks import Base

class Disk(Base.Disk):
    __revision__ = '$Revision: 296 $'

    def __init__(self, realmachines, path, **keywords):
        Base.Disk.__init__(self, realmachines, path, **keywords)
        from pyVC.errors import DiskError
        for realmachine in realmachines:
            if not realmachine.exists(self.path):
                raise DiskError, ('ERROR: Could not open disk device %s.' % self.path,
                 1,
                 realmachine.hostname)

    def __str__(self):
        return self.path

    def qemu(self, disks):
        return '-%s %s' % (disks.pop(0), self.path)

    def uml(self, disks):
        return '%s=%s' % (disks.pop(0), self.path)

    def xen(self, disks):
        from lxml.etree import Element, SubElement
        disk = Element('disk', type='block')
        SubElement(disk, 'driver', name='phy')
        SubElement(disk, 'source', dev=str(self.path))
        SubElement(disk, 'target', dev=str(disks.pop(0)))
        return disk

    def __repr__(self):
        return 'Disk(%s, device = "%s")' % (self.__realmachines, self.path)
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/pyVC/Disks/Floppy.py
# Compiled at: 2007-08-31 18:49:26
__revision__ = '$Revision: 278 $'
from pyVC.Disks import Base

class Disk(Base.Disk):
    __revision__ = '$Revision: 278 $'

    def __init__(self, realmachines, path, **keywords):
        from pyVC.errors import DiskError
        Base.Disk.__init__(self, realmachines, path, **keywords)
        for realmachine in realmachines:
            if not realmachine.isfile(self.path):
                if 'images_path' in realmachine.config['global'] and not realmachine.isfile(realmachine.config['global']['images_path'] + '/' + self.path):
                    raise DiskError, ('Could not open floppy image %s.' % self.path,
                     0,
                     realmachine.hostname)

    def __str__(self):
        return self._file

    def qemu(self, disks):
        return '-%s %s' % (disks.pop(0), self.path)

    def uml(self, disks):
        return '%s=%s' % (disks.pop(0), self.path)

    def xen(self, disks):
        from lxml.etree import Element, SubElement
        disk = Element('disk', type='file')
        SubElement(disk, 'source', file=str(self.path))
        SubElement(disk, 'target', dev=str(disks.pop(0)))
        return disk

    def __repr__(self):
        return 'Disk(%s, file = "%s")' % (self.__realmachines, self.path)
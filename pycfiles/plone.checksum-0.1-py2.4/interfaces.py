# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plone/checksum/interfaces.py
# Compiled at: 2008-04-01 12:04:28
from zope import interface
from zope.interface.common.mapping import IIterableMapping

class IChecksumManager(IIterableMapping):
    """A mapping where keys are identifiers and values are `IChecksum`
    objects.
    """
    __module__ = __name__

    def update_checksums():
        """Calculate and update all checksums
        """
        pass


class IChecksum(interface.Interface):
    __module__ = __name__

    def __str__():
        """Read the stored checksum or 'n/a'
        """
        pass

    def calculate():
        """Caclculate checksum
        """
        pass

    def update(checksum=None):
        """Store checksum.  If not given, I will calculate() myself.
        """
        pass

    def value():
        """Return the value that our checksum calculation is based on.
        Befware though that this will return all kinds of objects!"""
        pass
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/ZipFileWrapper.py
# Compiled at: 2019-12-11 16:37:58
"""Provide a ZipFile class which wraps the functionlity from zipfile
   Sutekh needs."""
from sutekh.base.io.BaseZipFileWrapper import BaseZipFileWrapper
from sutekh.io.PhysicalCardSetWriter import PhysicalCardSetWriter
from sutekh.io.IdentifyXMLFile import IdentifyXMLFile

class ZipFileWrapper(BaseZipFileWrapper):
    """The zip file wrapper.

       This provides useful functions for dumping + extracting the
       database to / form a zipfile"""

    def __init__(self, sZipFileName):
        super(ZipFileWrapper, self).__init__(sZipFileName)
        self._cWriter = PhysicalCardSetWriter
        self._cIdentifyFile = IdentifyXMLFile

    def _check_forced_reparent(self, oIdParser):
        """Do we need to force the parent of this to be 'My Collection'?"""
        if self._bForceReparent and oIdParser.type == 'PhysicalCardSet':
            return True
        return False

    def _should_force_reparent(self, oIdParser):
        """Check if we may need to force reparenting of card sets to
           'My Collection'"""
        if oIdParser.type == 'PhysicalCard':
            return True
        return False

    def _check_refresh(self, oIdParser):
        """Does this require we refresh the card set list?"""
        if oIdParser.type == 'PhysicalCard' or oIdParser.type == 'PhysicalCardSet':
            return True
        return False